# -* coding: utf-8 -*-

#################################################################################
# This file is part of EVALLIES.                                                #
#                                                                               #
# EVALLIES is a python package for lifelong learning speaker diarization.       #
# Home page: https://git-lium.univ-lemans.fr/Larcher/evallies                   #
#                                                                               #
# EVALLIES is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU LLesser General Public License as               #
# published by the Free Software Foundation, either version 3 of the License,   #
# or (at your option) any later version.                                        #
#                                                                               #
# EVALLIES is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU Lesser General Public License for more details.                           #
#                                                                               #
# You should have received a copy of the GNU Lesser General Public License      #
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.              #
#                                                                               #
#################################################################################
"""
Copyright 2020-2021 Anthony Larcher, Meysam Shamsi & Yevhenii Propkopalo

    :mod:`lium_baseline.system`

"""

import copy
import h5py
import logging
import numpy
import os
import pandas
import pickle
import scipy
import sidekit
import s4d
import torch
import yaml


from .utils import add_show_in_id
from .utils import allies_write_diar
from .utils import customize_threshold
from .utils import keep_recurring_speakers
from .utils import remove_show_from_id

from sidekit.nnet.xvector import extract_embeddings_per_speaker


def bic_linear_segmentation(init_diar, cep, model_cfg):
    """

    :param init_diar:
    :param cep:
    :param model_cfg:
    :return:
    """
    output_diar = init_diar.copy_structure()
    spk_lst = init_diar.unique('cluster')
    for spk in spk_lst:
        c = init_diar.filter('cluster', '==', spk)
        if c.duration() > 50:
            output_diar.append_diar(c)
    
    output_diar = s4d.segmentation(cep, output_diar)
    output_diar = s4d.bic_linear(cep, output_diar, model_cfg['first_seg']['thr_l'], sr=False)


    return output_diar


def init_clustering(init_diar, cep, model_cfg, vad_type="none"):
    """
    Calculate HAC diarization for a given segmentation
    Starting from a

    :param init_diar: initial segmentation
    :param cep: matrix of cepstral coefficient to run the BIC segmentation on
    :param model_cfg: a dictionary describing the system parameters
    :return: a s4d.Diar object (list of segments with clusterID, start and stop time
    """

    # Bic_lin is only applied when starting from a VAD segmentation or from UEM
    if vad_type != "reference":
        output_diar = bic_linear_segmentation(init_diar, cep, model_cfg)
    else:
        output_diar = init_diar

    # Apply BIC HAC
    cluster = s4d.clustering.hac_bic.HAC_BIC(cep, output_diar, model_cfg['first_seg']['thr_h'], sr=False)
    output_diar = cluster.perform()

    # Viterbi decoding is only applied when starting from a VAD segmentation or from scratch
    if vad_type != "reference":
        output_diar = s4d.viterbi.viterbi_decoding(cep, output_diar, model_cfg['first_seg']['thr_vit'])


    return output_diar


def vec2link(model_cfg, vec, current_diar, model=None):
    """

    :param model_cfg: a dictionary describing the system parameters
    :param vec:
    :param current_diar:
    :param model:
    :param model:
    :return:
    """

    if model_cfg["model"]["type"] == "lium_xv":
        return vec2link_xv(model_cfg, vec, current_diar)
    else:
        return vec2link_iv(model, model_cfg, vec, current_diar)


def vec2link_xv(model_cfg, xv_vec, current_diar):
    """

    :param model_cfg: a dictionary describing the system parameters
    :param xv_vec:
    :param current_diar:
    :return:
    """
    th_w = model_cfg["within_show"]["th_w"]

    #within_iv_mean = xv_vec.mean_stat_per_model()
    within_iv_mean = xv_vec

    # Compute scores
    ndx = sidekit.Ndx(models=within_iv_mean.modelset, testsegs=within_iv_mean.modelset)

    scores = sidekit.iv_scoring.cosine_scoring(within_iv_mean, within_iv_mean, ndx,
                                               wccn=None,
                                               check_missing=False)

    # Use 2 gaussian to shift the scores
    #if scores.modelset.shape[0] > 2:
    #    th_w = customize_threshold(scores, th_w)

    scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())

    # Make the cluster names consistent
    for idx in range(len(scores.modelset)):
        scores.modelset[idx] = xv_vec.modelset[idx]

    ######################################################################################
    # MODIFIED AS WE NOW USE COSINE SIMILARITIES
    ######################################################################################
    # Get the linkage matrix from the scores
    distances, th = s4d.clustering.hac_utils.scores2distance(scores, th_w)
    distance_sym = scipy.spatial.distance.squareform(distances)

    link = scipy.cluster.hierarchy.linkage(distance_sym, method=model_cfg['within_show']['hac_method'])

    return scores, link, th


def vec2link_iv(model, model_cfg, iv_vec, current_diar):
    """

    :param model:
    :param model_cfg: a dictionnary describing the system parameters
    :param iv_vec:
    :param current_diar:
    :return:
    """

    iv_vec.spectral_norm_stat1(model["model_iv"].norm_mean, model["model_iv"].norm_cov)
    # Compute scores
    ndx = sidekit.Ndx(models=iv_vec.modelset, testsegs=iv_vec.modelset)
    scores = sidekit.iv_scoring.fast_PLDA_scoring(iv_vec, iv_vec, ndx,
                                                  model["model_iv"].plda_mean,
                                                  model["model_iv"].plda_f,
                                                  model["model_iv"].plda_sigma,
                                                  p_known=0.0,
                                                  scaling_factor=1.0,
                                                  check_missing=False)
    scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())

    for idx in range(len(scores.modelset)):
        scores.modelset[idx] = xv_vec.modelset[idx]

    # Get the linkage matrix from the scores
    distances, th = s4d.clustering.hac_utils.scores2distance(scores, model_cfg['within_show']['th_w'])
    distance_sym = scipy.spatial.distance.squareform(distances)

    link = scipy.cluster.hierarchy.hac.linkage(distance_sym, method=model_cfg['within_show']['hac_method'])

    return scores, link, th


def extract_vectors(current_diar, root_folder, model_cfg, show, model=None):
    """
    Calculate the vectors (x/i) per cluster and segments according to the diarization
    and save in {file_path}/{out_file_name}

    :param root_folder:
    :param current_diar:
    :param model_cfg: a dictionary describing the system parameters
    :param model:
    :param show: file name correspond to wav file (used only for lium_iv case)
    :return: Extracted vectors correspond to input diarization
    """
    #if os.path.exists(f"{model_cfg['tmp_dir']}/feat/{show}.idmap.h5"):
    #    os.remove(f"{model_cfg['tmp_dir']}/feat/{show}.idmap.h5")

    if model_cfg["model"]["type"] == "lium_iv":

        feature_path = model_cfg['tmp_dir'] + "/feat/"
        if os.path.exists(f"{feature_path}/{show}.cep.h5"):
            os.remove(f"{feature_path}/{show}.cep.h5")

        fe = s4d.utils.get_feature_extractor(f"{root_folder}/wav/{show}.wav", type_feature_extractor='sid')
        idmap_bic = fe.save_multispeakers(current_diar.id_map(),
                                          output_feature_filename=f"{feature_path}/{show}.cep.h5",
                                          keep_all=False)
        # idmap_bic.write(f"{feature_path}/{show}.idmap.h5")
        fs = s4d.utils.get_feature_server(f"{feature_path}/{show}.cep.h5", 'sid')

        # Extract i-vectors per cluster
        current_vec = model["model_iv"].train(fs, idmap_bic, normalization=False)
        # Extract i-vectors per speaker
        current_vec_per_segment = model["model_iv"].train_per_segment(fs,
                                                                      current_diar.id_map(),
                                                                      normalization=False)

    elif model_cfg["model"]["type"] == "lium_xv":

        """
        current_im = current_diar.id_map()
        current_im.start = current_im.start * 160
        current_im.stop = current_im.stop * 160
        if os.path.exists(f"{model_cfg['tmp_dir']}/{show}.idmap.h5"):
            os.remove(f"{model_cfg['tmp_dir']}/{show}.idmap.h5")
        current_im.write(f"{model_cfg['tmp_dir']}/{show}.idmap.h5")
        current_vec_per_cluster = extract_embeddings_per_speaker(
            idmap_name=f"{model_cfg['tmp_dir']}/{show}.idmap.h5",
            model_filename=f"{model_cfg['model_dir']}/best_xtractor.pt",
            data_root_name=f"{model_cfg['wav_dir']}",
            device=torch.device("cuda"),
            transform_pipeline={},
            num_thread=5)

        diar_seg=copy.deepcopy(current_diar)
        for i in range(len(diar_seg)):
            diar_seg[i]["cluster"]="tmp_"+str(i)
        current_im = diar_seg.id_map()
        current_im.start = current_im.start * 160
        current_im.stop = current_im.stop * 160
        if os.path.exists(f"{model_cfg['tmp_dir']}/{show}_seg.idmap.h5"):
            os.remove(f"{model_cfg['tmp_dir']}/{show}_seg.idmap.h5")
        current_im.write(f"{model_cfg['tmp_dir']}/{show}_seg.idmap.h5")

        current_vec_per_segment = extract_embeddings_per_speaker(
            idmap_name=f"{model_cfg['tmp_dir']}/{show}_seg.idmap.h5",
            model_filename=f"{model_cfg['model_dir']}/best_xtractor.pt",
            data_root_name=f"{model_cfg['wav_dir']}",
            device=torch.device("cuda"),
            transform_pipeline={},
            num_thread=5)
        """

        #
        current_im = current_diar.id_map()
        # current_im.write(f"{file_path}/{show}.idmap.h5")

        # Get X-vector extractor name
        xtractor_name = model_cfg['tmp_dir'] + "model/best_xtractor.pt"

        # Extract 1 x-vector per segment
        current_vec_per_segment = sidekit.nnet.xvector.extract_embeddings(idmap_name=current_im,
                                                                          model_filename=xtractor_name,
                                                                          data_root_name=f"{root_folder}/wav/",
                                                                          device=torch.device("cuda"),
                                                                          file_extension="wav",
                                                                          transform_pipeline={},
                                                                          sliding_window=False,
                                                                          sample_rate=16000,
                                                                          num_thread=5,
                                                                          mixed_precision=False)

        # Extract 1 x-vector per speaker (cluster)
        current_vec_per_cluster = sidekit.nnet.xvector.extract_embeddings_per_speaker(
            idmap_name=current_im,
            model_filename=xtractor_name,
            data_root_name=f"{root_folder}/wav/",
            device=torch.device("cuda"),
            file_extension="wav",
            transform_pipeline={},
            sample_rate=16000,
            mixed_precision=False,
            num_thread=5)

    return current_vec_per_cluster, current_vec_per_segment


def perform_second_seg(model,
                       initial_diar,
                       within_iv,
                       within_iv_per_seg,
                       model_cfg):
    """

    :param model:
    :param initial_diar:
    :param within_iv:
    :param within_iv_per_seg:
    :param model_cfg:
    :return:
    """
    th_w = model_cfg['within_show']['th_w']
    hac_method = model_cfg["within_show"]["hac_method"]

    # Compute scores for each pair of segment to be used in human assisted correction
    # It provides information
    within_iv_mean = within_iv.mean_stat_per_model()
    ndx = sidekit.Ndx(models=within_iv_mean.modelset, testsegs=within_iv_mean.modelset)

    # If I-vectors:
    if model_cfg["model"]["type"] == "lium_iv":

        norm_mean = model["model_iv"].norm_mean
        norm_cov = model["model_iv"].norm_cov
        plda_mean = model["model_iv"].plda_mean
        plda_f = model["model_iv"].plda_f
        plda_sigma = model["model_iv"].plda_sigma

        # Normalize i-vectors
        within_iv_mean.spectral_norm_stat1(norm_mean, norm_cov)

        # If more than one speaker, compute scores
        if within_iv_mean.modelset.shape[0] > 1:
            scores = sidekit.iv_scoring.fast_PLDA_scoring(within_iv_mean, within_iv_mean, ndx,
                                                          plda_mean,
                                                          plda_f,
                                                          plda_sigma,
                                                          p_known=0.0,
                                                          scaling_factor=1.0,
                                                          check_missing=False)

            # Make sure the score matrix is perfectly symmetrical
            scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())

    # If X-vectors
    else:
        # Compute Cosine similarities
        scores = sidekit.iv_scoring.cosine_scoring(within_iv_mean, within_iv_mean, ndx,
                                                   wccn=None,
                                                   check_missing=False,
                                                   device=torch.device("cuda"))

        # Make sure the score matrix is perfectly symmetrical
        scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())

        # Calibration
        #if scores.modelset.shape[0] > 2:
        #    th_w = customize_threshold(scores, th_w)

    # Run HAC clustering
    new_diar, cluster_dict, merge = s4d.clustering.hac_iv.hac_iv(initial_diar,
                                                                 scores,
                                                                 threshold=th_w,
                                                                 method=hac_method)

    # Update the model names of i-vector
    # reverse the cluster dict:
    update_dict = dict()
    for k, v in cluster_dict.items():
        for _v in v:
            update_dict[_v] = k

    for idx, mod in enumerate(within_iv.modelset):
        if mod in update_dict:
            within_iv.modelset[idx] = update_dict[mod]

    for idx, mod in enumerate(within_iv_per_seg.modelset):
        if mod in update_dict:
            within_iv_per_seg.modelset[idx] = update_dict[mod]

    return new_diar, within_iv, within_iv_per_seg


def lium_vad_training(model_cfg, train_data):
    """
    Select data for VAD training
    Train the model
    return the model

    :param model_cfg:
    :param train_data:
    :return:
    """
    # TODO : top update to include the latest version

    # Prepare the training data
    #IL SUFFIT DE GENERER LA LISTE DE FICHIERS ET DE LA STOCKER DANS TMP
    training_file_list = []
    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):
        training_file_list.append(show)
    with open("list/vad_list.lst", "w") as fh:
        fh.write("\n".join(training_file_list))

    # Iterative training
    s4d.nnet.seqTrain(dataset_yaml=model_cfg['model']['vad']['db_yaml'],
                      model_yaml=model_cfg['model']['vad']['model_yaml'],
                      epochs=model_cfg['model']['vad']['epochs'],
                      lr=model_cfg['model']['vad']['lr'],
                      patience=2,
                      tmp_model_name=model_cfg['tmp_dir']+"/model/tmp_vad",
                      best_model_name=model_cfg['tmp_dir']+"/model/best_vad",
                      multi_gpu=True,
                      opt=model_cfg['model']['vad']['opt'],
                      log_interval=10,
                      num_thread=model_cfg['nb_thread']
                      )


def allies_initial_training(system_config, train_data):
    """
    Train the initial Diarization system

    :param system_config:
    :param train_data:
    :return:
    """
    # Load the config file
    with open(system_config, 'r') as fh:
        model_cfg = yaml.load(fh, Loader=yaml.FullLoader)

    if model_cfg["model"]["type"] == "lium_iv":
        model, model_cfg = lium_iv_initial_training(model_cfg, train_data)

    elif model_cfg["model"]["type"] == "lium_xv":
        model, model_cfg = lium_xv_initial_training(model_cfg, train_data)

    return model, model_cfg


def lium_iv_initial_training(model_cfg, train_data):
    """
    Train an i-vector-based diarization system

    Train UBM
    Train TV
    Extract i-vectors
    Train PLDA

    :param model_cfg: a dictionnary describing the system parameters 
    :param train_data: a Data generator used to access the data
    """

    fe = sidekit.FeaturesExtractor(**model_cfg["model"]["feature_extractor"])
    fs_acoustic = sidekit.FeaturesServer(feature_filename_structure=model_cfg['tmp_dir'] + "/feat/{}.h5",
                                         **model_cfg["model"]["vectors"]["ivectors"]["feature_server"])

    train_diar = s4d.diar.Diar()
    train_diar.add_attribut(new_attribut='gender', default='U')
    name_dict = {}
    # iterate on train_data
    if not os.path.isdir(f"{model_cfg['tmp_dir']}/feat"):
        os.makedirs(f"{model_cfg['tmp_dir']}/feat")

    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):

        if not os.path.isfile(f"{model_cfg['tmp_dir']}/feat/{show}.h5"):
            fe.save(show,
                    channel=0,
                    input_audio_filename=filename,
                    output_feature_filename=f"{model_cfg['tmp_dir']}/feat/{show}.h5")

        # Use the ref info to fill the Diar object
        for spk, start, end in zip(ref.speaker, ref.start_time, ref.end_time):
            train_diar.append(show=show,
                              cluster= spk,
                              start=int(round(float(start) * 100.)),
                              stop=int(round(float(end) * 100.))
                              )

    print(f'Training data contains:')
    print("\t" + f'{len(train_diar.unique("show"))} files')
    print("\t" + f'{len(train_diar.unique("cluster"))} speakers')
    print("\t" + f'{len(train_diar)} segments')
    name_dict[show] = int(idx)


    ######################################
    # Train UBM
    ######################################
    ubm_diar = train_diar.copy_structure()
    ubm_diar.segments = train_diar.segments[::20]
    ubm_idmap = ubm_diar.id_map()

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/ubm.h5"):
        ubm = sidekit.Mixture()
        logging.critical("Start UBM training with {} segments".format(len(ubm_idmap.leftids)))
        ubm.EM_split(fs_acoustic,
                     ubm_idmap,
                     model_cfg['model']['vectors']['ivectors']['distrib_nb'],
                     num_thread=model_cfg['nb_thread'],
                     save_partial=False)
        ubm.write(f"{model_cfg['tmp_dir']}/model/ubm.h5")
    else:
        logging.critical("Load UBM from file")
        ubm = sidekit.Mixture(f"{model_cfg['tmp_dir']}/model/ubm.h5")
    logging.critical("\t Done")

    # Get the size of features output by the FeatureServer
    feature_size = ubm.dim()

    ######################################
    # Train TV
    ######################################
    long_seg_diar = copy.deepcopy(train_diar)
    short_seg_diar = long_seg_diar.filter("duration", "<", 100)
    long_seg_diar = long_seg_diar.filter("duration", ">=", 100)
    tv_idmap = long_seg_diar.id_map()

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/TV.h5"):

        if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/tv_stat.h5"):
            # Accumulate sufficient statistics for the training data
            logging.critical("Create StatServer with {} segments".format(len(tv_idmap.leftids)) )
            tv_stat = sidekit.StatServer(tv_idmap,
                                         distrib_nb=ubm.get_distrib_nb(),
                                         feature_size=feature_size)

            tv_stat.accumulate_stat(ubm=ubm,
                                    feature_server=fs_acoustic,
                                    seg_indices=range(tv_stat.segset.shape[0]),
                                    num_thread=model_cfg['nb_thread']
                                    )

            tv_stat = add_show_in_id(tv_stat)
            tv_stat.write(f"{model_cfg['tmp_dir']}/model/tv_stat.h5")
            logging.critical("\t Done")
        else:
            tv_stat = sidekit.StatServer(f"{model_cfg['tmp_dir']}/model/tv_stat.h5")

        # Sufficient statistics are passed to the FactorAnalyser via an HDF5 file handler that stays in memory
        tv_stat_h5f = h5py.File(f'{model_cfg["tmp_dir"]}/tmp_tv_stat.h5', 'a', backing_store=False, driver='core')
        tv_stat.to_hdf5(tv_stat_h5f)

        tv_fa = sidekit.FactorAnalyser()
        logging.critical("Start TV training with {} segments".format(len(tv_stat.modelset)))
        tv_fa.total_variability(tv_stat_h5f,
                                ubm,
                                tv_rank=model_cfg['model']['vectors']['size'],
                                nb_iter=10,
                                min_div=True,
                                tv_init=None,
                                batch_size=300,
                                save_init=False,
                                output_file_name=None,
                                num_thread=model_cfg['nb_thread'])
        tv_fa.write(f"{model_cfg['tmp_dir']}/model/TV.h5")
    else:
        logging.critical("Load TV from file")
        tv_fa = sidekit.FactorAnalyser(f"{model_cfg['tmp_dir']}/model/TV.h5")
    logging.critical("\t Done")

    ######################################
    # Extract I-vectors and train PLDA
    ######################################
    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5"):

        if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5"):
            # Accumulate sufficient statistics for the short segment from training data
            short_seg_idmap = short_seg_diar.id_map()
            short_seg_stat = sidekit.StatServer(short_seg_idmap,
                                                distrib_nb=ubm.get_distrib_nb(),
                                                feature_size= feature_size)
            logging.critical("Start computing short segment statistics: {}".format(len(short_seg_stat.modelset)))

            short_seg_stat.accumulate_stat(ubm=ubm,
                                           feature_server=fs_acoustic,
                                           seg_indices=range(short_seg_stat.segset.shape[0]),
                                           num_thread=model_cfg['nb_thread']
                                           )
            logging.critical("short iv stat ok")
            # Rename in order to get one i-vector per segment
            #tv_stat = add_show_in_id(tv_stat)
            short_seg_stat = add_show_in_id(short_seg_stat)

            short_seg_stat.write(f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5")



        logging.critical("Start extracting i-vectors")
        long_iv = tv_fa.extract_ivectors(ubm, f"{model_cfg['tmp_dir']}/model/tv_stat.h5", num_thread=model_cfg['nb_thread'])
        short_iv = tv_fa.extract_ivectors(ubm, f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5",  num_thread=model_cfg['nb_thread'])

        current_iv = long_iv.merge(long_iv, short_iv)

        current_iv.write(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5")
    else:
        logging.critical("Load IV from file")
        current_iv = sidekit.StatServer(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5")
    logging.critical("\tI-vectors OK")

    # After taking the mean per speaker per file, we rename the clusters in order
    # to get one mean i-vector per speaker per file but same cluster_ID across shows
    current_iv_mean = current_iv.mean_stat_per_model()
    current_iv_mean = remove_show_from_id(current_iv_mean)

    # Normalize i-vectors
    norm_iv = copy.deepcopy(current_iv_mean)
    norm_mean, norm_cov = norm_iv.estimate_spectral_norm_stat1(1, 'sphNorm')
    norm_iv, n_recc, _ = keep_recurring_speakers(norm_iv, rank_F=model_cfg['model']['vectors']['size'], occ_number=2, filter_by_name=True)

    norm_iv.spectral_norm_stat1(norm_mean, norm_cov)
    logging.critical("start PLDA training")
    plda_fa = sidekit.FactorAnalyser()
    plda_fa.plda(norm_iv,
                 rank_f=model_cfg['model']['classifier']['plda_rank'],
                 nb_iter=20,
                 scaling_factor=1.,
                 output_file_name=f"{model_cfg['tmp_dir']}/model/plda",
                 save_partial=False)
    logging.critical("PLDA ok")

    model_iv = s4d.ModelIV()
    model_iv.ubm = ubm
    model_iv.tv = tv_fa.F
    model_iv.tv_mean = tv_fa.mean
    model_iv.tv_sigma = tv_fa.Sigma
    model_iv.norm_mean = norm_mean[:1]
    model_iv.norm_cov = norm_cov[:1]
    model_iv.plda_mean = plda_fa.mean
    model_iv.plda_f = plda_fa.F
    model_iv.plda_g = None
    model_iv.plda_sigma = plda_fa.Sigma
    model_iv.ivectors = current_iv
    model_iv.scores = None
    model_iv.nb_thread = 1

    model = dict()
    model["model_iv"] = model_iv
    model["global_diar"] = train_diar
    pickle.dump(model, open(f"{model_cfg['tmp_dir']}/model/model_allies_baseline_{model_cfg['model']['vectors']['type']}v.p", "wb" ))

    return model, model_cfg



def lium_xv_initial_training(model_cfg, train_data):
    """
    Train an x-vector-based diarization system

    :param model_cfg:
    :param train_data:
    :return:
    """
    # TODO: to update to use the latest version of SIDEKIT, supprimer PLDA et normalisation...

    if not os.path.isdir(f"{model_cfg['tmp_dir']}/model"):
        os.makedirs(f"{model_cfg['tmp_dir']}/model")

    # Train the VAD and save to disk
    #train_data_vad = copy.deepcopy(train_data)
    #if not os.path.isfile(model_cfg['tmp_dir'] + "/model/best_vad.pt"):
    #    lium_vad_training(model_cfg, train_data_vad)

    train_diar = s4d.diar.Diar()
    df_data = dict()
    df_data['speaker_idx'] = []
    df_data['database'] = []
    df_data['speaker_id'] = []
    df_data['start'] = []
    df_data['duration'] = []
    df_data['file_id'] = []
    df_data['gender'] = []
    train_diar.add_attribut(new_attribut='gender', default='U')
    name_dict = {}

    # iterate on train_data
    spk_idx = 0
    speaker_idx = dict()
    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):

        # Use the ref info to fill the Diar object
        # fill a pandas.DataFrame at the sale tim to select data for X-vector extractor training
        for spk, start, end in zip(ref.speaker, ref.start_time, ref.end_time):
            if spk not in speaker_idx:
                speaker_idx[spk] = spk_idx
                spk_idx += 1

            train_diar.append(show=show,
                              cluster= spk,
                              start=int(round(float(start) * 100.)),
                              stop=int(round(float(end) * 100.)))

            df_data["speaker_idx"].append(speaker_idx[spk])
            df_data["speaker_id"].append(spk)
            df_data["start"].append(start)
            df_data["duration"].append(end - start)
            df_data["file_id"].append(show)
            df_data["database"].append("allies_train")
            df_data["gender"].append('u')

    print(f'Training data contains:')
    print("\t" + f'{len(train_diar.unique("show"))} files')
    print("\t" + f'{len(train_diar.unique("cluster"))} speakers')
    print("\t" + f'{len(train_diar)} segments')

    df = pandas.DataFrame(df_data)
    df = df.loc[df['duration'] > model_cfg['model']['vectors']['xvectors']['duration']]
    vc = df.speaker_idx.value_counts()
    selected_df = df[df.speaker_idx.isin(vc.index[vc.values >= model_cfg['model']['vectors']['xvectors']['min_nb_sessions']])]
    speaker_new_idx = dict(zip(list(selected_df.speaker_idx.unique()), numpy.arange(len(list(selected_df.speaker_idx.unique())))))
    selected_df = selected_df.reset_index(drop=True)
    for idx in range(len(selected_df)):
        selected_df.at[idx, 'speaker_idx'] = speaker_new_idx[selected_df.at[idx, 'speaker_idx']]
    
    selected_df.to_csv("list/xvector.csv", index=False)

    training_speaker_nb = len(selected_df.speaker_idx.unique())

    model_cfg["model"]["speaker_nb"] = training_speaker_nb

    # TODO A MODIFIER
    if not os.path.isfile(model_cfg['tmp_dir']+"/model/best_xtractor.pt"):
        sidekit.nnet.xtrain(speaker_number=training_speaker_nb,
                            dataset_yaml=model_cfg['model']['vectors']['xvectors']['db_yaml'],
                            epochs=model_cfg['model']['vectors']['xvectors']['epochs'],
                            lr=model_cfg['model']['vectors']['xvectors']['lr'],
                            model_yaml=model_cfg['model']['vectors']['xvectors']['xtractor_yaml'],
                            model_name=None,
                            loss=model_cfg['model']['vectors']['xvectors']["loss"],
                            tmp_model_name=model_cfg['tmp_dir']+"/model/tmp_xtractor",
                            patience=50,
                            opt=model_cfg['model']['vectors']['xvectors']['opt'],
                            best_model_name=model_cfg['tmp_dir']+"/model/best_xtractor",
                            multi_gpu=True,
                            num_thread=model_cfg['nb_thread'])

    # Extract x-vectors
    train_diar = train_diar.filter("duration", ">=", 100)

    training_idmap = train_diar.id_map()
    #training_idmap.start = training_idmap.start * 160
    #training_idmap.stop = training_idmap.stop * 160

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/training_xv.h5"):
        if model_cfg['model']['vectors']['xvectors']["transforms"] is None:
            model_cfg['model']['vectors']['xvectors']["transforms"] = dict()
        training_xv = sidekit.nnet.xvector.extract_embeddings(idmap_name=training_idmap,
                                                              model_filename=model_cfg['tmp_dir']+"/model/best_xtractor.pt",
                                                              data_root_name=train_data.root_folder + '/wav/',
                                                              device=torch.device("cuda:0"),
                                                              transform_pipeline=model_cfg['model']['vectors']['xvectors']["transforms"])
        training_xv.write(f"{model_cfg['tmp_dir']}/model/training_xv.h5")

    training_xv = sidekit.StatServer(f"{model_cfg['tmp_dir']}/model/training_xv.h5")

    model_iv = s4d.ModelIV()
    model_iv.norm_mean = None
    model_iv.norm_cov = None
    model_iv.plda_mean = None
    model_iv.plda_f = None
    model_iv.plda_g = None
    model_iv.plda_sigma = None
    model_iv.ivectors = training_xv
    model_iv.scores = None
    model_iv.nb_thread = 1

    model = dict()
    model["model_iv"] = model_iv
    model["global_diar"] = train_diar
    pickle.dump(model, open(f"{model_cfg['tmp_dir']}/model/model_allies_baseline_{model_cfg['model']['vectors']['type']}v.p", "wb" ))

    return model, model_cfg


def allies_init_seg(model, model_cfg, show, data_folder, verbose=False):
    """

    :param model:
    :param model_cfg: dictionary containing all required parameters
    :param show:
    :param filename:
    :param data_folder:
    :param verbose:
    :return:
    """
    # TODO add some verbose with logging

    # Initialize the logger
    logging_format = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format, datefmt='%m-%d %H:%M')
    logger = logging.getLogger('Monitoring')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("log/allies.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    #logger.info(yaml.dump(model_cfg, default_flow_style=False))

    first_seg_path = f"{model_cfg['tmp_dir']}/seg/first_th{model_cfg['first_seg']['thr_h']}/"
    second_seg_path = first_seg_path + f"second_th{model_cfg['within_show']['th_w']}/"

    if not os.path.isdir(first_seg_path):
        os.makedirs(first_seg_path)

    # Perform first seg if it doesn't exist
    if not os.path.isfile(f"{first_seg_path}/{show}.mdtm"):

        logger.info("Perform 1st pass of diarization")

        # Extract MFCC if they don't exist yet
        if not os.path.isfile(f"{model_cfg['tmp_dir']}/feat/{show}.h5"):
            logger.info("\t* extract MFCCs")
            fe = sidekit.FeaturesExtractor(**model_cfg["model"]["feature_extractor"])
            fe.save(show,
                    channel=0,
                    input_audio_filename=f"{data_folder}/wav/{show}.wav",
                    output_feature_filename=f"{model_cfg['tmp_dir']}/feat/{show}.h5")

        fs_seg = sidekit.FeaturesServer(feature_filename_structure=model_cfg['tmp_dir'] + "/feat/{}.h5",
                                        **model_cfg["first_seg"]["feature_server"])

        cep, _ = fs_seg.load(show)

        # Load or create the initial segmentation
        # When starting from scratch, Start from UEM
        if model_cfg["model"]["vad"]["type"] == "none":
            init_diar = s4d.Diar.read_uem(f"{model_cfg['model']['vad']['dir']}/{show}.uem")
            logger.info("\t* load initial segmentation from UEM")
        # Start from the reference segmentation
        elif model_cfg["model"]["vad"]["type"] == "reference":
            logger.info("\t* load initial segmentation from reference")
            init_diar = s4d.Diar.read_mdtm(f"{model_cfg['model']['vad']['dir']}/{show}.mdtm")
            for i in range(len(init_diar)):
                init_diar[i]['cluster'] = "tmp_"+str(i)
        # Start from VAD segmentation
        else:
            logger.info(f"\t* load initial segmentation from {model_cfg['model']['vad']['dir']}/{show}.rttm")
            init_diar = s4d.Diar.read_rttm(f"{model_cfg['model']['vad']['dir']}/{show}.rttm")

            init_diar.pad(25)
            init_diar.pack(50)


        # Compute intersection of init_diar with UEM to speed up the process
        uem_diar = s4d.Diar.read_uem(f"{data_folder}/uem/{show}.uem")
        init_diar = s4d.Diar.intersection(init_diar, uem_diar)

        # Run the first pass of segmentation
        logger.info("\t* run 1st clustering")
        current_diar = init_clustering(init_diar, cep, model_cfg, model_cfg["model"]["vad"]["type"])

        # Extract segment representation (i-vectors or x-vectors)
        logger.info("\t* extract vectors")
        first_pass_vec, first_pass_vec_per_seg = extract_vectors(current_diar,
                                                                 data_folder,
                                                                 model_cfg,
                                                                 show,
                                                                 model)

        # save current vectors to disk
        first_pass_vec.write(f"{first_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v.h5")
        first_pass_vec_per_seg.write(f"{first_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v_per_seg.h5")

        # Save current segmentation to disk
        allies_write_diar(current_diar, f"{first_seg_path}/{show}.mdtm")

    # Perform second pass of segmentation if required
    if model_cfg["second_seg"]:

        logger.info("Perform 2nd pass of diarization")

        # Load diarization from the first pass
        current_diar = s4d.Diar.read_mdtm(f"{first_seg_path}/{show}.mdtm")

        # Load vectors from the first pass
        current_vec = sidekit.StatServer(f"{first_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v.h5")
        current_vec_per_seg = sidekit.StatServer(f"{first_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v_per_seg.h5")

        current_diar, current_vec, current_vec_per_seg = perform_second_seg(model,
                                                                            current_diar,
                                                                            current_vec,
                                                                            current_vec_per_seg,
                                                                            model_cfg)


        # re-extract x-vectors based on the final diarization to have correct vectors for the clusters
        final_vec_per_speaker, final_vec_per_seg = extract_vectors(current_diar,
                                                                   data_folder,
                                                                   model_cfg,
                                                                   show,
                                                                   model)

        # Write final vectors
        final_vec_per_speaker.write(f"{second_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v.h5")
        final_vec_per_seg.write(f"{second_seg_path}/{show}_{model_cfg['model']['vectors']['type']}v_per_seg.h5")

        # Write final segmentation
        allies_write_diar(current_diar, f"{second_seg_path}/{show}.mdtm")


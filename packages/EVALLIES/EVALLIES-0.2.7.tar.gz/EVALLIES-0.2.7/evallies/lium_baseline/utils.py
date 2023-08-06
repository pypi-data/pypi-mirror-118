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

    :mod:`lium_baseline.utils`

"""


import copy
import numpy
import sidekit
import sklearn.mixture
import s4d

from ..user_simulation import Reference
# from ..der_single import compute_der
from ..der import der_cross as compute_der

def allies_write_diar(current_diar, filename):
    """

    :param current_diar:
    :param filename:
    :return:
    """
    c_diar = copy.deepcopy(current_diar)
    for idx, seg in enumerate(c_diar):
        c_diar.segments[idx]['start'] = float(seg['start']) / 100.
        c_diar.segments[idx]['stop'] = float(seg['stop']) / 100.

    c_diar.sort(['show', 'start'])
    with open(filename, 'w', encoding="utf8") as fic:
        for line in s4d.Diar.to_string_seg(c_diar, time_float=True):
            fic.write(line)


def add_show_in_id(im):
    """
    Work on StatServer 
    """
    im2 = copy.deepcopy(im)
    max_length = 0
    for mod, seg in zip(im.modelset, im.segset):
        if max_length < 1 + len(mod) + len(seg):
            max_length = 1 + len(mod) + len(seg)
            im2.modelset = im2.modelset.astype('<U{}'.format(max_length))

    for ii, c_id in enumerate(im.modelset):
        im2.modelset[ii] = im.segset[ii] + "$" + c_id

    return im2


def remove_show_from_id(im):
    """
    Work on StatServer
    :param im:
    :return:
    """
    im2 = copy.deepcopy(im)
    im2.modelset = im2.modelset.astype('U', copy=False)
    for idx, c_id in enumerate(im2.modelset):
        im2.modelset[idx] = c_id.split('$')[1]
    return im2

def s4d_to_allies(s4d_segmentation):
    """
    Convert a s4d.Diar object into the proper ALLIES format for segmentation
    :param s4d_segmentation: is a s4d.Diar object
    """
    spk = []
    st = []
    en = []
    for segment in s4d_segmentation:
        spk.append(segment["cluster"])
        st.append(float(segment["start"]) / 100.)
        en.append(float(segment["stop"]) / 100.)
    hyp = Reference(spk, st, en)
    #hyp = {"speaker": spk, "start_time": st, "end_time": en}
    return hyp

def keep_recurring_speakers(iv_ss, rank_F, occ_number=2, filter_by_name=False):
    """
    """
    unique, counts = numpy.unique(iv_ss.modelset, return_counts=True)
    tot_sessions = 0
    kept_idx = []
    for model in range(unique.shape[0]):
        if counts[model] >= occ_number and (
            (
                not (unique[model]).startswith("speaker")
                and not (unique[model]).startswith("presentat")
                and not (unique[model]).startswith("sup+")
                and not (unique[model]).startswith("voix")
                and not (unique[model]).startswith("publicitaire")
                and not (unique[model]).startswith("locuteur")
                and not (unique[model]).startswith("inconnu")
                and not (unique[model]).startswith("traduct")
                and not ("#" in (unique[model]))
                and "_" in (unique[model])
                and filter_by_name
            )
            or (not filter_by_name)
        ):
            kept_idx = numpy.append(
                kept_idx, numpy.where(iv_ss.modelset == unique[model])
            )
            tot_sessions += counts[model]
    #
    flt_iv = sidekit.StatServer()
    flt_iv.stat0 = numpy.ones((tot_sessions, 1))
    flt_iv.stat1 = numpy.ones((tot_sessions, rank_F))
    flt_iv.modelset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.segset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.start = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.stop = numpy.empty(tot_sessions, dtype="|O")
    #
    i = 0
    for model in range(unique.shape[0]):
        if counts[model] >= occ_number and (
            (
                not (unique[model]).startswith("speaker")
                and not (unique[model]).startswith("presentat")
                and not (unique[model]).startswith("sup+")
                and not (unique[model]).startswith("voix")
                and not (unique[model]).startswith("publicitaire")
                and not (unique[model]).startswith("locuteur")
                and not (unique[model]).startswith("inconnu")
                and not (unique[model]).startswith("traduct")
                and not ("#" in (unique[model]))
                and "_" in (unique[model])
                and filter_by_name
            )
            or (not filter_by_name)
        ):
            for ivector in numpy.where(iv_ss.modelset == unique[model])[0]:
                flt_iv.stat1[i, :] = iv_ss.stat1[ivector, :]
                flt_iv.modelset[i] = iv_ss.modelset[ivector]
                flt_iv.segset[i] = iv_ss.segset[ivector]
                flt_iv.start[i] = iv_ss.start[ivector]
                flt_iv.stop[i] = iv_ss.stop[ivector]
                i += 1
    unique = numpy.unique(flt_iv.modelset)
    return flt_iv, unique.shape[0], kept_idx



def apply_link_on_diar(current_diar, cluster_list, full_link_tmp):
    """
    Apply a linkage matrix to a given diarization to merge linked clusters

    :param current_diar:
    :param cluster_list:
    :param full_link_tmp:
    :return: a new diarization that is resulted by current_diar and full_link_tmp
    """

    cluster_dict = dict()
    i = 0

    while i < len(full_link_tmp):

        # the cluster_list of the 2 clusters
        if len(cluster_list) > int(full_link_tmp[i][0]) and len(cluster_list) > int(full_link_tmp[i][1]):
            c0 = cluster_list[int(full_link_tmp[i][0])]
            c1 = cluster_list[int(full_link_tmp[i][1])]

            c_label = ''
            if c1 in cluster_dict:
                c_label = c1
            else:
                for c_clu_dic in cluster_dict:
                    if c1 in cluster_dict[c_clu_dic]:
                        c_label = c_clu_dic

            if c_label != '':
                # c0 is put in c1, and c1 is not empty
                cluster_dict[c_label].append(c0)
            else:
                cluster_dict[c1] = [c0]
                c_label = c1
            if c0 in cluster_dict:
                # remove c0 key
                cluster_dict[c_label] += cluster_dict[c0]
                cluster_dict.pop(c0)
            # add the speaker of the new cluster
            #         if c_label !=c1:
            cluster_list.append(c_label)
            current_diar.rename('cluster', [c0], c_label)
        else:
            #print("in gone", full_link_tmp[i])
            pass

        i += 1

    return current_diar


def check_der(bottomline_diar, bottomline_cluster_list, full_link, ref, uem):
    """
    Applying linkage matrix on a input diarization and calculate DER

    :param bottomline_diar:
    :param bottomline_cluster_list:
    :param full_link: linkage matrix
    :param ref:
    :param uem:
    :return: The DER and new diarization
    """
    diar_tmp = copy.deepcopy(bottomline_diar)
    cluster_list = copy.deepcopy(bottomline_cluster_list)
    full_link_tmp = copy.deepcopy(full_link)

    current_diar = apply_link_on_diar(diar_tmp, cluster_list, full_link_tmp)
    
    hyp = s4d_to_allies(current_diar)
    der, fa_rate, miss_rate, conf_rate, error, time, newspkmap = compute_der([ref], [hyp], [uem], collar = 0.250)
    
#     hyp = s4d_to_allies(current_diar)
#     der, fa_rate, miss_rate, conf_rate, time, newspkmap = compute_der(ref, hyp, uem, {}, 0.250)

    return der, current_diar


def concat_statservers(ss_1, ss_2):
    """
    Concatenate two stat servers
    :param ss_1: first statserver
    :param ss_2: second statserver
    :return:
    """
    tot_sessions = ss_1.modelset.shape[0] + ss_2.modelset.shape[0]

    flt_iv = sidekit.StatServer()
    flt_iv.stat0 = numpy.ones((tot_sessions, 1))
    flt_iv.stat1 = numpy.ones((tot_sessions, ss_1.stat1.shape[1]))
    flt_iv.modelset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.segset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.start = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.stop = numpy.empty(tot_sessions, dtype="|O")

    for idx in range(ss_1.modelset.shape[0]):
        flt_iv.stat1[idx, :] = ss_1.stat1[idx, :]
        flt_iv.modelset[idx] = str(ss_1.modelset[idx])
        flt_iv.segset[idx] = ss_1.segset[idx]
        flt_iv.start[idx] = ss_1.start[idx]
        flt_iv.stop[idx] = ss_1.stop[idx]

    for idx2 in range(ss_2.modelset.shape[0]):
        idx = idx2 + ss_1.modelset.shape[0]
        flt_iv.stat1[idx, :] = ss_2.stat1[idx2, :]
        flt_iv.modelset[idx] = str(ss_2.modelset[idx2])
        flt_iv.segset[idx] = ss_2.segset[idx2]
        flt_iv.start[idx] = ss_2.start[idx2]
        flt_iv.stop[idx] = ss_2.stop[idx2]

    return flt_iv


def rename_models(within_iv, within_diar, existing_models):
    """
    Change model names in order to avoid duplicated ID between files

    :param within_iv:
    :param within_diar:
    :param existing_models:
    :return:
    """
    within_models = dict()
    idx = 0

    for mod in set(within_iv.modelset):
        while f"Spk{idx}" in existing_models:
            idx += 1
        within_models[mod] = f"Spk{idx}"
        idx += 1

    within_iv.modelset = within_iv.modelset.astype('U50')
    for idx, mod in enumerate(within_iv.modelset):
        within_iv.modelset[idx] = within_models[mod]

    for idx, seg in enumerate(within_diar.segments):
        within_diar.segments[idx]['cluster'] = within_models[seg['cluster']]

    return within_iv, within_diar


def customize_threshold(scores, th_w):
    """
    Estimate a bi-Gaussian distribution to fit the input scores and shift the input threshold
    to match the score distribution

    :param scores: the scores to analyse
    :param th_w: the original threshold that is modified in this function
    :return:
    """
    iu1 = numpy.triu_indices(scores.scoremat.shape[0], 1)
    _s = scores.scoremat[iu1][:, None]
    gmm = sklearn.mixture.GaussianMixture(n_components=2,
                                          covariance_type="tied",
                                          init_params="kmeans").fit(_s)
    var = numpy.var(_s)
    means = gmm.means_.squeeze()
    th_w += (-0.5 * (numpy.log(gmm.weights_[:, None] ** 2 / var) - means ** 2 / var).dot([1, -1]) / (
            means / var).dot([1, -1]))[0]

    return th_w

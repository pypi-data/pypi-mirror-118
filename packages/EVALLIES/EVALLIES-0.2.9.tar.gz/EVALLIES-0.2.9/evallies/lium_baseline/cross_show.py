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
import fastcluster
import numpy
import scipy
import sidekit
import torch

from ..user_simulation import MessageToUser
from ..user_simulation import Request

from s4d import Diar
from .utils import s4d_to_allies
from .utils import rename_models
from .utils import concat_statservers



def concat_statservers(ss_1, ss_2):
    out_sessions = numpy.unique(ss_1.modelset).shape[0]

    in_sessions = numpy.unique(ss_2.modelset).shape[0]

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


def compare_longest_segment_id(previous_diar_id, within_diar_id, within_diar, previous_diar, ref_path):
    """

    """
    # Get the time of the middle of the longest segment for previous_diar_id in previous_diar
    tmp_diar = copy.deepcopy(previous_diar)
    tmp_diar.filter("cluster", "==", previous_diar_id).add_duration().sort("duration", reverse=True)
    old_show = tmp_diar[0]["show"]
    old_middle_point = (tmp_diar[0]["stop"] - tmp_diar[0]["start"]) // 2

    # Get the time of the middle of the longest segment for the longest seg within_diar_id in within_diar
    tmp_diar = copy.deepcopy(within_diar)
    tmp_diar.filter("cluster", "==", within_diar_id).add_duration().sort("duration", reverse=True)
    new_show = tmp_diar[0]["show"]
    new_middle_point = (tmp_diar[0]["stop"] - tmp_diar[0]["start"]) // 2

    # Compare the speaker ID for both in the reference
    old_ref = Diar.read_mdtm(f"{ref_path}/{old_show}.mdtm")
    new_ref = Diar.read_mdtm(f"{ref_path}/{new_show}.mdtm")

    old_ref_seg = old_ref.get_seg_at_time(old_middle_point)
    new_ref_seg = new_ref.get_seg_at_time(new_middle_point)

    return old_ref_seg["clsuter"] == new_ref_seg["cluster"]


def check_dif_files(old_modelname,new_modelname,within_diar,prev_diar):
    """
    Check if old_modelname and new_modelname are the same speaker in the reference
    return True if they are
    """
    l=0
    seg_old=0
    for i in range(len(prev_diar)):
        if str(prev_diar[i][1]) == str(old_modelname):
            dur = prev_diar[i][4]-prev_diar[i][3]
            if dur > l:
                l=dur
                seg_old=i
    l=0
    seg_new=0
    for i in range(len(within_diar)):
        if within_diar[i][1]==new_modelname:
            dur = within_diar[i][4]-within_diar[i][3]
            if dur> l:
                l = dur
                seg_new=i
    root = '/lium/buster1/prokopalo/EXPE/2020_12_07_recipe_newProtocol_sincnet/data/ALLIES/'
    ref_old = Diar.read_mdtm(root+'mdtm/'+prev_diar[seg_old][0] +'.mdtm')
    ref_new = Diar.read_mdtm(root+'mdtm/'+within_diar[seg_new][0] +'.mdtm')
    #print(ref_old)
    #print(ref_new)
    #print()
    old= "1"
    new ="2"
    center_old = int((prev_diar[seg_old][3]+prev_diar[seg_old][4])/2)
    center_new = int((within_diar[seg_new][3]+within_diar[seg_new][4])/2)
    for i in range(len(ref_old)):
        #print(ref_old[i])
        if ref_old[i][3] < center_old and ref_old[i][4]>center_old:
            old = ref_old[i][1]
    for i in range(len(ref_new)):
        if ref_new[i][3] < center_new and ref_new[i][4]>center_new:
            new = ref_new[i][1]

    return old == new


def compute_distance_cross_show(previous_vec, previous_diar, within_vec):
    """
    Here we compute the scores considering previous and current clusters and then modify the score matrix
    to enable only clustering of previous and current clusters (no previous/previous and no current/current).

    :param previous_vec:
    :param previous_diar:
    :param within_vec:
    :return:
    """
    # merge the mean_per_model for previous and within
    ll_vec = concat_statservers(previous_vec, within_vec)

    # Compute the score matrix
    ndx = sidekit.Ndx(models=ll_vec.modelset, testsegs=ll_vec.modelset)
    scores = sidekit.iv_scoring.cosine_scoring(ll_vec,
                                               ll_vec,
                                               ndx,
                                               wccn=None,
                                               check_missing=False,
                                               device=torch.device("cuda"))

    scores.scoremat = -0.5 * (scores.scoremat + scores.scoremat.transpose())

    # Constrain the scores to forbid any new clustering between previous shows
    for vec_idx, mod in enumerate(previous_vec.modelset):
        same_indices = numpy.argwhere(previous_vec.modelset != mod)
        scores.scoremat[vec_idx, same_indices] = numpy.inf

    #for iv_idx in range(previous_vec.modelset.shape[0]):
    #    for iv_jdx in range(previous_vec.modelset.shape[0]):
    #        if previous_vec.modelset[iv_idx] == previous_vec.modelset[iv_jdx]:
    #            scores.scoremat[iv_idx, iv_jdx] = scores.scoremat[iv_idx, iv_jdx]
    #        else:
    #            scores.scoremat[iv_idx, iv_jdx] = numpy.inf

    # Add to keep the within show clustering
    for ii in range(previous_vec.modelset.shape[0], ll_vec.modelset.shape[0]):
        for jj in range(previous_vec.modelset.shape[0], ll_vec.modelset.shape[0]):
            if not ll_vec.modelset[ii] == ll_vec.modelset[jj]:
                scores.scoremat[ii, jj] = numpy.inf

    modelset_seg_idx = dict()
    for seg in previous_diar.segments:
        modelset_seg_idx[seg['cluster']] = numpy.where(ll_vec.modelset == seg['cluster'])[0]

    numpy.fill_diagonal(scores.scoremat, 0.0)
    return ll_vec, scores


def cross_show(previous_vec,
               previous_diar,
               within_vec,
               within_diar,
               th_x):
    """

    :param previous_vec:
    :param previous_diar:
    :param within_vec:
    :param within_diar:
    :param th_x:
    :return:
    """
    within_vec_backup = copy.deepcopy(within_vec)
    previous_vec_backup = copy.deepcopy(previous_vec)

    # get the mean_per_model for previous and within
    within_vec_mean = within_vec.mean_stat_per_model()
    previous_vec_mean = previous_vec.mean_stat_per_model()

    """
    Compute distance matrix to perform HAC between previous and within cluster.
    This matrix is normalized to enable/disable clustering between previous/previous
    and within/within clusters
    """
    ll_vec, scores = compute_distance_cross_show(previous_vec_mean, previous_diar, within_vec_mean)

    scores.scoremat += 1.
    th_x += 1.
    numpy.fill_diagonal(scores.scoremat, 0.0)
    squareform_plda = scipy.spatial.distance.squareform(scores.scoremat)
    Z = fastcluster.linkage(squareform_plda, method='complete', preserve_input=True)

    T = scipy.cluster.hierarchy.fcluster(Z, th_x, 'distance')

    # Don't allow to modify the names of previously existing clusters
    # Create a dictionary with old_model_name as key and new_cluster as value
    cluster_dict = dict()
    clusters_by_index = dict()
    for ii in range(T.shape[0]):
        if T[ii] not in clusters_by_index:
            clusters_by_index[T[ii]] = ll_vec.modelset[ii]
        cluster_dict[ll_vec.modelset[ii]] = clusters_by_index[T[ii]]

    # concatenate previous_vec et within_vec
    new_previous_vec = concat_statservers(previous_vec_backup, within_vec_backup)
    new_previous_diar = copy.deepcopy(previous_diar)
    new_previous_diar.segments += within_diar.segments

    # Modify the model names for vectors
    for ii, mod in enumerate(new_previous_vec.modelset):
        new_previous_vec.modelset[ii] = cluster_dict[mod]

    for ii, seg in enumerate(new_previous_diar.segments):
        new_previous_diar.segments[ii]['cluster'] = cluster_dict[seg['cluster']]

    for ii, seg in enumerate(within_diar.segments):
        within_diar.segments[ii]['cluster'] = cluster_dict[seg['cluster']]

    return new_previous_vec, new_previous_diar, within_diar


def cross_show_HAL(previous_vec,
                   previous_diar,
                   within_vec,
                   within_diar,
                   th_x,
                   lim,
                   user,
                   file_info,
                   archive_file_info):
    """

    :param previous_vec:
    :param previous_diar:
    :param within_vec:
    :param within_diar:
    :param th_x:
    :param lim:
    :param user:
    :param file_info:
    :param archive_file_info:
    :return:
    """
    within_vec_backup = copy.deepcopy(within_vec)
    previous_vec_backup = copy.deepcopy(previous_vec)

    # get the mean_per_model for previous and within
    within_vec_mean = within_vec.mean_stat_per_model()
    previous_vec_mean = previous_vec.mean_stat_per_model()

    """
    Compute distance matrix to perform HAC between previous and within cluster.
    This matrix is normalized to enable/disable clustering between previous/previous
    and within/within clusters
    """
    # merge the mean_per_model for previous and within
    ll_vec = concat_statservers(previous_vec_mean, within_vec_mean)

    # Compute the score matrix
    ndx = sidekit.Ndx(models=ll_vec.modelset, testsegs=ll_vec.modelset)
    scores = sidekit.iv_scoring.cosine_scoring(ll_vec,
                                               ll_vec,
                                               ndx,
                                               wccn=None,
                                               check_missing=False,
                                               device=torch.device("cuda"))

    previous_locked_spk = []
    linkage_speaker_dict = {}

    # For each speaker in the current file
    for ii in range(previous_vec_mean.modelset.shape[0], ll_vec.modelset.shape[0]):
        #print(f"Look for matching of current speaker {ii}")

        question_number = 0

        # Get the current name of the speaker
        current_speaker_name = scores.modelset[ii]
        #print(f"current speaker = {current_speaker_name}")

        # get the scores obtained with all previous speakers and rank them
        sorted_idx = numpy.argsort(scores.scoremat[ii][:previous_vec_mean.modelset.shape[0]])[::-1]
        sorted_scores_current_speaker = scores.scoremat[ii, sorted_idx]

        #print(sorted_scores_current_speaker)

        # If one score is above th_x AND that the corresponding previous speaker is not locked
        for jj, previous_spk_idx in enumerate(sorted_idx):

            #print(f"\tCompare to previous speaker {jj}")

            previous_spk_name = ll_vec.modelset[previous_spk_idx]
            #print(f"\tprevious speaker name is: {previous_spk_name}")

            # There  are scores higher than the threshold
            if sorted_scores_current_speaker[previous_spk_idx] > th_x:

                #print(f"\t\tSome scores are above the threshold")

                if not ll_vec.modelset[previous_spk_idx] in previous_locked_spk:
                    # ---> link the speakers
                    linkage_speaker_dict[current_speaker_name] = ll_vec.modelset[previous_spk_idx]
                    # ---> lock the previous speaker
                    previous_locked_spk.append(ll_vec.modelset[previous_spk_idx])
                    # move to next speaker
                    break

            """
            # There are no more scores higher than the threshold
            else:

                if previous_spk_idx not in previous_locked_spk:

                    #print(f"\t\t\tSpeaker not locked")

                    # Get the time of the middle of the longest segment for the longest seg within_diar_id in within_diar
                    tmp_diar = copy.deepcopy(within_diar)
                    tmp_diar = tmp_diar.filter("cluster", "==", current_speaker_name).add_duration()
                    tmp_diar.sort(["duration"], reverse=True)
                    show1 = tmp_diar[0]["show"]
                    #print(f"\t\t{tmp_diar[0]}")
                    t1 = (tmp_diar[0]["stop"] + tmp_diar[0]["start"]) / 200.

                    # Get the time of the middle of the longest segment for previous_diar_id in previous_diar
                    tmp_diar = copy.deepcopy(previous_diar)
                    tmp_diar = tmp_diar.filter("cluster", "==", previous_spk_name).add_duration()
                    tmp_diar.sort(["duration"], reverse=True)
                    show2 = tmp_diar[0]["show"]
                    #print(f"\t\t{tmp_diar[0]}")
                    t2 = (tmp_diar[0]["stop"] + tmp_diar[0]["start"]) / 200.

                    # Ask the question to the user
                    complete_hyp = copy.deepcopy(previous_diar)
                    complete_hyp.append_diar(within_diar)
                    message_to_user = MessageToUser(file_info,
                                                    s4d_to_allies(complete_hyp),
                                                    Request('same', t1, t2, archive_file_info[show2]))

                    keep_questioning, answer = user.validate(message_to_user)

                    question_number += 1

                    if answer.answer:
                        linkage_speaker_dict[current_speaker_name] = ll_vec.modelset[previous_spk_idx]
                        previous_locked_spk.append(ll_vec.modelset[previous_spk_idx])
                        break

                    if question_number > lim:
                        break
            """

    # concatenate previous_vec et within_vec
    new_previous_vec = concat_statservers(previous_vec_backup, within_vec_backup)
    new_previous_diar = copy.deepcopy(previous_diar)
    new_previous_diar.segments += within_diar.segments

    for ii, mod in enumerate(new_previous_vec.modelset):
        if mod in list(linkage_speaker_dict.keys()):
            new_previous_vec.modelset[ii] = linkage_speaker_dict[mod]
    for ii, seg in enumerate(new_previous_diar.segments):
        if seg['cluster'] in list(linkage_speaker_dict.keys()):
            new_previous_diar.segments[ii]['cluster'] = linkage_speaker_dict[seg['cluster']]
    for ii, seg in enumerate(within_diar.segments):
        if seg['cluster'] in list(linkage_speaker_dict.keys()):
            within_diar.segments[ii]['cluster'] = linkage_speaker_dict[seg['cluster']]

    return new_previous_vec, new_previous_diar, within_diar


def allies_cross_show_clustering(show,
                                 show_idx,
                                 archive_vectors,
                                 archive_file_info,
                                 current_diar,
                                 current_vec,
                                 th_x,
                                 lim,
                                 user,
                                 file_info,
                                 human_in_the_loop=False):
    """

    :param show_idx:
    :param archive_vectors:
    :param archive_file_info:
    :param current_diar:
    :param current_vec:
    :param th_x:
    :param lim:
    :param user:
    :param file_info:
    :param uem:
    :param ref:
    :param reference_path:
    :param human_in_the_loop:
    :return:
    """
    # Process first show
    if show_idx == 0:
        archive_vectors["previous_vec"] = copy.deepcopy(current_vec)
        archive_vectors["previous_diar"] = current_diar

        archive_file_info[show] = copy.deepcopy(file_info)

    else:
        archive_file_info[show] = copy.deepcopy(file_info)

        if human_in_the_loop:
            previous_vec, previous_diar, current_diar = cross_show_HAL(previous_vec=archive_vectors["previous_vec"],
                                                                       previous_diar=archive_vectors["previous_diar"],
                                                                       within_vec=current_vec,
                                                                       within_diar=current_diar,
                                                                       th_x=th_x,
                                                                       lim=lim,
                                                                       user=user,
                                                                       file_info=file_info,
                                                                       archive_file_info=archive_file_info)
        else:
            previous_vec, previous_diar, current_diar = cross_show(previous_vec=archive_vectors["previous_vec"],
                                                                   previous_diar=archive_vectors["previous_diar"],
                                                                   within_vec=current_vec,
                                                                   within_diar=current_diar,
                                                                   th_x=th_x)
        archive_vectors["previous_vec"]=previous_vec
        archive_vectors["previous_diar"]=previous_diar

    return archive_vectors, current_diar



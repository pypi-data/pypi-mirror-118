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

    :mod:`lium_baseline.interactive`

"""

import copy
import numpy
import random
import scipy
import sidekit
import sklearn
import s4d
import os

from .system import init_clustering
from .system import extract_vectors
from .system import vec2link
from .utils import allies_write_diar
from .utils import apply_link_on_diar
from .utils import check_der
from .utils import s4d_to_allies
from ..user_simulation import MessageToUser
from ..user_simulation import Request
from ..der_single import *

from ..der import der_cross as compute_der


def create_bottomline_clustering(model, model_cfg, show, current_diar, file_path):
    """
    For a given diarization do subclustering as bottomline clustering :
    the subclustering name is {inital clustering name}_{subcluster name}
    :param model:
    :param model_cfg: a dictionnary describing the system parameters
    :param show: file name
    :param current_diar:
    :param file_path:
    :return:
    """
    fs_seg = sidekit.FeaturesServer(feature_filename_structure=model_cfg['tmp_dir'] + "/feat/{}.h5",
                                    **model_cfg["first_seg"]["feature_server"])
    cep, _ = fs_seg.load(show)

    link_within_clusters_dic = {}
    vec_within_clusters_dic = {}
    bottomline_diar = s4d.Diar()

    for cluster in current_diar.unique("cluster"):
        # Do BIC HAC per cluster
        init_diar = s4d.Diar()
        idx_seg = 0
        for seg in current_diar:
            if seg["cluster"] == cluster:
                # init_clustering needs init_diar without cluster label
                init_diar.append(show=seg["show"], cluster="tmp_" + str(idx_seg), start=seg["start"], stop=seg["stop"])
                idx_seg += 1

        diar_per_cluster = init_clustering(copy.deepcopy(init_diar),
                                           cep,
                                           model_cfg,
                                           "reference")

        #print(f"cluster_{cluster} with {len(diar_per_cluster)} segs changed to "
        #      f"{len(diar_per_cluster.unique('cluster'))} clusters")
        # Creat a diarization with bottom line clustering
        for seg in diar_per_cluster:
            bottomline_diar.append(show=seg["show"],
                                   cluster=cluster + "_" + seg["cluster"],
                                   start=seg["start"],
                                   stop=seg["stop"])
        bottomline_diar.sort()

        if len(diar_per_cluster.unique('cluster')) > 1:
            # calculate vector per cluster
            current_vec_within_cluster, _ = extract_vectors(diar_per_cluster,
                                                            file_path,
                                                            model_cfg,
                                                            show,
                                                            model)
            vec_within_clusters_dic[cluster] = current_vec_within_cluster

            # calculate score and link for each cluster
            scores_within_cluster, link_within_cluster, th_cluster = vec2link(model_cfg,
                                                                              current_vec_within_cluster,
                                                                              diar_per_cluster,
                                                                              model=model)
            link_within_cluster[:, 2] = link_within_cluster[:, 2] - th_cluster
            extend_link_within_cluster = numpy.zeros(
                (link_within_cluster.shape[0], link_within_cluster.shape[1] + 1)) - 1
            extend_link_within_cluster[:, :-1] = link_within_cluster
            link_within_clusters_dic[cluster] = extend_link_within_cluster

    return bottomline_diar, link_within_clusters_dic, vec_within_clusters_dic


def create_bottom_linkage(link_within_clusters_dic, bottomline_cluster_list, vec_within_clusters_dic):
    """
    Merge linkage matrix from subclustering to generate a single linkage matrix with sorted distance
    :param link_within_clusters_dic: a dictionary with cluster name as key and linkage matrix that create subclustering
    :param bottomline_cluster_list: a list of bottomline_clustering that contains
    {baseline clustering label}_{subcluster name}
    :param vec_within_clusters_dic: a dictionary with cluster name as key and extracted vectors for subclustering
    :return: a full linkage matrix that make baseline diarization when it applys to bottomline diarization
    """
    full_link = []

    while True:
        mindis = float('inf')
        idx_mindis = None
        cluster_mindis = None
        # find the a node with min distance:
        for cluster in link_within_clusters_dic:
            for idx, node in enumerate(link_within_clusters_dic[cluster]):
                if node[-1] == -1 and mindis > node[2]:
                    mindis = node[2]
                    idx_mindis = idx
                    cluster_mindis = cluster

        if idx_mindis is not None:
            link_within_clusters_dic[cluster_mindis][idx_mindis][-1] = len(bottomline_cluster_list) + len(full_link)
            new_node = link_within_clusters_dic[cluster_mindis][idx_mindis][:-1]
            within_cluster_modelset_list = list(vec_within_clusters_dic[cluster_mindis].modelset)

            if new_node[0] < len(within_cluster_modelset_list):
                new_node[0] = bottomline_cluster_list.index(cluster_mindis + "_"
                                                            + within_cluster_modelset_list[int(new_node[0])])
            else:
                new_node[0] = link_within_clusters_dic[cluster_mindis][int(new_node[0]
                                                                           - len(within_cluster_modelset_list))][-1]

            if new_node[1] < len(within_cluster_modelset_list):
                new_node[1] = bottomline_cluster_list.index(cluster_mindis
                                                            + "_" + within_cluster_modelset_list[int(new_node[1])])
            else:
                new_node[1] = link_within_clusters_dic[cluster_mindis][int(new_node[1]
                                                                           - len(within_cluster_modelset_list))][-1]

            full_link.append(new_node)
        else:
            break

    return full_link


def combine_upper_and_bottom_linkage(bottom_linkage, link_clusters_tmp, bottomline_cluster_list_tmp, hac_vec):
    """

    :param bottom_linkage: bottom linkage matrix that contain the HAC for spliting baseline clusters
    :param link_clusters_tmp: upper linkage matrix that contain the HAC for merging baseline clusters
    :param bottomline_cluster_list_tmp: a list of bottomline_clustering that contains
    {baseline clustering label}_{subcluster name}
    :param hac_vec:
    :return: a theresold for HAC and the full linkage matrix 
    """
    full_link_tmp = copy.deepcopy(bottom_linkage)
    merging_cluster_list = list(hac_vec.modelset)
    extend_link_clusters = numpy.zeros((link_clusters_tmp.shape[0], link_clusters_tmp.shape[1] + 1)) - 1
    extend_link_clusters[:, :-1] = copy.deepcopy(link_clusters_tmp)

    # idx_node = len(extend_link_clusters)
    for idx_node, node in enumerate(extend_link_clusters):

        extend_link_clusters[idx_node][-1] = len(bottomline_cluster_list_tmp) + len(full_link_tmp)
        new_node = extend_link_clusters[idx_node][:-1]

        if new_node[0] < len(merging_cluster_list):
            cls = bottomline_cluster_list_tmp[0]
            ii = 0
            while not bottomline_cluster_list_tmp[ii].startswith(merging_cluster_list[int(node[0])] + "_"):
                cls = bottomline_cluster_list_tmp[ii]
                ii += 1
#             for cls in bottomline_cluster_list_tmp:
#                 if cls.startswith(merging_cluster_list[int(node[0])] + "_"):
#                     break

            new_node[0] = bottomline_cluster_list_tmp.index(cls)
        else:
            new_node[0] = extend_link_clusters[int(new_node[0] - len(merging_cluster_list))][-1]

        if new_node[1] < len(merging_cluster_list):
            cls = bottomline_cluster_list_tmp[0]
            ii = 0
            while not bottomline_cluster_list_tmp[ii].startswith(merging_cluster_list[int(node[1])] + "_"):
                cls = bottomline_cluster_list_tmp[ii]
                ii += 1
            # for cls in bottomline_cluster_list_tmp:
            #    if cls.startswith(merging_cluster_list[int(node[1])] + "_"):
            #        break
            new_node[1] = bottomline_cluster_list_tmp.index(cls)
        else:
            new_node[1] = extend_link_clusters[int(new_node[1] - len(merging_cluster_list))][-1]

        full_link_tmp.append(new_node)

    # set the lower distance in sub-clustering distance as th_clustering
    if len(bottom_linkage) > 0:
        th_clustering = copy.deepcopy(bottom_linkage)[-1][2]
        for ndx in range(len(copy.deepcopy(bottom_linkage)), len(full_link_tmp)):
            full_link_tmp[ndx][2] += th_clustering
    else:
        th_clustering = full_link_tmp[0][2] - 1

    return th_clustering, full_link_tmp


def correct_link_after_removing_node(number_cluster, node_idx, temporary_link_list, removed_nodes_number):
    """
    correction of nodes naming after removing nodes.
    :param number_cluster:
    :param node_idx:
    :param temporary_link_list:
    :param removed_nodes_number:
    :return: corrected linkage matrix
    """
    removed_node_idx = number_cluster + node_idx

    for idx_link in range(node_idx, len(temporary_link_list) - 1):

        if temporary_link_list[idx_link][0] == removed_node_idx:
            _ = temporary_link_list.pop(idx_link)
            return correct_link_after_removing_node(number_cluster,
                                                    idx_link,
                                                    temporary_link_list,
                                                    removed_nodes_number + 1)

        elif temporary_link_list[idx_link][1] == removed_node_idx:
            _ = temporary_link_list.pop(idx_link)
            return correct_link_after_removing_node(number_cluster,
                                                    idx_link,
                                                    temporary_link_list,
                                                    removed_nodes_number + 1)

        else:
            if temporary_link_list[idx_link][0] > removed_node_idx:
                temporary_link_list[idx_link][0] = temporary_link_list[idx_link][0] - removed_nodes_number

            if temporary_link_list[idx_link][1] > removed_node_idx:
                temporary_link_list[idx_link][1] = temporary_link_list[idx_link][1] - removed_nodes_number

    return temporary_link_list


def question_quality(node,
                     node_list1,
                     node_list2,
                     bottomline_cluster_list,
                     hac_vec_per_seg,
                     init_diar,
                     temporary_link_list,
                     conditional_questioning,
                     question_type,
                     verbos=False):
    """
     Evaluate the question based on conditional_questioning
    :param node_list2:
    :param node: The node correspond to question
    :param node_list1: list of leaves correspond to right branch
    :param node_list1: list of leaves correspond to left branch
    :param bottomline_cluster_list: list of clusters in bottomline diarization
    :param hac_vec_per_seg: StatServer of segments' vectors
    :param init_diar: bottomline diarization
    :param temporary_link_list: the linkage matrix that should br applied to bottomline diarization
                                to have last state of diarization
    :param conditional_questioning: the type of measurement to evaluate questioning
                                    (calinski_harabasz and std (not suggested) is implemented)
    :param question_type: separation or clustering
    :return: True or False as a proposition of the question to be asked
    """
    if conditional_questioning in ['calinski_harabasz', 'silhouette', 'davies_bouldin', 'calinski_harabasz_invs',
                                   'silhouette_invs', 'davies_bouldin_invs']:

        link_tmp = copy.deepcopy(temporary_link_list)
        diar_tmp = copy.deepcopy(init_diar)
        current_diar = apply_link_on_diar(diar_tmp, bottomline_cluster_list, link_tmp)

        if len(current_diar.unique("cluster")) < 2:
            if verbos:
                print(f"{conditional_questioning} is not possible to be calculated for one cluster -> True")
            return True

        current_labels = []
        for seg in current_diar:
            current_labels.append(seg['cluster'])

        if "calinski_harabasz" in conditional_questioning:
            current_score = sklearn.metrics.calinski_harabasz_score(hac_vec_per_seg.stat1, current_labels)
        elif "silhouette" in conditional_questioning:
            current_score = sklearn.metrics.silhouette_score(hac_vec_per_seg.stat1, current_labels)
        elif "davies_bouldin" in conditional_questioning:
            current_score = sklearn.metrics.davies_bouldin_score(hac_vec_per_seg.stat1, current_labels)
        else:
            if verbos:
                print(f"{conditional_questioning} is not valid -> True")
            return True

        if question_type == "separation":

            link_tmp = copy.deepcopy(temporary_link_list)

            ii = 0
            for ii, fl in enumerate(link_tmp):
                if numpy.array_equal(fl, node[:4]):
                    _ = link_tmp.pop(ii)
                    break
            link_tmp = correct_link_after_removing_node(len(bottomline_cluster_list), ii, link_tmp, 1)
            diar_tmp = copy.deepcopy(init_diar)
            new_diar = apply_link_on_diar(diar_tmp, bottomline_cluster_list, link_tmp)

            if len(new_diar.unique("cluster")) < 2:
                if verbos:
                    print(f"{conditional_questioning} is not possible to be calculated for one cluster (after separation) -> True")
                return True

            changed_labels = []
            for seg in new_diar:
                changed_labels.append(seg['cluster'])

            if "calinski_harabasz" in conditional_questioning:
                changed_score = sklearn.metrics.calinski_harabasz_score(hac_vec_per_seg.stat1, changed_labels)
            elif "silhouette" in conditional_questioning:
                changed_score = sklearn.metrics.silhouette_score(hac_vec_per_seg.stat1, changed_labels)
            elif "davies_bouldin" in conditional_questioning:
                changed_score = sklearn.metrics.davies_bouldin_score(hac_vec_per_seg.stat1, changed_labels)
            else:
                if verbos:
                    print(f"{conditional_questioning} is not valid -> True")
                return True

        elif question_type == "clustering":

            link_tmp = copy.deepcopy(temporary_link_list)

            link_tmp.append(node[:4])
            diar_tmp = copy.deepcopy(init_diar)
            new_diar = apply_link_on_diar(diar_tmp, bottomline_cluster_list, link_tmp)

            if len(new_diar.unique("cluster")) < 2:
                if verbos:
                    print(f"{conditional_questioning} is not possible to be calculated for one cluster (after clustering) -> True")
                return True

            changed_labels = []
            for seg in new_diar:
                changed_labels.append(seg['cluster'])

            if "calinski_harabasz" in conditional_questioning:
                changed_score = sklearn.metrics.calinski_harabasz_score(hac_vec_per_seg.stat1, changed_labels)
            elif "silhouette" in conditional_questioning:
                changed_score = sklearn.metrics.silhouette_score(hac_vec_per_seg.stat1, changed_labels)
            elif "davies_bouldin" in conditional_questioning:
                changed_score = sklearn.metrics.davies_bouldin_score(hac_vec_per_seg.stat1, changed_labels)
            else:
                if verbos:
                    print(f"{conditional_questioning} is not valid -> True")
                return True
#             changed_score = sklearn.metrics.calinski_harabasz_score(hac_vec_per_seg.stat1, changed_labels)
         
        else:
            if verbos:
                print(f"Invalid question_type ({question_type}) shoud be separation or clustering"
                  f"-> ignore conditional questioning ")
            return True

        # NEVER USE A VARIABLE WITH THE SAME NAME AS THE METHOD
        if 'invs' in conditional_questioning:
            q_quality = current_score < changed_score
        else:
            q_quality = current_score > changed_score
        if verbos:
            print(f"{question_type}: current_score({current_score}) < changed_score({changed_score}) -> {q_quality}")
    else:
        q_quality = True

    return q_quality


def get_node_speakers(node_spk, number_cluster, link):
    """
    Get a node and return the all sub cluster id

    :param node_spk: row of the linkage matrix
    :param number_cluster: number in link matrix
    :param link: linkage matrix
    :return: cluster_list: a list of clusters id in link
    """

    if node_spk >= number_cluster:
        cluster_list = get_node_speakers(link[int(node_spk - number_cluster)][0],
                                         number_cluster,
                                         link) + get_node_speakers(link[int(node_spk - number_cluster)][1],
                                                                   number_cluster,
                                                                   link)
    else:
        cluster_list = [int(node_spk)]

    return cluster_list


def get_roots_nodes(node, number_cluster, link):
    """
    Get a node and return the all upper cluster id

    :param node:
    :param number_cluster: number in link matrix
    :param link: linkage matrix
    :return: cluster_list: a list of clusters id which may not be in link
    """
    ii = 0
    while not numpy.array_equal(link[ii], node):
        ii += 1
    node_idx_list = [ii + number_cluster]

    for ii, fl in enumerate(link):
        if fl[0] in node_idx_list or fl[1] in node_idx_list:
            node_idx_list.append(ii + number_cluster)

    return node_idx_list


def sort_node_sides_ccs(current_diar,
                        first_spk,
                        second_spk,
                        scores_per_segment,
                        candidate_pair_number=None):
    """
    Provide two lists of segments by which has maximum plda similarity scores to cluster's center

    :param current_diar:
    :param first_spk:
    :param second_spk:
    :param scores_per_segment:
    :param candidate_pair_number:
    :return:
    """
    # finding the index of segment in current_diar for investigation in scores_per_segment
    segs_indx_cluster1 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in first_spk:
            segs_indx_cluster1.append(i)
    segs_indx_cluster2 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in second_spk:
            segs_indx_cluster2.append(i)

    similarity_scoremat = copy.deepcopy(scores_per_segment.scoremat)

    # calculate the sum of similarity to cluster's segments
    cluster1_similarity_sum = {}
    for i in range(len(segs_indx_cluster1)):
        for j in range(len(scores_per_segment.scoremat[i])):
            if j not in cluster1_similarity_sum:
                cluster1_similarity_sum[j] = 0
            if j in segs_indx_cluster1 and j != i:
                cluster1_similarity_sum[j] += scores_per_segment.scoremat[i][j]
    cluster2_similarity_sum = {}
    for i in range(len(segs_indx_cluster2)):
        for j in range(len(scores_per_segment.scoremat[i])):
            if j not in cluster2_similarity_sum:
                cluster2_similarity_sum[j] = 0
            if j in segs_indx_cluster2 and j != i:
                cluster2_similarity_sum[j] += scores_per_segment.scoremat[i][j]

    # creat a list of combination pair and their correspond additional similarity from cluster center as score
    list_pair = []
    list_pair_scores = []
    for s1 in cluster1_similarity_sum:
        for s2 in cluster2_similarity_sum:
            list_pair.append([s1, s2])
            list_pair_scores.append(cluster1_similarity_sum[s1] + cluster2_similarity_sum[s2])

    # sort the list_pair based on list_pair_scores
    _, list_pair_sorted = (list(t) for t in zip(*sorted(zip(list_pair_scores,
                                                            list_pair))))
    # we are looking for maximum the similarity score
    list_pair_sorted.reverse()

    first_seg_list_sorted = []
    second_seg_list_sorted = []
    for p in list_pair_sorted:
        first_seg_list_sorted.append(current_diar[p[0]])
        second_seg_list_sorted.append(current_diar[p[1]])

    if candidate_pair_number is None:
        return first_seg_list_sorted, second_seg_list_sorted
    else:
        return first_seg_list_sorted[:candidate_pair_number], second_seg_list_sorted[:candidate_pair_number]


def sort_node_sides_cc(current_diar,
                       first_spk,
                       second_spk,
                       current_vec,
                       candidate_pair_number=None):
    """
    Provide two lists of segments by which has minimum sum of distances from cluster centers

    :param current_diar:
    :param first_spk:
    :param second_spk:
    :param current_vec:
    :param candidate_pair_number:
    :return:
    """
    # finding the index and correspond vectore of segment in current_diar for each cluster
    segs_indx2vec_cluster1 = {}
    for i in range(len(current_diar)):
        if current_diar[i][1] in first_spk:
            segs_indx2vec_cluster1[i] = current_vec.stat1[i]
    segs_indx2vec_cluster2 = {}
    for i in range(len(current_diar)):
        if current_diar[i][1] in second_spk:
            segs_indx2vec_cluster2[i] = current_vec.stat1[i]

    # calculate cluster center of each cluster
    cluster1_center = numpy.mean(list(segs_indx2vec_cluster1.values()), axis=0)
    cluster2_center = numpy.mean(list(segs_indx2vec_cluster2.values()), axis=0)

    # calculate the distance between each segment from cluster center
    segs_indx2distance_cc_cluster1 = {}
    for s in segs_indx2vec_cluster1:
        segs_indx2distance_cc_cluster1[s] = scipy.spatial.distance.euclidean(segs_indx2vec_cluster1[s],
                                                                             cluster1_center)
    segs_indx2distance_cc_cluster2 = {}
    for s in segs_indx2vec_cluster2:
        segs_indx2distance_cc_cluster2[s] = scipy.spatial.distance.euclidean(segs_indx2vec_cluster2[s],
                                                                             cluster2_center)

    # creat a list of combination pair and their correspond additional distance from cluster center as score
    list_pair = []
    list_pair_scores = []
    for s1 in segs_indx2distance_cc_cluster1:
        for s2 in segs_indx2distance_cc_cluster2:
            list_pair.append([s1, s2])
            list_pair_scores.append(segs_indx2distance_cc_cluster1[s1] + segs_indx2distance_cc_cluster2[s2])

    # sort the list_pair based on list_pair_scores
    _, list_pair_sorted = (list(t) for t in zip(*sorted(zip(list_pair_scores,
                                                            list_pair))))

    first_seg_list_sorted = []
    second_seg_list_sorted = []
    for p in list_pair_sorted:
        first_seg_list_sorted.append(current_diar[p[0]])
        second_seg_list_sorted.append(current_diar[p[1]])

    if candidate_pair_number is None:
        return first_seg_list_sorted, second_seg_list_sorted
    else:
        return first_seg_list_sorted[:candidate_pair_number], second_seg_list_sorted[:candidate_pair_number]


def sort_node_sides_min(current_diar,
                        first_spk,
                        second_spk,
                        scores_per_segment,
                        candidate_pair_number=None):
    """
    Provide two lists of segments by which has minimum distance in scores_per_segment

    :param current_diar:
    :param first_spk:
    :param second_spk:
    :param scores_per_segment:
    :param candidate_pair_number:
    :return:
    """

    # finding the index of segment in current_diar for investigation in scores_per_segment
    segs_indx_cluster1 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in first_spk:
            segs_indx_cluster1.append(i)
    segs_indx_cluster2 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in second_spk:
            segs_indx_cluster2.append(i)

    similarity_scoremat = copy.deepcopy(scores_per_segment.scoremat)

    first_seg_list_sorted = []
    second_seg_list_sorted = []

    # finding the max length of first_seg_list_sorted and second_seg_list_sorted
    if candidate_pair_number is None:
        _seg_list_sorted_len = len(segs_indx_cluster1) * len(segs_indx_cluster2)
    else:
        _seg_list_sorted_len = min(len(segs_indx_cluster1) * len(segs_indx_cluster2), candidate_pair_number)

    while (len(first_seg_list_sorted) < _seg_list_sorted_len and
           numpy.any((similarity_scoremat != -float('inf')))):

        # finding the index of two segments with minimum distance or maximum similarity
        first_seg_idx, second_seg_idx = numpy.unravel_index(similarity_scoremat.argmax(),
                                                            similarity_scoremat.shape)
        if first_seg_idx in segs_indx_cluster1 and second_seg_idx in segs_indx_cluster2:
            first_seg_list_sorted.append(current_diar[first_seg_idx])
            second_seg_list_sorted.append(current_diar[second_seg_idx])
        similarity_scoremat[first_seg_idx, second_seg_idx] = -float('inf')

    return first_seg_list_sorted, second_seg_list_sorted


def sort_node_sides_max(current_diar,
                        first_spk,
                        second_spk,
                        scores_per_segment,
                        candidate_pair_number=None):
    """
    Provide two lists of segments by which has maximum distance in scores_per_segment

    :param current_diar:
    :param first_spk:
    :param second_spk:
    :param scores_per_segment:
    :param candidate_pair_number:
    :return:
    """
    # finding the index of segment in current_diar for investigation in scores_per_segment
    segs_indx_cluster1 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in first_spk:
            segs_indx_cluster1.append(i)
    segs_indx_cluster2 = []
    for i in range(len(current_diar)):
        if current_diar[i][1] in second_spk:
            segs_indx_cluster2.append(i)

    similarity_scoremat = copy.deepcopy(scores_per_segment.scoremat)

    first_seg_list_sorted = []
    second_seg_list_sorted = []

    # finding the max length of first_seg_list_sorted and second_seg_list_sorted
    if candidate_pair_number is None:
        _seg_list_sorted_len = len(segs_indx_cluster1) * len(segs_indx_cluster2)
    else:
        _seg_list_sorted_len = min(len(segs_indx_cluster1) * len(segs_indx_cluster2), candidate_pair_number)

    while (len(first_seg_list_sorted) < _seg_list_sorted_len and
           numpy.any((similarity_scoremat != float('inf')))):

        # finding the index of two segments with maximum distance or minimum similarity
        first_seg_idx, second_seg_idx = numpy.unravel_index(similarity_scoremat.argmin(),
                                                            similarity_scoremat.shape)
        if first_seg_idx in segs_indx_cluster1 and second_seg_idx in segs_indx_cluster2:
            first_seg_list_sorted.append(current_diar[first_seg_idx])
            second_seg_list_sorted.append(current_diar[second_seg_idx])
        similarity_scoremat[first_seg_idx, second_seg_idx] = float('inf')

    return first_seg_list_sorted, second_seg_list_sorted


def sort_node_sides_random(first_seg_list,
                           second_seg_list,
                           candidate_pair_number=None):
    """
    Shuffle the two lists

    :param first_seg_list:
    :param second_seg_list:
    :param candidate_pair_number: number of condidate pair as a list. None for maximum length
    :return:
    """
    first_seg_list_ = copy.deepcopy(first_seg_list)
    second_seg_list_ = copy.deepcopy(second_seg_list)

    tmp_list = []
    for seg1 in first_seg_list_:
        for seg2 in second_seg_list_:
            tmp_list.append([seg1, seg2])
    random.shuffle(tmp_list)
    first_seg_list_sorted = []
    second_seg_list_sorted = []
    for seg_pair in tmp_list:
        first_seg_list_sorted.append(seg_pair[0])
        second_seg_list_sorted.append(seg_pair[1])

    if candidate_pair_number is None:
        return first_seg_list_sorted, second_seg_list_sorted
    else:
        return first_seg_list_sorted[:candidate_pair_number], second_seg_list_sorted[:candidate_pair_number]


def sort_node_sides_longest(first_seg_list,
                            second_seg_list,
                            candidate_pair_number=None):
    """
    Sort each list of segments by descending duration

    :param first_seg_list:
    :param second_seg_list:
    :param candidate_pair_number: number of condidate pair as a list. None for maximum length
    :return:
    """
    # For each segment list, sort according to the length of the segments
    first_seg_list_sorted = []
    second_seg_list_sorted = []

    first_duration = numpy.zeros(len(first_seg_list))
    for idx, seg in enumerate(first_seg_list):
        first_duration[idx] = seg["stop"] - seg["start"]

    first_indices = numpy.argsort(first_duration)
    for ii in first_indices[::-1]:
        first_seg_list_sorted.append(first_seg_list[ii])

    second_duration = numpy.zeros(len(second_seg_list))
    for idx, seg in enumerate(second_seg_list):
        second_duration[idx] = seg["stop"] - seg["start"]

    second_indices = numpy.argsort(second_duration)
    for ii in second_indices[::-1]:
        second_seg_list_sorted.append(second_seg_list[ii])

    if candidate_pair_number is None:
        return first_seg_list_sorted, second_seg_list_sorted
    else:
        return first_seg_list_sorted[:candidate_pair_number], second_seg_list_sorted[:candidate_pair_number]


def sort_node_sides(first_seg_list,
                    second_seg_list,
                    first_spk,
                    second_spk,
                    scores_per_segment,
                    current_diar,
                    current_vec,
                    selection_criteria,
                    candidate_pair_number=None):
    """
    Sort both lists according to the chosen criteria
    return two lists but sorted according to the chosen criteria

    :param first_seg_list:
    :param second_seg_list:
    :param first_spk:
    :param second_spk:
    :param scores_per_segment:
    :param current_diar:
    :param current_vec:
    :param selection_criteria: longest, cluster_center, cluster_center_plda, random, max_noBICHAC
    max, min, ideal
    :param candidate_pair_number:
    :return:
    """


    if selection_criteria == "longest":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_longest(first_seg_list,
                                                                                second_seg_list,
                                                                                candidate_pair_number)

    elif selection_criteria == "cluster_center":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_cc(current_diar,
                                                                           first_spk,
                                                                           second_spk,
                                                                           current_vec,
                                                                           candidate_pair_number)

    elif selection_criteria == "cluster_center_score":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_ccs(current_diar,
                                                                            first_spk,
                                                                            second_spk,
                                                                            scores_per_segment,
                                                                            candidate_pair_number)

    elif selection_criteria == "max_noBICHAC":
        # first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_max_NBH(first_seg_list,
        #                                                                        second_seg_list,
        #                                                                        scores_per_cluster,
        #                                                                        current_diar,
        #                                                                        current_vec,
        #                                                                        selection_criteria)
        print("Not implemented yet")
        pass

    elif selection_criteria == "max":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_max(current_diar,
                                                                            first_spk,
                                                                            second_spk,
                                                                            scores_per_segment,
                                                                            candidate_pair_number)

    elif selection_criteria == "min":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_min(current_diar,
                                                                            first_spk,
                                                                            second_spk,
                                                                            scores_per_segment,
                                                                            candidate_pair_number)

    elif selection_criteria == "random":
        first_seg_list_sorted, second_seg_list_sorted = sort_node_sides_random(first_seg_list,
                                                                               second_seg_list,
                                                                               candidate_pair_number=None)

    return first_seg_list_sorted, second_seg_list_sorted


def get_segment_sorted_list(node_to_check,
                            linkage_matrix,
                            bottomline_cluster_list,
                            scores_per_segment,
                            current_diar,
                            current_vec,
                            selection_criteria="longest"):
    """

    :param node_to_check:
    :param linkage_matrix:
    :param bottomline_cluster_list:
    :param scores_per_segment:
    :param current_diar:
    :param current_vec:
    :param user:
    :param file_info:
    :param selection_criteria:
    :return:
    """
    # Get the list of speakers for each side of the node
    first_clusters = get_node_speakers(node_to_check[0], len(bottomline_cluster_list), linkage_matrix)
    first_spk = [bottomline_cluster_list[n] for n in first_clusters]

    second_clusters = get_node_speakers(node_to_check[1], len(bottomline_cluster_list), linkage_matrix)
    second_spk = [bottomline_cluster_list[n] for n in second_clusters]

    # Get the list of segments corresponding to each speaker
    first_seg_list = [seg for seg in current_diar.segments if seg["cluster"] in first_spk]
    second_seg_list = [seg for seg in current_diar.segments if seg["cluster"] in second_spk]

    # Sort the two lists of segments according to the chosen criteria
    first_seg_list_sorted, second_seg_list_sorted = sort_node_sides(first_seg_list,
                                                                    second_seg_list,
                                                                    first_spk,
                                                                    second_spk,
                                                                    scores_per_segment,
                                                                    current_diar,
                                                                    current_vec,
                                                                    selection_criteria)

    return first_seg_list_sorted, second_seg_list_sorted


def ask_question_al(node_to_check,
                    linkage_matrix,
                    bottomline_cluster_list,
                    scores_per_segment,
                    init_diar,
                    current_vec,
                    user,
                    file_info,
                    uem,
                    selection_criteria="longest"):
    """

    :param init_diar:
    :param uem:
    :param scores_per_segment:
    :param linkage_matrix:
    :param node_to_check:
    :param bottomline_cluster_list:
    :param current_vec:
    :param user:
    :param file_info:
    :param selection_criteria:
    :return:
    """
    first_seg_list_sorted, second_seg_list_sorted = get_segment_sorted_list(node_to_check,
                                                                            linkage_matrix,
                                                                            bottomline_cluster_list,
                                                                            scores_per_segment,
                                                                            init_diar,
                                                                            current_vec,
                                                                            selection_criteria)

    # TODO: The segment should be selected from list or can be provided by expert
    # For now it will select the head of list

    # Taking into account UEM files in order to ask question in UEM area
    # /!\ considering each seg_list separately. /!\
    idx = 0
    seg_not_exist = True
    while seg_not_exist and idx != len(first_seg_list_sorted):
        selected_seg_first = first_seg_list_sorted[idx]
        for u in range(len(uem.start_time)):
            if int(uem.start_time[u] * 100) < selected_seg_first["start"] < int(uem.end_time[u] * 100) \
                    or int(uem.start_time[u] * 100) < selected_seg_first["stop"] < int(uem.end_time[u] * 100):
                seg_not_exist = False
        idx += 1

    if idx > len(first_seg_list_sorted):
        print(f"Investigate cluster ({first_seg_list_sorted[0]['cluster']}) "
              f"that does not contain segment in UEM area.")
        return False, "None", True

    idx = 0
    seg_not_exist = True
    while seg_not_exist and idx != len(second_seg_list_sorted):
        selected_seg_second = second_seg_list_sorted[idx]
        for u in range(len(uem.start_time)):
            if (int(uem.start_time[u] * 100) < selected_seg_second["start"] < int(
                    uem.end_time[u] * 100) or
                    selected_seg_second["stop"] > int(uem.start_time[u] * 100) and selected_seg_second[
                        "stop"] < int(uem.end_time[u] * 100)):
                seg_not_exist = False
        idx += 1

    if idx > len(second_seg_list_sorted):
        print(
            f"Investigate cluster ({second_seg_list_sorted[0]['cluster']}) that does not contain segment in UEM area.")
        return False, "None", True

    # change below answer, in order to deal with non perfect segmentation
    t1 = [selected_seg_first["start"] / 100., selected_seg_first["stop"] / 100.]
    t2 = [selected_seg_second["start"] / 100., selected_seg_second["stop"] / 100.]
    # For first segments of each side, get the center of the segment in seconds
    #         t1 = (selected_seg_first["start"] + selected_seg_first["stop"]) / 200.
    #         t2 = (selected_seg_second["start"] + selected_seg_second["stop"]) / 200.

    # Ask the question to the user
    message_to_user = MessageToUser(file_info,
                                    s4d_to_allies(init_diar),
                                    Request('same', t1, t2))

    hal, answer = user.validate(message_to_user)

    # Return the answer from the user
    return answer.answer, answer.name, hal


def apply_ideal_correction(bottomline_diar, ref, uem, der_track_show):
    """

    :param bottomline_diar:
    :param ref:
    :param uem:
    :param der_track_show:
    :return:
    """
    hyp = s4d_to_allies(copy.deepcopy(bottomline_diar))
    der, fa_rate, miss_rate, conf_rate, error, time, newspkmap = compute_der([ref], [hyp], [uem], collar = 0.250)
    #     der, fa_rate, miss_rate, conf_rate, time, newspkmap = compute_der(ref, hyp, uem, {}, 0.250)
    der_track_cs = {"time": time, "der_log": [der], "correction": ["initial"]}

    removelist = []
    first_pass_diar = copy.deepcopy(bottomline_diar)
    for s in range(len(first_pass_diar)):
        best_match_spk = None
        best_match_len = 0
        for i in range(len(ref.start_time)):
            intersec_dur = min(first_pass_diar[s]["stop"] / 100.,
                               ref.end_time[i]) - max(first_pass_diar[s]["start"] / 100.,
                                                      ref.start_time[i])
            if intersec_dur > best_match_len:
                best_match_len = intersec_dur
                best_match_spk = ref.speaker[i]
        if best_match_spk is not None:
            first_pass_diar[s]["cluster"] = best_match_spk
        else:
            removelist.append(s)

    new_diar = copy.deepcopy(first_pass_diar)
    hyp = s4d_to_allies(new_diar)
    der, fa_rate, miss_rate, conf_rate, error, time, newspkmap = compute_der([ref], [hyp], [uem], collar = 0.250)
#     der, fa_rate, miss_rate, conf_rate, time, newspkmap = compute_der(ref, hyp, uem, {}, 0.250)
    der_track_cs["der_log"].append(der)
    der_track_cs["correction"].append("ideal")
    der_track_show['ideal'] = der_track_cs

    return new_diar, der_track_show


def run_active_learning_tree(link,
                             init_diar,
                             hac_iv_vec_per_seg,
                             th,
                             bottomline_cluster_list,
                             hac_iv_vec,
                             user,
                             file_info,
                             uem,
                             ref,
                             selection_method="longest",
                             conditional_questioning=None,  # "calinski_harabasz","std"
                             confirm2stop=float('inf')):
    """
     Active correction between until a bottomline_clustering and full dendrogram
    :param bottomline_cluster_list:
    :param link: full linkage matrix for creating dendrogram
    :param init_diar: A diar object correspond to bottomline clustering
    :param hac_iv_vec_per_seg: StatServer of segments' vector match with init_diar segment
    :param th: The threshold of distance for HAC clustering in link
    :param hac_iv_vec: StatServer of cluster' vector match with init_diar cluster
    :param user: separation or clustering
    :param file_info,
    :param uem,
    :param ref
    :param selection_method: selection method of segments in cluster for question generation
    (longest segment is implemented)
    :param conditional_questioning: [None or "calinski_harabasz" or "std"] in order to estimate the correction or
    confirmation answer and increase questioning performance
    :param confirm2stop : An integer number (or 'ideal') that show after how many confirmation
    (in each sepereation and clustering direction) the question generation should be stop
    :return: False,the last diarziation result after interaction, a dictionary of DER as log of process
    """
    number_cluster = len(bottomline_cluster_list)

    tmp = numpy.zeros((link.shape[0], link.shape[1] + 2))
    tmp[:, :-2] = link
    tmp[:, -2] = link[:, 2] - th
    tmp[:, -1] = numpy.abs(link[:, 2] - th)
    links_to_check = tmp[numpy.argsort(tmp[:, -1])]
    # This corresponds to the links that must be done if not using any human assistance
    temporary_link_list = []
    for _l in link:
        if _l[2] <= th:
            temporary_link_list.append(_l)

    # Check all nodes from the tree
    no_more_clustering = False
    no_more_separation = False
    clustering_confirm = 0
    separation_confirm = 0

    # a list of nodes that have separated to avoid any conflict with clustering
    # it will be used in case of prioritize_separation2clustering
    stop_separation_list = []  # a list of nodes that have gotten confirmation for separation question
    stop_clustering_list = []  # a list of nodes that have gotten confirmation for clustering question

    der, new_diar = check_der(init_diar, bottomline_cluster_list, temporary_link_list, ref, uem)
    #print("Initial DER based on bottomline_diar and linkage : ", der)

    der_track_show = {"der_log": [der], "correction": ["initial"]}

    for node in links_to_check:

        # In case we stop exploring the tree
        if no_more_clustering and no_more_separation:
            break

        subnodes_list1 = get_node_speakers(node[0], number_cluster, link)
        subnodes_list2 = get_node_speakers(node[1], number_cluster, link)

        # Check node below the threshold
        if node[-2] <= 0:

            subnodes_list = subnodes_list1 + subnodes_list2
            node_in_stop_separation_list = False
            for n_idx in subnodes_list:
                if n_idx in stop_separation_list:
                    node_in_stop_separation_list = True

            if node_in_stop_separation_list:
                pass
            # If we already decided not tyo explore down the tree
            elif no_more_separation:
                pass

            elif conditional_questioning and not question_quality(node,
                                                                  subnodes_list1,
                                                                  subnodes_list2,
                                                                  bottomline_cluster_list,
                                                                  hac_iv_vec_per_seg,
                                                                  copy.deepcopy(init_diar),
                                                                  temporary_link_list,
                                                                  conditional_questioning,
                                                                  question_type="separation"):
                pass
#                 stop_separation_list += subnodes_list
#                 print(f"Conditional questioning ({conditional_questioning}) does not advice separation")

            # otherwise as question to the human about this node
            else:
                # Ask the human
                is_same_speaker, investigated_spk, _ = ask_question_al(node_to_check=node,
                                                                       linkage_matrix=link,
                                                                       bottomline_cluster_list=bottomline_cluster_list,
                                                                       scores_per_segment=None,
                                                                       init_diar=init_diar,
                                                                       current_vec=hac_iv_vec_per_seg,
                                                                       user=user,
                                                                       file_info=file_info,
                                                                       uem=uem,
                                                                       selection_criteria=selection_method)

                # if the question was related to times that corespond to speakers
                if investigated_spk != "None":
                    # if the human validate the node (it has been grouped and it must be)
                    if is_same_speaker:

                        # confirmation in split question > update in split Blacklist (stop_separation_list)
                        stop_separation_list += subnodes_list

                        link_tmp = copy.deepcopy(temporary_link_list)
                        diar_tmp = copy.deepcopy(init_diar)
                        der, new_diar = check_der(diar_tmp, bottomline_cluster_list, link_tmp, ref, uem)
                        #print(f"not_separation:", der)
                        der_track_show["der_log"].append(der)
                        der_track_show["correction"].append("not_separation")
                        separation_confirm += 1
                        if separation_confirm == confirm2stop:
                            no_more_separation = True

                    # if the human decide to separate the node
                    else:
                        # correction in split question > update in merge Blacklist  (stop_clustering_list)
                        stop_clustering_list += get_roots_nodes(node[:4], number_cluster, link)

                        for ii, fl in enumerate(temporary_link_list):
                            if numpy.array_equal(fl, node[:4]):
                                _ = temporary_link_list.pop(ii)
                                break
                        temporary_link_list = correct_link_after_removing_node(number_cluster, ii, temporary_link_list,
                                                                               1)

                        # Record the correction and the DER
                        link_tmp = copy.deepcopy(temporary_link_list)
                        diar_tmp = copy.deepcopy(init_diar)
                        der, new_diar = check_der(diar_tmp, bottomline_cluster_list, link_tmp, ref, uem)
                        print(f"separation:", der)
                        der_track_show["der_log"].append(der)
                        der_track_show["correction"].append("separation")

        # Check node above the threshold
        elif node[-2] > 0:

            if node[0] in stop_clustering_list or node[1] in stop_clustering_list:
                pass
            # If we already decided not tyo explore up the tree
            elif no_more_clustering:
                pass

            elif conditional_questioning and not question_quality(node,
                                                                  subnodes_list1,
                                                                  subnodes_list2,
                                                                  bottomline_cluster_list,
                                                                  hac_iv_vec_per_seg,
                                                                  copy.deepcopy(init_diar),
                                                                  temporary_link_list,
                                                                  conditional_questioning,
                                                                  question_type="clustering"):

#                 stop_clustering_list += get_roots_nodes(node[:4], number_cluster, link)
                pass
#                 print(f"Conditional questioning ({conditional_questioning}) does not advice clustering")

                # otherwise as question to the human about this node
            else:

                # Ask the human
                is_same_speaker, investigated_spk, _ = ask_question_al(node,
                                                                       link,
                                                                       bottomline_cluster_list,  # scores_per_cluster,
                                                                       None,  # scores_per_segment,
                                                                       init_diar,
                                                                       hac_iv_vec_per_seg,
                                                                       user,
                                                                       file_info,
                                                                       uem,
                                                                       selection_criteria=selection_method)

                # if the question was related to times that corespond to speakers
                if investigated_spk != "None":
                    # if the human validate the node (it has not been grouped and it must be)
                    if is_same_speaker:

                        # correction in merge question > update in split Blacklist (stop_separation_list)
                        stop_separation_list += subnodes_list1 + subnodes_list2

                        temporary_link_list.append(node[:4])
                        # Record the correction and the DER
                        link_tmp = copy.deepcopy(temporary_link_list)
                        diar_tmp = copy.deepcopy(init_diar)
                        der, new_diar = check_der(diar_tmp, bottomline_cluster_list, link_tmp, ref, uem)
                        print("clustering :", der)
                        der_track_show["der_log"].append(der)
                        der_track_show["correction"].append("clustering")

                    # Else stop exploring the tree upward
                    else:

                        # confirmation in merge question > update in merge Blacklist (stop_clustering_list)
                        stop_clustering_list += get_roots_nodes(node[:4], number_cluster, link)

                        if set(range(len(bottomline_cluster_list))).issubset(set(stop_clustering_list)):
                            no_more_clustering = True
                        link_tmp = copy.deepcopy(temporary_link_list)
                        diar_tmp = copy.deepcopy(init_diar)
                        der, new_diar = check_der(diar_tmp, bottomline_cluster_list, link_tmp, ref, uem)
                        #print("not_clustering :", der)
                        der_track_show["der_log"].append(der)
                        der_track_show["correction"].append("not_clustering")
                        clustering_confirm += 1
                        if clustering_confirm == confirm2stop:
                            no_more_clustering = True

    return False, new_diar, der_track_show


def allies_within_show_hal(model_cfg,
                           model,
                           data_folder,
                           show,
                           init_diar,
                           vec_per_cluster,
                           vec_per_seg,
                           file_info,
                           uem,
                           ref,
                           user,
                           c2s=float('inf')):

    """
    :param data_folder:
    :param model_cfg:
    :param model:
    :param show:
    :param dir_output_system:
    :param init_diar:
    :param vec_per_cluster:
    :param vec_per_seg:
    :param tmp_path:
    :param file_info:
    :param uem:
    :param ref:
    :param user:
    :param c2s:
    :param conditional_clustering: 'calinski_harabasz',
                                        'silhouette',
                                        'davies_bouldin',
                                        'calinski_harabasz_invs',
                                        'silhouette_invs',
                                        'davies_bouldin_invs'
    :return: new diarization object
    """
    der_track_show = {}

    hal_dir = f"{model_cfg['tmp_dir']}/seg/first_th{model_cfg['first_seg']['thr_h']}" \
              f"/second_th{model_cfg['within_show']['th_w']}/hal/"

    if not os.path.isdir(hal_dir):
        os.makedirs(hal_dir)

    #####################################################################################################
    # Creat dendrogram by using upper level of current clustering and segments in each cluster######
    #####################################################################################################
    if len(init_diar.unique("cluster")) < 2:
        link_clusters = numpy.array([])
    else:
        scores_clusters, link_clusters, th_clusters = vec2link(model_cfg, vec_per_cluster, init_diar, model)


    backup_vad_type = model_cfg["model"]["vad"]["type"]
    backup_thr_h = model_cfg['first_seg']['thr_h']
    model_cfg["model"]["vad"]["type"] = "reference"
    model_cfg['first_seg']['thr_h']=model_cfg['within_show']['thr_h']


    bottomline_diar, link_within_clusters_dic, vec_within_clusters_dic = create_bottomline_clustering(model,
                                                                                                      model_cfg,
                                                                                                      show,
                                                                                                      init_diar,
                                                                                                      data_folder)
    model_cfg["model"]["vad"]["type"] = backup_vad_type
    model_cfg['first_seg']['thr_h'] = backup_thr_h

    bottomline_cluster_list = bottomline_diar.unique('cluster')

    #######################################################################
    #       add sub cluster linkage for splitting Q in full link          #
    bottom_linkage = create_bottom_linkage(link_within_clusters_dic, bottomline_cluster_list, vec_within_clusters_dic)

    ########################################################################################
    #       check does bottomline_diar plus sub cluster linkage make current_diar          #
    hyp = s4d_to_allies(init_diar)
    der_init, fa_rate, miss_rate, conf_rate, error, time, newspkmap = compute_der([ref], [hyp], [uem], collar = 0.250)
    #print("DER of init_diar: ", der_init)

    #print("Current DER (original) : ", der_init)


    hyp = s4d_to_allies(bottomline_diar)
    der, fa_rate, miss_rate, conf_rate, error, time, newspkmap = compute_der([ref], [hyp], [uem], collar = 0.250)
    #print("DER of bottomline_diar: ", der)
    
#     import pdb
#     pdb.set_trace()

    vec_per_seg.modelset = vec_per_seg.modelset.astype(object)
    for idx in range(len(bottomline_diar)):
        vec_per_seg.modelset[idx] = bottomline_diar[idx]['cluster']

    if c2s != 'ideal':

        #######################################################################
        #          add upper linkage for merging Q in full link               #
        bottom_linkage_tmp = copy.deepcopy(bottom_linkage)
        link_clusters_tmp = copy.deepcopy(link_clusters)
        bottomline_cluster_list_tmp = copy.deepcopy(bottomline_cluster_list)

        if len(init_diar.unique("cluster")) < 2:
            full_link_tmp = bottom_linkage_tmp
            if len(bottom_linkage) > 1:
                th_clustering = bottom_linkage[-1][2]
            else:
                th_clustering = 0
        else:
            th_clustering, full_link_tmp = combine_upper_and_bottom_linkage(bottom_linkage_tmp,
                                                                            link_clusters_tmp,
                                                                            bottomline_cluster_list_tmp,
                                                                            vec_per_cluster)

        #######################################################################
        #              Run HAL on top of current diarization                  #
        if len(full_link_tmp) < 1:

            der_track_cs = {"time": time, "der_log": [der_init], "correction": ["initial"]}
            new_diar=init_diar
        else:
            _, new_diar,der_track_cs = run_active_learning_tree(copy.deepcopy(numpy.array(full_link_tmp)),
                                                                copy.deepcopy(bottomline_diar),
                                                                copy.deepcopy(vec_per_seg),
                                                                th_clustering,
                                                                bottomline_cluster_list_tmp,
                                                                copy.deepcopy(vec_per_cluster),
                                                                copy.deepcopy(user),
                                                                file_info,
                                                                uem,
                                                                ref,
                                                                "longest",
                                                                model_cfg['within_show']['conditional_questioning'],
                                                                float(c2s))

            der_track_cs["time"] = time

        der_track_show[f"{str(c2s)}_{model_cfg['within_show']['conditional_questioning']}"] = der_track_cs

        #prefix = f"{dir_output_system}/HAL_c2s_{c2s}_th_h_{model_cfg['within_show']['hal_seg']}"
        #if model_cfg['within_show']['conditional_questioning']:
        #    hal_path = f"{prefix}_{model_cfg['within_show']['conditional_questioning']}/"
        #else:
        #    hal_path = f"{prefix}/"

    else:
        # ideal correction
        new_diar, der_track_show = apply_ideal_correction(bottomline_diar, ref, uem, der_track_show)
        #hal_path = f"{dir_output_system}/simulate_bestHAL/"

    if not os.path.isdir(hal_dir):
        os.makedirs(hal_dir)

    allies_write_diar(new_diar, f"{hal_dir}/{show}.mdtm")

    return new_diar


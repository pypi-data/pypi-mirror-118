
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
Copyright 2020-2021 Anthony Larcher & Olivier Galibert

    :mod:`user_simulation`

"""
import numpy as np
import s4d

from scipy.optimize import linear_sum_assignment

class UserSimulation:

    def __init__(self, parameters):
        self.cost = 0
        self.hyp_to_ref_name_map = {}
        self.ref_to_hyp_name_map = {}
        self.max_cost_per_file = parameters["max_cost_per_file"]
        self.request_collar_cost = parameters["request_collar_cost"]
        self.minimal_validation_time = parameters['minimal_validation_time']
        self.minimal_validation_purity = parameters['minimal_validation_purity']
        self.q_boundaries = parameters['question_allow_boundaries'] if 'question_allow_boundaries' in parameters else True
        self.q_same_intra_show = parameters['question_allow_same_intra_show'] if 'question_allow_same_intra_show' in parameters else True
        self.q_different_intra_show = parameters['question_allow_different_intra_show'] if 'question_allow_different_intra_show' in parameters else True
        self.q_same_inter_show = parameters['question_allow_same_inter_show'] if 'question_allow_same_inter_show' in parameters else True
        self.q_different_inter_show = parameters['question_allow_different_inter_show'] if 'question_allow_different_inter_show' in parameters else True
        self.q_name = parameters['question_allow_name'] if 'question_allow_name' in parameters else True
        self.file_infos = {}

    def make_spkmap(self, spk):
        spkmap = {}
        spkcount = 0
        spkunmap = []
        for s in spk.speaker:
            if not s in spkmap:
                spkunmap.append(s)
                spkmap[s] = spkcount
                spkcount += 1
        return spkmap, spkunmap, spkcount
    
    def range_to_frontiers(self, rng):
        rng.sort()
        pos = 0
        while pos < len(rng) - 1:
            if rng[pos][1] >= rng[pos + 1][0]:
                rng[pos] = (rng[pos][0], max(rng[pos][1], rng[pos + 1][1]))
                rng.pop(pos + 1)
            else:
                pos = pos + 1
        front = []
        for r in rng:
            front.append(("n", r[0]))
            front.append(("p", r[1]))
        return front
    
    def filter_frontier_on_uem(self, front, uem):
        uemi = 0
        fri = 0
        fo = []
        while uemi != len(uem.start_time) and fri != len(front):
            if uem.start_time[uemi] < front[fri][1]:
                if uem.end_time[uemi] >= front[fri][1]:
                    if front[fri][0] != 'n':
                        if len(fo) == 0 or fo[-1][1] < uem.start_time[uemi]:
                            fo.append(('n', uem.start_time[uemi]))
                        fo.append((front[fri][0], front[fri][1]))
                    else:
                        fo.append((front[fri][0], front[fri][1]))
                    fri += 1
                else:
                    if front[fri][0] != 'n':
                        if len(fo) == 0 or fo[-1][1] < uem.start_time[uemi]:
                            fo.append(('n', uem.start_time[uemi]))
                        fo.append((front[fri][0], uem.end_time[uemi]))
                    uemi += 1
            else:
                fri += 1
        return fo

    def filter_frontiers_on_uem(self, front, uem):
        fo = []
        for fr in front:
            fo.append(self.filter_frontier_on_uem(fr, uem))
        return fo
    
    def merge_two_frontiers(self, front1, front2, end1, end2):
        frontr = []
        pos1 = 0
        pos2 = 0
        while pos1 < len(front1) or pos2 < len(front2):
            ctime = (
                front1[pos1][1]
                if pos2 == len(front2)
                else front2[pos2][1]
                if pos1 == len(front1)
                else min(front1[pos1][1], front2[pos2][1])
            )
            mode1 = end1 if pos1 == len(front1) else front1[pos1][0]
            mode2 = end2 if pos2 == len(front2) else front2[pos2][0]
            frontr.append((mode1 + mode2, ctime))
            if pos1 != len(front1) and front1[pos1][1] == ctime:
                pos1 += 1
            if pos2 != len(front2) and front2[pos2][1] == ctime:
                pos2 += 1
        return frontr
    
    
    def make_merge_frontier(self, hyp_union, ref_union, ref_frontiers_collar):
        hr = self.merge_two_frontiers(hyp_union, ref_union, "n", "n")
        frontr = []
        for f in ref_frontiers_collar:
            frontr.append(self.merge_two_frontiers(hr, f, "nn", "n"))
        return frontr
    
    
    def make_frontiers(self, spk, spkmap, spkcount):
        rngs = [[] for i in range(spkcount)]
        for i in range(0, len(spk.speaker)):
            spki = spkmap[spk.speaker[i]]
            rngs[spki].append((spk.start_time[i], spk.end_time[i]))
        front = []
        for r in rngs:
            front.append(self.range_to_frontiers(r))
        return front
    
    
    def make_union_frontiers(self, spk):
        rngs = []
        for i in range(0, len(spk.speaker)):
            rngs.append((spk.start_time[i], spk.end_time[i]))
        return self.range_to_frontiers(rngs)
    
    
    def frontiers_add_collar(self, front, collar):
        cfront = []
        for f in front:
            a = f[1] - collar
            b = f[1] + collar
            if a < 0:
                a = 0
            if len(cfront) == 0 or a > cfront[-1][1]:
                cfront.append((f[0], a))
                cfront.append(("t", b))
            else:
                cfront[-1] = ("t", b)
        return cfront
    
    
    def make_times(self, front):
        times = []
        for s in front:
            time = 0
            ptime = 0
            for p in s:
                if p[0] == "n":
                    ptime = p[1]
                elif p[0] == "p":
                    time += p[1] - ptime
            times.append(time)
        return times
    
    
    def add_time(self, thyp, thyn, mode, eh, er, tc, efa, emiss, econf):
        if mode == "ppp":
            return eh, er + thyn, tc + thyp, efa, emiss, econf + thyn
        if mode == "ppn":
            return eh + thyp, er, tc, efa, emiss, econf
        if mode == "ppt":
            return eh, er, tc + thyp, efa, emiss, econf
        if mode == "pnn":
            return eh + thyp, er, tc, efa + thyp, emiss, econf
        if mode == "pnt":
            return eh, er, tc + thyp, efa, emiss, econf
        if mode == "npp":
            return eh, er + thyn, tc, efa, emiss + thyn, econf
        # npn npt nnn nnt
        return eh, er, tc, efa, emiss, econf
    
    
    def compute_times(self, frontr, fronth):
        eh = 0
        er = 0
        rc = 0
        efa = 0
        emiss = 0
        econf = 0
        hpos = 0
        tbeg = 0
        thyp = 0
        hypbef = 0
        for f in frontr:
            tend = f[1]
            while hpos < len(fronth):
                dinter = min(fronth[hpos][1], tend)
                if fronth[hpos][0] == "p":
                    thyp += dinter - hypbef
                if fronth[hpos][1] > tend:
                    break
                hypbef = dinter
                hpos += 1
            eh, er, rc, efa, emiss, econf = self.add_time(
                thyp, tend - tbeg - thyp, f[0], eh, er, rc, efa, emiss, econf
            )
    
            if hpos < len(fronth):
                hypbef = min(fronth[hpos][1], tend)
            tbeg = tend
            thyp = 0
        while hpos < len(fronth):
            if fronth[hpos][0] == "p":
                thyp += fronth[hpos][1] - tbeg
            tbeg = fronth[hpos][1]
            hpos += 1
        eh, er, rc, efa, emiss, econf = self.add_time(
            thyp, 0, "pnn", eh, er, rc, efa, emiss, econf
        )
        return (
            round(eh, 3),
            round(er, 3),
            round(rc, 3),
            round(efa, 3),
            round(emiss, 3),
            round(econf, 3),
        )
    
    
    def compute_miss(self, funion, front):
        miss = []
        for f1 in front:
            hpos = 0
            tbeg = 0
            thyp = 0
            hypbef = 0
            fa = 0
            for f in funion:
                tend = f[1]
                while hpos < len(f1):
                    dinter = min(f1[hpos][1], tend)
                    if f1[hpos][0] == "p":
                        thyp += dinter - hypbef
                    if f1[hpos][1] > tend:
                        break
                    hypbef = dinter
                    hpos += 1
                if f[0] == "n":
                    fa += thyp
                if hpos < len(f1):
                    hypbef = min(f1[hpos][1], tend)
                tbeg = tend
                thyp = 0
            while hpos < len(f1):
                if f1[hpos][0] == "p":
                    thyp += f1[hpos][1] - tbeg
                tbeg = f1[hpos][1]
                hpos += 1
            fa += thyp
            fa = round(fa, 3)
            miss.append(fa)
        return miss
    
    
    def accumulate_confusion(self, fref, fhyp, map_rh, map_hr):
        ref_spkcount = len(fref)
        hyp_spkcount = len(fhyp)
        correct_ref = [0] * ref_spkcount
        correct_hyp = [0] * hyp_spkcount
        lost_ref = [0] * ref_spkcount
        lost_hyp = [0] * hyp_spkcount
        confusion_matrix = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
        fri = [0] * ref_spkcount
        fhi = [0] * hyp_spkcount
        cur_time = 0
        while True:
            ridx = []
            r_is_t = []
            hidx = []
            time = -1
    
            # Build the list of who is in the segment
            for i in range(ref_spkcount):
                if fri[i] != len(fref[i]):
                    cf = fref[i][fri[i]]
                    if time == -1 or cf[1] < time:
                        time = cf[1]
                    if cf[0] != "n":
                        ridx.append(i)
                        r_is_t.append(cf[0] == "t")
    
            for i in range(hyp_spkcount):
                if fhi[i] != len(fhyp[i]):
                    cf = fhyp[i][fhi[i]]
                    if time == -1 or cf[1] < time:
                        time = cf[1]
                    if cf[0] != "n":
                        hidx.append(i)
    
            if time == -1:
                break
    
            # Only do the computations when there's something to do
            if len(ridx) > 0 or len(hidx) > 0:
                duration = time - cur_time
    
                # Hyp and ref mapped together end up in correct time and are removed from the lists
                i = 0
                while i != len(ridx):
                    r = ridx[i]
                    h = map_rh[r]
                    dropped = False
                    if h != -1:
                        slot = -1
                        for j in range(len(hidx)):
                            if hidx[j] == h:
                                slot = j
                                break
                        if slot != -1:
                            correct_ref[r] += duration
                            correct_hyp[h] += duration
                            ridx.pop(i)
                            r_is_t.pop(i)
                            hidx.pop(slot)
                            dropped = True
                    if not dropped:
                        i += 1
    
                # Ref in transition is removed from the list if mapped to some hyp
                i = 0
                while i != len(ridx):
                    r = ridx[i]
                    if r_is_t[i] and map_rh[r] != -1:
                        ridx.pop(i)
                        r_is_t.pop(i)
                    else:
                        i += 1
    
                if len(hidx) == 0:
                    # If there's no hyp, we're all in lost_ref
                    for r in ridx:
                        lost_ref[r] += duration
    
                elif len(ridx) == 0:
                    # If there's no ref, we're all in lost_hyp
                    for h in hidx:
                        lost_hyp[h] += duration
    
                else:
                    # Otherwise we're in confusion.  Amount of confusion time to give
                    # is equal to the max of the ref and hyp times
                    conf_time = max(len(ridx), len(hidx)) * duration
    
                    # Number of slots, otoh, is equal to the product of the number of
                    # refs and hyps
                    conf_slots = len(ridx) * len(hidx)
    
                    # Give the time equally in all slots
                    conf_one_time = conf_time / conf_slots
                    for r in ridx:
                        for h in hidx:
                            confusion_matrix[r, h] += conf_one_time
    
            # Step all the done segments
            for r in range(ref_spkcount):
                if fri[r] != len(fref[r]) and fref[r][fri[r]][1] == time:
                    fri[r] += 1
            for h in range(hyp_spkcount):
                if fhi[h] != len(fhyp[h]) and fhyp[h][fhi[h]][1] == time:
                    fhi[h] += 1
            cur_time = time
    
        return correct_ref, correct_hyp, lost_ref, lost_hyp, confusion_matrix
    
    
    def find_common_point(self, f1, f2):
        fr = merge_two_frontiers(f1, f2, "nn", "n")
        st = None
        en = None
        dur = None
        for i in range(1, len(fr)):
            if fr[i][0] == "pp":
                st1 = fr[i - 1][1]
                en1 = fr[i][1]
                dur1 = en1 - st1
                if dur == None or dur < dur1:
                    st = st1
                    en = en1
                    dur = dur1
        # Should we randomize?  Let's be nice for now
        return (st + en) / 2

    def align(self, ref, hyp, uem, collar):
        r = {}
        r['ref_spkmap'], r['ref_spkunmap'], r['ref_spkcount'] = self.make_spkmap(ref)
        r['hyp_spkmap'], r['hyp_spkunmap'], r['hyp_spkcount'] = self.make_spkmap(hyp)
    
        r['ref_frontiers'] = self.filter_frontiers_on_uem(self.make_frontiers(ref, r['ref_spkmap'], r['ref_spkcount']), uem)
        r['hyp_frontiers'] = self.filter_frontiers_on_uem(self.make_frontiers(hyp, r['hyp_spkmap'], r['hyp_spkcount']), uem)
        r['ref_frontiers_collar'] = []
        for front in r['ref_frontiers']:
            r['ref_frontiers_collar'].append(self.filter_frontier_on_uem(self.frontiers_add_collar(front, collar), uem))
    
        r['ref_union'] = self.filter_frontier_on_uem(self.make_union_frontiers(ref), uem)
        r['hyp_union'] = self.filter_frontier_on_uem(self.make_union_frontiers(hyp), uem)
    
        r['merge_frontiers'] = self.make_merge_frontier(r['hyp_union'], r['ref_union'], r['ref_frontiers_collar'])
    
        r['ref_times'] = self.make_times(r['ref_frontiers'])
        r['hyp_times'] = self.make_times(r['hyp_frontiers'])
    
        eh = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        er = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        tc = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        efa = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        emiss = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        econf = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
        de = np.zeros((r['ref_spkcount'], r['hyp_spkcount']), dtype="float64")
    
        r['miss_hyp'] = self.compute_miss(r['ref_union'], r['hyp_frontiers'])
        r['miss_ref'] = self.compute_miss(r['hyp_union'], r['ref_frontiers'])
    
        for rr in range(r['ref_spkcount']):
            for hh in range(r['hyp_spkcount']):
                (
                    eh[rr, hh],
                    er[rr, hh],
                    tc[rr, hh],
                    efa[rr, hh],
                    emiss[rr, hh],
                    econf[rr, hh],
                ) = self.compute_times(r['merge_frontiers'][rr], r['hyp_frontiers'][hh])
                de[rr, hh] = (
                        r['ref_times'][rr] + r['miss_hyp'][hh] - efa[rr, hh] - emiss[rr, hh] - econf[rr, hh]
                )
    
        r['map_rh'] = [-1] * r['ref_spkcount']
        r['map_hr'] = [-1] * r['hyp_spkcount']
        solved_ref = [0] * r['ref_spkcount']
        solved_hyp = [0] * r['hyp_spkcount']
        for rs, hs in self.ref_to_hyp_name_map.items():
            rid = r['ref_spkmap'][rs] if rs in r['ref_spkmap'] else -1
            hid = r['hyp_spkmap'][hs] if hs in r['hyp_spkmap'] else -1
            if rid != -1:
                solved_ref[rid] = -1
            if hid != -1:
                solved_hyp[hid] = -1
            if rid != -1 and hid != -1:
                r['map_rh'][rid] = hid
                r['map_hr'][hid] = rid

        solved_ref_back = []
        solved_hyp_back = []
        for i in range(r['ref_spkcount']):
            if solved_ref[i] == 0:
                solved_ref[i] = len(solved_ref_back)
                solved_ref_back.append(i)
        for i in range(r['hyp_spkcount']):
            if solved_hyp[i] == 0:
                solved_hyp[i] = len(solved_hyp_back)
                solved_hyp_back.append(i)

        solved_ref_count = len(solved_ref_back)
        solved_hyp_count = len(solved_hyp_back)
        opt_size = max(solved_ref_count, solved_hyp_count)
        costs = np.zeros((opt_size, opt_size), dtype="float64")
        for r1 in range(solved_ref_count):
            rr = solved_ref_back[r1]
            for h1 in range(solved_hyp_count):
                hh = solved_hyp_back[h1]
                costs[r1, h1] = -round(de[rr, hh] * 1000)            

        (map1, map2) = linear_sum_assignment(costs)
        for i1 in range(opt_size):
            i = map1[i1]
            j = map2[i1]
            if (
                i < solved_ref_count
                and j < solved_hyp_count
                and de[i, j] > 0
                and tc[i, j] > 0
            ):
                rr = solved_ref_back[i]
                hh = solved_hyp_back[j]
                r['map_rh'][rr] = hh
                r['map_hr'][hh] = rr
    
        r['ref_mixed_frontiers'] = []
        for rr in range(r['ref_spkcount']):
            if r['map_rh'][rr] == -1:
                r['ref_mixed_frontiers'].append(r['ref_frontiers'][rr])
            else:
                r['ref_mixed_frontiers'].append(r['ref_frontiers_collar'][rr])
    
        (
            r['correct_ref'],
            r['correct_hyp'],
            r['lost_ref'],
            r['lost_hyp'],
            r['confusion_matrix'],
        ) = self.accumulate_confusion(r['ref_mixed_frontiers'], r['hyp_frontiers'], r['map_rh'], r['map_hr'])
    
        r['conf'] = 0
        for rr in range(r['ref_spkcount']):
            for hh in range(r['hyp_spkcount']):
                r['conf'] += r['confusion_matrix'][rr, hh]
        r['totaltime'] = 0
        r['miss'] = 0
        for rr in range(r['ref_spkcount']):
            r['totaltime'] += r['ref_times'][rr]
            r['miss'] += r['lost_ref'][rr]
        r['fa'] = 0
        for hh in range(r['hyp_spkcount']):
            r['fa'] += r['lost_hyp'][hh]
        return r

    def find_best_information(ref, hyp, collar, uem):
        """
    
        :param ref:
        :param hyp:
        :param collar:
        :return:
        """

        r = self.align(ref, hyp, uem, collar)
        best_segment_fix = None
    
        # Do one pass over the reference segments to see how much to gain if one hypothesis segment is corrected
        # Assume the speaker is correct if there's only one, or that the biggest is correct otherwise
    
        nf = len(r['ref_frontiers'][0])
        for i in range(0, len(ref.speaker)):
            # segment boundaries
            st = ref.start_time[i]
            en = ref.end_time[i]
    
            # amount of silence before and after the segment
            silence_before = 0
            silence_after = 0
            for f in ref_union:
                if f[1] < st:
                    silence_before = st - f[1] if f[0] == 'p' else 0
                if f[1] > en:
                    silence_after = f[1] - en if f[0] == 'n' else 0
                    break
    
            # scan the hypothesis, collate the per-speaker time
            hyptime = {}
            for j in range(0, len(hyp_frontiers)):
                hst = hyp.start_time[j]
                hen = hyp.end_time[j]
                if not (hen <= st or hst >= en):
                    if hen > en:
                        hen = en
                    if hst < st:
                        hst = st
                    hspk = hyp.speaker[j]
                    if hspk in hyptime:
                        hyptime[hspk] += hen - hst
                    else:
                        hyptime[hspk] = hen - hst
    
            # compute the fixed time under the assumption that the longest speaker is correct
            fixed_time = 0
            if len(hyptime) > 1:
                best_time = 0
                for s in hyptime:
                    tm = hyptime[s]
                    if tm > best_time:
                        best_time = tm
                    fixed_time += tm
                fixed_time -= best_time
    
            # compute the time in speech in the silences on the border, and the time in silence in the speech
            if len(hyp_union) > 0:
                stf = 0
                enf = len(hyp_union) - 1
                for j in range(0, len(hyp_union)):
                    if hyp_union[j][1] < st:
                        stf = j
                    if hyp_union[j][1] > en:
                        enf = j
                        break
                # pre/post-segment silence
                if hyp_union[stf][1] < st and hyp_union[stf][0] == 'n':
                    sp = st - silence_before;
                    if sp < hyp_union[stf][1]:
                        sp = hyp_union[stf][1]
                    fixed_time += st - sp
                if hyp_union[enf][1] > en and hyp_union[enf][0] == 'p':
                    sp = en + silence_after;
                    if sp > hyp_union[enf][1]:
                        sp = hyp_union[enf][1]
                    fixed_time += sp - en
                # in-segment silence
                sp = st
                for j in range(stf, enf + 1):
                    if hyp_union[j][1] > st and hyp_union[j][0] == 'p':
                        sp = hyp_union[j][1]
                    if hyp_union[j][1] > st and hyp_union[j][1] < en and hyp_union[j][0] == 'n':
                        fixed_time += hyp_union[j][1] - sp
    
            else:
                # nothing in the hypothesis, all the time is fixed
                fixed_time += en - st;
            if fixed_time:
                if (best_segment_fix == None) or (best_segment_fix[1] < fixed_time):
                    best_segment_fix = [fixed_time, st, en]
    
        # find the couple of maximum confusion where both sides are mapped
        max_conf = 0
        max_conf_r = None
        max_conf_h = None
        for r in range(r['ref_spkcount']):
            for h in range(r['hyp_spkcount']):
                if r['confusion_matrix'][r, h] > max_conf and r['map_rh'][r] != -1 and r['map_hr'][h] != -1:
                    max_conf = confusion_matrix[r, h]
                    max_conf_r = r
                    max_conf_h = h
        if max_conf_r != None:
            # Of the two, pick the speaker with the maximum amount of error associated
            error_spk_ref = r['lost_ref'][r]
            for h in range(hyp_spkcount):
                error_spk_ref += r['confusion_matrix'][max_conf_r, h]
            error_spk_hyp = r['lost_hyp'][h]
            for r in range(ref_spkcount):
                error_spk_hyp += r['confusion_matrix'][r, max_conf_h]
    
            if (error_spk_ref > error_spk_hyp) or not correction_type[1]:
                # We want to pivot on the reference, that means merging the mapped hyp speaker and the mapped max error hyp speaker
                correct_point = find_common_point(r['ref_frontiers'][max_conf_r], r['hyp_frontiers'][r['map_rh'][max_conf_r]])
                bad_point = find_common_point(r['ref_frontiers'][max_conf_r], r['hyp_frontiers'][max_conf_h])
                p1 = min(correct_point, bad_point)
                p2 = max(correct_point, bad_point)
                max_conf_a = Answer(True, "same", np.float32(p1), np.float32(p2), "", "")
                #max_conf_a = {"answer": {"value": True}, "response_type": "same", "time_1": np.float32(p1),
                #              "time_2": np.float32(p2)}
            elif (error_spk_hyp >= error_spk_ref) or not correction_type[0]:
                # We want to pivot on the hypothesis, that means splitting the mapped ref speaker and the mapped max error ref speaker
                correct_point = find_common_point(r['ref_frontiers'][r['map_hr'][max_conf_h]], r['hyp_frontiers'][max_conf_h])
                bad_point = find_common_point(r['ref_frontiers'][max_conf_r], r['hyp_frontiers'][max_conf_h])
                #print(f"{correct_point} {bad_point}")
                p1 = min(correct_point, bad_point)
                p2 = max(correct_point, bad_point)
                max_conf_a = Answer(False, "same", np.float32(p1), np.float32(p2), "", "")
                #max_conf_a = {"answer": {"value": False}, "response_type": "same", "time_1": np.float32(p1),
                #              "time_2": np.float32(p2)}
    
        if (best_segment_fix == None and max_conf == 0) or (correction_type == (False, False, False)):
            #return {"answer": {"value": False}, "response_type": "stop", "time_1": np.float32(0.0),
            #        "time_2": np.float32(0.0)}
            return Answer(False, "stop", np.float32(0.0), np.float32(0.0), "", "")
        if best_segment_fix == None or max_conf > best_segment_fix[0] or not correction_type[2]:
            return max_conf_a
        else:
            #return {"answer": {"value": True}, "response_type": "boundary", "time_1": np.float32(best_segment_fix[1]),
            #        "time_2": np.float32(best_segment_fix[2])}
            return Answer(True, "boundary", np.float32(best_segment_fix[1]), np.float32(best_segment_fix[2]), "", "")

    def compute_answer_cost(self, a):
        cost = 0
        if a.response_type == "same":
            time_1 = a.time_1
            time_2 = a.time_2
            if type(time_1) is list:
                cost += (time_1[1]-time_1[0])+(time_2[1]-time_2[0])
            else:
                if abs(time_2 - time_1) >= self.request_collar_cost:
                    cost += 2 * self.request_collar_cost
                else:
                    cost += max(time_1, time_2) - min(time_1, time_2) + self.request_collar_cost
        elif a.response_type == "boundary":
            cost = max(a.time_2 - a.time_1, self.request_collar_cost)
        elif a.response_type == "name":
            cost = self.request_collar_cost
        return cost

    def read(self, file_info, uem, reference):
        assert(file_info not in self.file_infos)
        self.file_info = file_info
        self.file_infos[file_info.file_id] = [reference, uem, file_info]

    def validate(self, message):
        answer = {}
#         print("entered validate:")
        #print(f"cost = {self.cost}, et max = {self.max_cost_per_file}")
        if self.cost >= self.max_cost_per_file:
            answer = Answer(False, "stop", 0.0, 0.0, "", "")
        elif message.file_info.supervision == "active":
            if message.system_request.request_type == "same":
                time_1 = message.system_request.time_1
                time_2 = message.system_request.time_2
                second_show = message.system_request.second_show
                #change below answer, in order to deal with non perfect segmentation
                if type(time_1) is list:
                    spk1 = self.find_speaker_for_segment(time_1[0],time_1[1])
                else:
                    spk1 = self.find_speaker_for_time(time_1)
                    
                if type(time_2) is list:
                    spk2 = self.find_speaker_for_segment(time_2[0],time_2[1], second_show)
                else:
                    spk2 = self.find_speaker_for_time(time_2, second_show)
                    
                if type(time_1) is list:
                    self.cost += (time_1[1]-time_1[0])+(time_2[1]-time_2[0])
                    print(
                        "USER: Check for same on %0.2f-%0.2f (%s) vs. %0.2f-%0.2f (%s)"
                        % (time_1[0],time_1[1], spk1, time_2[0],time_2[1], spk2)
                    )
                else:
                    if abs(time_2 - time_1) >= self.request_collar_cost:
                        self.cost += 2 * self.request_collar_cost
                    else:
                        self.cost += max(time_1, time_2) - min(time_1, time_2) + self.request_collar_cost
                    print(
                        "USER: Check for same on %0.2f (%s) vs. %0.2f (%s)"
                        % (time_1, spk1, time_2, spk2)
                    )
                if spk1 ==None or spk2==None:
                    print("Asking about a time where is not annotated in reference as speaker.")
                    # By putting answer.name="None" the correction can be signaled that Does the question has been asked? 
                    answer = Answer(spk1 == spk2, "same", time_1, time_2, "" if second_show == "" or second_show == self.file_info else second_show, "None")
                else:
                    answer = Answer(spk1 == spk2, "same", time_1, time_2, "" if second_show == "" or second_show == self.file_info else second_show, "")

            elif message.system_request.request_type == "boundary":
                st, en = self.find_segment_for_time(message.system_request.time_1)
                if st != None:
                    self.cost += max(en - st, self.request_collar_cost)
                    print(
                        "USER: Check for boundary on %f (%f - %f)"
                        % (message.system_request.time_1, st, en)
                    )
                    answer = Answer(True, "boundary", st, en, "", "" )
                else:
                    self.cost += self.request_collar_cost
                    print(
                        "USER: Check for boundary on %f (not speech)"
                        % (message.system_request.time_1)
                    )
                    answer = Answer(False, "boundary", 0.0, 0.0, "", "" )

            elif message.system_request.request_type == "name":
                spk1 = self.find_speaker_for_time(message.system_request.time_1)
                if spk1 != "" and spk1 in self.ref_to_hyp_name_map:
                    spk1 = self.ref_to_hyp_name_map[spk1]
                answer = Answer(spk1 != "", "name", message.system_request.time_1, 0.0, "", spk1)

        elif message.file_info.supervision == "interactive":
            #print("Interactive model ON")
            answer = find_best_information(self.file_infos[self.file_info.file_id][0],
                                           message.hypothesis,
                                           self.file_infos[self.file_info.file_id][1], 
                                           0.250,
                                           correction_type=self.correction_type)

        else:
            answer = Answer(True, "stop", 0.0, 0.0, "" )
            #answer = {
            #    "response_type": 'stop',
            #    "time_1": np.float32(0),
            #    "time_2": np.float32(0),
            #    "answer": {"value": False},
            #}
        self.cost += self.compute_answer_cost(answer)
        #return answer['response_type'] != "stop", answer
        return answer.response_type != "stop", answer

    def final_commit(self, hypothesis):
        res = []
        r = self.align(self.file_infos[self.file_info.file_id][0], hypothesis, self.file_infos[self.file_info.file_id][1], 0.250)
        for hh in range(r['hyp_spkcount']):
            hn = r['hyp_spkunmap'][hh]
            if hn in self.hyp_to_ref_name_map:
                res.append([hn, "known"])
                continue
            duration = r['hyp_times'][hh]
            ri = r['map_hr'][hh]
            if ri == -1:
                if duration < self.minimal_validation_time:
                    res.append([hn, "short"])
                else:
                    res.append([hn, "bad"])
                continue
            ratio = r['correct_hyp'][hh] / duration
            if ratio < self.minimal_validation_purity:
                res.append([hn, "bad"])
                continue
            rn = r['ref_spkunmap'][ri]
            self.hyp_to_ref_name_map[hn] = rn
            self.ref_to_hyp_name_map[hn] = hn
            res.append([hn, "good"])
        return res

    def find_segment_for_time(self, time):
        ref = self.file_infos[self.file_info][0]
        for i, s in enumerate(ref.speaker):
            if (
                    time >= ref.start_time[i]
                    and time < ref.end_time[i]
            ):
                return ref.start_time[i], ref.end_time[i]
        return None, None

    def find_speaker_for_time(self, time, show = ""):
        show = show.file_id if show != "" else self.file_info.file_id
        ref = self.file_infos[show][0]
        for i, s in enumerate(ref.speaker):
            #            print(i, s, time, )
            if (
                    time >= ref.start_time[i]
                    and time < ref.end_time[i]
            ):
                return s
        return None
    
    def find_speaker_for_segment(self, start_time, end_time, show = ""):
        show = show.file_id if show != "" else self.file_info.file_id
        ref = self.file_infos[show][0]
        
        max_dur_seg=0
        best_match_spk=None
        for i, s in enumerate(ref.speaker):
            intersec_dur=min(end_time,ref.end_time[i])-max(start_time,ref.start_time[i])
            if intersec_dur>max_dur_seg:
                max_dur_seg=intersec_dur
                best_match_spk=s
                    
        return best_match_spk


class Request:

    def __init__(self, request_type, time_1, time_2, second_show=""):
        self.request_type = request_type
        self.time_1 = time_1
        self.time_2 = time_2
        self.second_show = second_show


class MessageToUser:

    def __init__(self, file_info, hypothesis, system_request):
        self.file_info = file_info
        self.hypothesis = hypothesis
        self.system_request = system_request

class Answer:

    def __init__(self, answer, response_type, time_1, time_2, second_show, name):
        self.answer = answer
        self.response_type = response_type
        self.time_1 = time_1
        self.time_2 = time_2
        self.second_show = second_show
        self.name = name

    def __repr__(self):
        return f"answer = {self.answer}\nresponse_type = {self.response_type}\ntime_1 = {self.time_1}\nsecond_show = {self.second_show}\ntime_2 =  {self.time_2}\nname = {self.name}"

class FileInfo:

    def __init__(self, file_id, supervision, time_stamp):
        self.file_id = file_id
        self.supervision = supervision
        self.time_stamp = time_stamp


class Reference:

    def __init__(self, speaker, start_time, end_time):
        self.speaker = speaker
        self.start_time = start_time
        self.end_time = end_time

    def to_diar(self, show):
        """
        Convert the Reference object into S4D DIAR object
        :return:
        """
        diar = s4d.Diar()
        for spk, start, stop in zip(self.speaker, self.start_time, self.end_time):
            diar.append(show = show,
                        cluster = spk,
                        cluster_type = 'speaker',
                        start = int(float(start) * 100),
                        stop = int(float(stop) * 100))

        return diar


class UEM:

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


    def to_diar(self, show):
        """
        Convert the UEM object into S4D DIAR object
        :return:
        """
        diar = s4d.Diar()
        for start, stop in zip(self.start_time, self.end_time):
            diar.append(show = show,
                        cluster = "uem",
                        start = int(float(start) * 100),
                        stop = int(float(stop) * 100))

        return diar



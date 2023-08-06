#!/usr/bin/python

from user_simulation import *

uparams = {
    "max_cost_per_file": 1000,
    "request_collar_cost": 3,
    "question_allow_boundaries": True,
    "question_allow_same_intra_show": True,
    "question_allow_different_intra_show": True,
    "question_allow_same_inter_show": True,
    "question_allow_different_inter_show": True,
    "question_allow_name": True,
    'minimal_validation_time': 60.0,
    'minimal_validation_purity': 0.8
    }

def load_uem(f):
    st = []
    en = []
    for l in open(f, "r"):
        e = l.split()
        st.append(e[2])
        en.append(e[3])
    return UEM(np.cast["float64"](st), np.cast["float64"](en))

def load_ref(f):
    spk = []
    ref_st = []
    ref_en = []
    for l in open(f, "r"):
        e = l.split()
        ref_st.append(np.cast["float64"](round(float(e[2]), 3)))
        ref_en.append(np.cast["float64"](round(float(e[2]) + float(e[3]), 3)))
        spk.append(e[7])
    return Reference(spk, ref_st, ref_en)

def load_hyp(f):
    return load_ref(f)

us = UserSimulation(uparams)

ref = load_ref("utest/LCP_EntreLesLignes_2013-03-16_212400.mdtm")
uem = load_uem("utest/LCP_EntreLesLignes_2013-03-16_212400.uem")
hyp = load_hyp("utest/20130316.2124.LCP_EntreLesLignes.hyp.mdtm")
fi = FileInfo("20130316.2124.LCP_EntreLesLignes", "active", 0)

us.read(fi, uem, ref)

msg = MessageToUser(fi, hyp, Request('name', 1140, 0, ""))

ans = us.validate(msg)

print(ans)

val = us.final_commit(hyp)
print(val)


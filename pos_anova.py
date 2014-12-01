from scipy import stats
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

nouns = sorted([float(n.replace("\n", "")) for n in tuple(open('n.txt', "r"))])
satellites = sorted([float(n.replace("\n", "")) for n in tuple(open('r.txt', "r"))])
adjs = sorted([float(n.replace("\n", "")) for n in tuple(open('a.txt', "r"))])
ss = sorted([float(n.replace("\n", "")) for n in tuple(open('s.txt', "r"))])
verbs = sorted([float(n.replace("\n", "")) for n in tuple(open('v.txt', "r"))])

plt.hist([n for n in nouns], 5000, color="blue", label="nouns", alpha=.5)
plt.hist([n for n in verbs], 5000, color="red", label="verbs", alpha=.5)
plt.hist([n for n in adjs], 5000, color="green", label="satellites", alpha=.5)
plt.hist([n for n in satellites], 5000, color="yellow", label="adjs", alpha=.5)
plt.hist([n for n in ss], 5, color="gray", label="ss", alpha=.5)

f_val, p_val = stats.f_oneway(nouns, verbs, adjs, satellites, ss)

print "One-way ANOVA P =", p_val  
print "One-way ANOVA F =", f_val  
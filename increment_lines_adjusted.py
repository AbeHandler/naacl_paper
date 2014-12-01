import numpy as np
import sys
import re
import math
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import Image

lowess = sm.nonparametric.lowess

increments = np.linspace(0, 1, num=1000)


#these ratios come from wordnetcheck
synratio = 1.38035667709
hyporatio = 0.358620245857
hyperratio = 1.44090670617
meroratio = 1.83191715951
holoratio = 4.04529267639

syns = []
meros = []
hypers = []
hypos = []
stems = []
holos = []
increments = []

with open("textfiles/increments.txt") as results:
    for line in results.readlines():
        try:
            line = line.replace("\n", "")
            top, bottom, syn, mero, holo, hyper, hypo, stem, none = line.split(",")
            increments.append((float(top) + float(bottom)) / 2)
            syns.append(int(syn))
            holos.append(int(holo))
            meros.append(int(mero))
            hypers.append(int(hyper))
            hypos.append(int(hypo))
            stems.append(int(stem))
        except ValueError:
            pass

syns = np.array(syns)

alpha = .4

x = np.arange(1, len(syns) + 1, 1)

hypers = [h * hyperratio for h in hypers]
syns = [h * synratio for h in syns]
meros = [h * meroratio for h in meros]
holos = [h * holoratio for h in holos]
hypos = [h * hyporatio for h in hypos]


z = [a[1] for a in lowess(hypers, x, frac=.1)]
plt.plot(increments, z, label="Hypernyms", linestyle="-", marker='s', markevery=100)


z = [a[1] for a in lowess(syns, x, frac=.1)]
line, = plt.plot(increments, z, label="Synonyms", linestyle=':', marker='*', markevery=100)


z = [a[1] for a in lowess(hypos, x, frac=.1)]
line, = plt.plot(increments, z, label="Hyponyms", marker='D', markevery=100)
line.set_dashes([2, 6, 2, 6, 2, 6])

z = [a[1] for a in lowess(meros, x, frac=.1)]
plt.plot(increments, z, label="Meronyms", linestyle='-.', marker='^', markevery=100)

z = [a[1] for a in lowess(holos, x, frac=.1)]
plt.plot(increments, z, label="Holonyms", linestyle='--', marker='o', markevery=100)


plt.xlabel('Cosine distance')
plt.ylabel('Adjusted count')
plt.legend(loc=2)
plt.xlim(0,1)
plt.ylim(0, 260)


plt.savefig('increment_lines_adjusted.png', bbox_inches='tight')
Image.open('increment_lines_adjusted.png').convert('L').save('increment_lines_adjusted_bw.png')
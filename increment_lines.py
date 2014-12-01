import numpy as np
import sys
import re
import math
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import Image
import statsmodels.api as sm

from matplotlib.ticker import MultipleLocator

lowess = sm.nonparametric.lowess

increments = np.linspace(0, 1, num=1000)

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

#line.set_dashes([2, 8, 2, 8, 2, 8])

'''
plt.scatter(increments, stems, color="red", alpha=alpha, label="Same stems", marker=".")
plt.scatter(increments, hypers, color="purple", alpha=alpha, label="Hypernyms", marker="o")
plt.scatter(increments, syns, color="green", alpha=alpha, label="Synonyms", marker="+")
plt.scatter(increments, hypos, color="yellow", alpha=alpha, label="Hyponyms", marker="D")
plt.scatter(increments, meros, color="orange", alpha=alpha, label="Meronyms", marker="v")
plt.scatter(increments, holos, color="blue", alpha=alpha, label="Holonyms", marker="^")
'''

plt.xlabel('Cosine distance')
plt.ylabel('Count')
plt.legend(loc=2)
#plt.ylim(1,1000)
#plt.xlim(.2,1)

#plt.axes().yaxis.set_major_locator(MultipleLocator(5))
#plt.axes().xaxis.set_major_locator(MultipleLocator(.01))
#plt.loglog()

plt.xlim(0,1)
plt.ylim(0,260)

plt.savefig('increment_lines.png', bbox_inches='tight')
Image.open('increment_lines.png').convert('L').save('increment_lines_bw.png')
#plt.savefig('increment_lines.png', bbox_inches='tight', pad_inches=.4)
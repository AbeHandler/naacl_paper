import re

totals = [i.replace("\n", "") for i in tuple(open("textfiles/results.txt", "r"))]

lookup = {}
lookup['v'] = "verb"
lookup['a'] = "adjective"
lookup['n'] = "noun"
lookup['r'] = "adverb"
lookup['s'] = "adjective satellite"

typesr = ['hyper', 'hypo', 'syn', 'holo', 'mero']

for typer in typesr:
    vals = [t for t in totals if re.findall("^" + typer, t) > 0]
    for p in lookup.keys():
        pos_hits = [v for v in vals if t.split(",")[1] == p]
        pos_total = sum(float(t.split(",")[2]) for t in pos_hits)
        pos_hits = sum(float(t.split(",")[7]) for t in pos_hits)
        if pos_total > 0:
            totalfrac = round(100 * (pos_hits / pos_total))
        else:
            totalfrac = 0
        print "{} {} {} {} {}".format(typer, lookup[p], pos_total, pos_hits, totalfrac, 3)

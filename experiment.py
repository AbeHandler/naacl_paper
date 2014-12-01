from gensim.models import word2vec
from wordnetter import synononymous
from wordnetter import hypernomous
from wordnetter import not_in_wordnet
from wordnetter import holonymous
from wordnetter import meronymous
from wordnetter import hyoponomous

from wordnetter import get_all_possible_hyponyms
from wordnetter import get_all_possible_hypernyms
from wordnetter import get_all_possible_holonyms
from wordnetter import get_all_possible_meronyms

from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import random
import argparse
import os
import math

try:
    os.remove("textfiles/results.txt")
except OSError:
    pass

model = word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
stemmer = SnowballStemmer("english")
parser = argparse.ArgumentParser()
parser.add_argument('--out', '-o')
args = vars(parser.parse_args())

def same_stem(one, two):
	if stemmer.stem(one) == stemmer.stem(two):
		return True
	else:
		return False

def printout(line):
    if args['out']:
        writeto = "textfiles/" + args['out']
        with open(writeto, "a") as results:
            results.write('\n' + line)

def inStopWords(w):
    if s in stopwords.words('english'):
        return True
    return False

words = list(set(reuters.words()))

random.shuffle(words)

words = set(words)

words = [s for s in words if not inStopWords(s)]

parts_of_speech = [wn.VERB, wn.ADJ, wn.NOUN, wn.ADV, wn.ADJ_SAT]

counter = 0
for r in words:
    counter = counter + 1
    r = r.encode('ascii', 'ignore')
    try:
        k = 0
        sims = model.most_similar(positive=[r], topn=200)
        for s in sims:
            k = k + 1
            for pos in parts_of_speech:
                s = (s[0].encode("ascii", 'ignore'), s[1])
                hit = False
                search = True
                if same_stem(s[0], r):
                    search = False
                    printout(",".join(['same stem', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(counter) + "-" + str(k), str(1)]))
                if not_in_wordnet(r, pos):
                    search = False
                    printout(",".join(['not_in_wordnet', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(counter) + "-" + str(k), str(1)]))
                if search:
                    hyper = hypernomous(r, s[0], pos)
                    hypo = hyoponomous(r, s[0], pos)
                    syno = synononymous(r, s[0], pos)
                    holo = holonymous(r, s[0], pos)
                    mero = meronymous(r, s[0], pos)
                    all_possible_hyper = get_all_possible_hypernyms(r, s[0], pos)
                    all_possible_hypo = get_all_possible_hyponyms(r, s[0], pos)
                    all_possible_mero = get_all_possible_meronyms(r, s[0], pos)
                    all_possible_holo = get_all_possible_holonyms(r, s[0], pos)
                    all_possible_syns = len(wn.synsets(r, pos=pos)) * len(wn.synsets(s[0], pos=pos))
                    tracker = str(counter) + "-" + str(k)
                    printout(",".join(['hyper', pos, str(model.similarity(s[0], r)), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), tracker, str(hyper), str(all_possible_hyper)]))
                    printout(",".join(['hypo', pos, str(model.similarity(s[0], r)), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), tracker, str(hypo), str(all_possible_hypo)]))
                    printout(",".join(['syn', pos, str(model.similarity(s[0], r)), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), tracker, str(syno), str(all_possible_syns)]))
                    printout(",".join(['holo', pos, str(model.similarity(s[0], r)), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), tracker, str(holo), str(all_possible_holo)]))
                    printout(",".join(['mero', pos, str(model.similarity(s[0], r)), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), tracker, str(mero), str(all_possible_mero)]))
                    if (((hyper + hypo + syno + holo + mero) == 0) or ((hyper + hypo + syno + holo + mero) == 5)):
                        printout(",".join(['none', pos, str(model.similarity(s[0], r)), r, s[0], str(s[1]), tracker]))
                    print "debug mero {} {} {}".format(mero, tracker, pos)
                    print "debug syn {} {} {}".format(syno, tracker, pos)
                    print "debug holo {} {} {}".format(holo, tracker, pos)
                    print "debug hpyer {} {} {}".format(hyper, tracker, pos)
                    print "debug hypo {} {} {}".format(hypo, tracker, pos)
                    print "debug total {} {} {}".format(all_possible_syns, tracker, pos)
                    print "******"
                    #print "counter {}".format(str(counter) + "-" + str(k))
                    #printout(",".join(['total', pos, str(all_possible_syns), r.replace(',', ""), s[0].replace(',', ""), str(s[1]), str(counter) + "-" + str(k), str(math.ceil(mero) + math.ceil(holo) + math.ceil(syno) + math.ceil(hypo) + math.ceil(hyper))]))
    except KeyError:
        print printout(",".join(['KeyError', r]))
        pass
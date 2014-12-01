import sys

for line in sys.stdin:
    try:
        numerator = 0
        denominator = 0
        line = line.replace("\n", "")
        pieces = line.split(",")
        num = float(pieces[7])
        dem = float(pieces[8])
        if dem > 0:
            print (num / dem) * 100
        else:
            pass
    except ValueError:
        print "V" + line
    except IndexError:
        print "I" + line
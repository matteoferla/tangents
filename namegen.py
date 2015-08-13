import re
import string
import random
import collections
import sys

__doc__ = """
This is a very simple script..
Autogen is the main function. It returns a string, the first value is the number of species, the second the kmer (1 or 2).
There are no objs. The reason why is that it is highly linear.
trainer and trainer2 were copypaste laziness. sorry.
The trainer generates the data or the data is loaded from the data.json file.
I downloaded the LSPN indices with were parsed with _LPSN_lister for each trainer run. The JSON file is the data.

"""

def trainerdump():
    import json
    json.dump([[trainer(0), trainer(1)],[trainer2(0), trainer2(1)]],open('data.json','w',encoding="utf8"))

def trainerload(kmer,i):
    import json
    obj=json.load(open('data.json','r',encoding="utf8"))
    return obj[kmer-1][i]

def autogen(pool=100, kmer=1):
    out=''
    if kmer == 1:
        gn = trainerload(1,0)
        sp = trainerload(1,1)
        for a in range(1, pool):
            out+=generator(gn).capitalize() + " " + generator(sp)+"\n"
    else:
        gn = trainerload(2,0)
        sp = trainerload(2,1)
        for a in range(1, pool):
            out+=generator2(gn).capitalize() + " " + generator2(sp)+"\n"
    return out

def trainer2(n=0):
    bacteria = _LPSN2lister('AC.html') + _LPSN2lister('DL.html') + _LPSN2lister('MR.html') + _LPSN2lister('SZ.html')
    lista = ['__' + i[n].lower() + '_' for i in bacteria]
    d = collections.Counter([k[i:i + 3] for k in lista for i in range(0, len(k) - 2)])
    kpool = [q + g for g in '_' + string.ascii_lowercase for q in '_' + string.ascii_lowercase]
    for i in kpool:
        try:
            # s=sys.float_info.epsilon
            s = 0
            for k in '_' + string.ascii_lowercase:
                s += d[i + k]
            for k in '_' + string.ascii_lowercase: d[i + k] /= s
        except ZeroDivisionError:
            pass
    return d

def generator2(di):
    letter = '__'
    word = _chooser(di, letter)
    word += _chooser(di, '_' + word)
    tm = 0
    while tm < 1000:
        letter = _chooser(di, word[-2:])[-1]
        if letter == '_': break
        word += letter
        tm += 1
    else:
        word = generator2(di)
    return word

def trainer(n):
    bacteria = _LPSN2lister('AC.html') + _LPSN2lister('DL.html') + _LPSN2lister('MR.html') + _LPSN2lister(
        'SZ.html')  # renamed downloads of http://www.bacterio.net/-allnamesac.html
    lista = ['_' + i[n].lower() + '_' for i in bacteria]
    d = collections.Counter([k[i:i + 2] for k in lista for i in range(0, len(k))])
    for i in '_' + string.ascii_lowercase:
        s = 0
        for k in '_' + string.ascii_lowercase:
            s += d[i + k]
        for k in '_' + string.ascii_lowercase: d[i + k] /= s
    return d

def generator(di):
    letter = '_'
    word = ''
    while True:
        letter = _chooser(di, letter)
        if letter == '_': break
        word += letter
    return word

def _chooser(di, p):
    s = 0
    x = random.random()
    for i in '_' + string.ascii_lowercase:
        s += di[p + i]
        if s > x: break
    else:
        raise Exception('Bug: ' + p + '+something is impossible')
    return i

def _LPSN2lister(fn):
    l = ''
    with open(fn, encoding="utf8") as f:
        l = f.read()
    return [[m.group(1), m.group(2)] for m in
            re.finditer('\<span class\=\"genusspecies\"\>(\w+)\<\/span\>\s+\<span class\=\"\w+\"\>(\w+)', l)]



if __name__ == "__main__":
    print(autogen(100,2))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__description__ = \
    """
This script determines what is the ancrstry of a set of sequences.
For more see: http://blog.matteoferla.com/2017/07/in-vivo-shuffling-via-heteroduplex.html

Multiple separate files? If you
cat *.seq > sequencing.fa
You will need to check that there is a space before > due to missing \\n before end of file.
I fixed mine with search-and-replace-all and not pretentiously with awk.

NB. Written for python 3, not tested under 2.
"""
__author__ = "Matteo Ferla. [Github](https://github.com/matteoferla)"
__email__ = "matteo.ferla@gmail.com"
__date__ = ""
__license__ = "Cite me!"
__version__ = "1.0"

import argparse
from pprint import PrettyPrinter

pp = PrettyPrinter()

verbose=False
if verbose:
    debugprint=print
else:
    debugprint=lambda *x: None

import csv, os, re
from collections import Counter
from Bio import SeqIO
#from Bio import pairwise2 #this seems to be broken

def heteroduplex_resolvase(infile, reffile, reversed=False):
    refball=list(SeqIO.parse(reffile,'fasta'))
    for query in SeqIO.parse(infile,'fasta'):
        debugprint(query.name)
        #reverse
        if reversed:
            query.seq=query.seq.reverse_complement()
        #trim
        while query.seq[-1] == 'N':
            query.seq=query.seq[:-1]
        while query.seq[0] == 'N':
            query.seq=query.seq[1:]
        #align
        SeqIO.write([query,*refball],'temp.fa','fasta')
        os.system('/usr/local/bin/muscle -in temp.fa -out temp.al.fa -quiet')
        out=list(SeqIO.parse('temp.al.fa','fasta'))
        #find where does the coding part start in the ref.
        #TODO find what the secret command in muscle to stop the reshuffling.
        #Actually it seems to not shuffle when its pairwise.
        ref_al=[]
        for gene in out:
            if gene.name == query.name:
                query=gene
            else:
                ref_al.append(gene)
        # check for ends
        outofbound=True
        same = Counter()
        differ=Counter()
        variant_count=0
        conserved_count=0
        issue_count=0
        var_sites=[]
        for i in range(len(query.seq)):
            alldash=all([gene.seq[i] == '-' for gene in ref_al])
            if alldash==False and outofbound == True:
                outofbound = False
                debugprint('Read starts at ',i)
            if alldash==True and outofbound == False: #so you have got to the end.
                outofbound=True
                debugprint('Read stops at ', i)
                break
            if not outofbound:
                consensus=all([gene.seq[i] == query.seq[i] for gene in ref_al])
                error=not any([gene.seq[i] == query.seq[i] for gene in ref_al])
                if not consensus:
                    if not error:
                        same.update([gene.name for gene in ref_al if gene.seq[i] == query.seq[i]])
                        differ.update([gene.name for gene in ref_al if gene.seq[i] != query.seq[i]])
                        variant_count+=1
                        var_sites.append(i)
                    else:
                        debugprint('ISSUE in line ',i,': ', query.seq[i], ' vs. ', *[gene.seq[i] for gene in ref_al])
                        issue_count+=1
                else:
                    conserved_count+=1
        if variant_count+conserved_count>200:
            a=[gene.seq for gene in ref_al if gene.name == same.most_common(2)[0][0]][0]
            b=[gene.seq for gene in ref_al if gene.name == same.most_common(2)[1][0]][0]
            x=query.seq
            dealbraker_sites=[i for i in var_sites if a[i] != b[i]]
            an=sum([a[i] == x[i] for i in dealbraker_sites])
            bn=sum([b[i] == x[i] for i in dealbraker_sites])
        if verbose or variant_count+conserved_count>200:
            print('In {seq} are {var} variants and {cons} conserved ({issue} issues). Best two: {best}. Site favoring the first {first}, the second {second}. Total: {other}'.format(
                seq=query.name, var=variant_count, cons=conserved_count, issue=issue_count,first=an,second=bn,
                best=''.join(['{FP} = {same} match &  {diff} differ; '.format(FP=x,same=same[x],diff=differ[x]) for x, xi in same.most_common(2)]), other=same.most_common()))
        debugprint('#'*12)


if __name__ == "__main__" and 1 == 0:
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input", help="the query fasta file")
    parser.add_argument("reference", help="the reference file")
    parser.add_argument("-reverse", action='store_true', help="the reference file")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    heteroduplex_resolvase(args.input, args.reference, args.reverse)
else:
    heteroduplex_resolvase('sequencing.fa','refs.pure.fa',True)

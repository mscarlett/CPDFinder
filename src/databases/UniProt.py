'''
Created on Feb 19, 2014

@author: Michael Scarlett
'''
import urllib,urllib2
import os
from os.path import join
import databases
from databases import OMIM
url = 'http://www.uniprot.org/'

def createMIMdir():
    with open(databases.MIM_TO_SP_FILE, "r") as fh1:
        for line in fh1:
            try:
                strs = line.split()
                mim = int(strs[0][:-1])
                pds = OMIM.getPDs(mim)
                if len(pds) != 0:
                    remainder = strs[1:]
                    sp = remainder[0]
                    with open(join(databases.PD_DIR,sp), "w") as fh2:
                        for pd in pds:
                            fh2.write(pd.string()+"\n")
                    with open(join(databases.OMIM_DIR, sp), "w") as fh2:
                        fh2.write(str(mim))
            except:
                pass

def getMIM(sp):
    with open(join(databases.OMIM_DIR, sp),"r") as fh:
        return fh.read()

def getFASTA(protein):
    fname = "http://www.uniprot.org/uniprot/" + protein + ".fasta"
    response = urllib2.urlopen(fname)
    result = response.read()
    return result

def fetch(**params):
    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = "mscarle3@jhu.edu"
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    result = response.read()
    return result

def buildDict():
    names = set()
    with open(databases.OMIM_DICT_FILE, "r") as fh:
        for line in fh:
            names.add(int(line.strip()))
    sps = []
    with open(databases.MIM_TO_SP_FILE, "r") as fh:
        for line in fh:
            try:
                strs = line.split()
                mim = int(strs[0][:-1])
                if mim not in names:
                    continue
                remainder = strs[1:]
                while remainder[-1] == ",":
                    remainder += fh.next().split()
                length = len(remainder) + 1
                           
                for i in range(0,length/3):
                    sp = remainder[i*3]
                    if os.path.exists(join(databases.FEP_DIR,sp)):
                        sps.append(sp)
            except:
                pass
    with open(databases.UNIPROT_DICT_FILE, "w") as fh2:
        for sp in sps:
            fh2.write(sp + "\n")
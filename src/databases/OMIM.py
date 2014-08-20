from __future__ import division

from Bio.Data.IUPACData import protein_letters_3to1
import urllib
import urllib2
import ast
import databases
import datetime as dt
import time
import re

#We are limited to 4 requests per second
requestsPerSecond = 4
minDelta = dt.timedelta(microseconds=1000000*1/requestsPerSecond)
lastTime = dt.datetime.now()
regex = re.compile(" AND | OR |, | \(")

def getPDs(mim):
    data = fetch(mimNumber=mim,include="all")
    allelicVariants = data["omim"]["entryList"][0]["entry"]["allelicVariantList"]
    del data
    
    pds = []
    
    for entry in allelicVariants:
        try:
            mutation = entry["allelicVariant"]["mutations"]
            mutation = regex.split(mutation)[1:]
            for m in mutation:
                try:
                    first = m[0:3]
                    second = m[-3:]
                    position = m[3:-3]
                    pds.append(newPD(first, second, position))
                except ValueError:
                    #Position is not a number
                    pass
                except KeyError:
                    #Strings are not amino acids
                    pass
                except AttributeError:
                    #First or second are not strings
                    pass
        except KeyError:
            #No mutations?
            pass    
        
    return pds

def fetch(**params):
    #Check delta time to make sure we aren't making too many requests
    delta = dt.datetime.now() - lastTime
    if delta < minDelta:
        time.sleep((minDelta.microseconds-delta.microseconds)/1000000)
        
    params["apiKey"] = "4ED97F7F9E1FDA2F779979BCB92CB8BFBC100AF9"
    params["format"] = "python"
    
    url = "http://api.omim.org/api/entry?" + urllib.urlencode(params)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    result = response.read()
    return ast.literal_eval(result)

def buildDict():
    with open(databases.OMIM_SPROT_FILE, "r") as fh1, open(databases.OMIM_DICT_FILE, "w") as fh2:
        for line in fh1:
            try:
                line = line.strip()
                if line[1:5] == "omim":
                    num = int(line[10:16])
                    fh2.write(str(num)+"\n")
            except:
                pass

def newPD(original, mutated, position):
    return original + position + mutated
    
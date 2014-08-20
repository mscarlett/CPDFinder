import databases
import gzip
from os.path import join
import urllib2
from xml.etree import ElementTree

XML_GZ_FILE = "http://www.bioinf.org.uk/fosta/fosta.xml.gz"

class SimpleReader(object):
    
    def __init__(self, fh):
        self.iterator = ElementTree.iterparse(fh, events=("start", "end"))
        __, self.root = next(self.iterator)
        self.fh = fh
    
    def __iter__(self):
        for event, elem in self.iterator:
            if event == "start":
                if elem.tag == "fep":
                    protein = elem.text
                    if protein != None:
                        self.animalProteins.append(protein)
                    else:
                        self.fh.write(self.humanProtein.attrib["id"] + " " + str(len(self.animalProteins))+"\n")
                    elem.clear()
                elif elem.tag == "root":
                    self.humanProtein = elem
                    self.animalProteins = []
                else:
                    elem.clear()
            elif event == "end" and elem.tag == "root":
                yield elem.attrib["id"], self.animalProteins
                self.humanProtein.clear()
            else:
                elem.clear()
                
    def process(self):
        for humanProtein, animalProteins in self:
            with open(join(databases.FEP_DIR, humanProtein)) as f:
                for animalProtein in animalProteins:
                    f.write(animalProtein + "\n")
            
def download(destFileName):
    compressedFile = urllib2.urlopen(XML_GZ_FILE)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode="rb")
    with open(destFileName, 'w') as outfile:
        for line in decompressedFile:
            outfile.write(line)
'''
Pipeline for obtaining missense mutations that cause Mendelian disease
from the OMIM database and parsing them to find compensated pathogenic deviations

Created on Jun 21, 2014

@author: Michael Scarlett

Note: BioPython and Luigi are required to resolve dependencies.
'''
import databases
from databases import ClustalOmega, FOSTA, OMIM, PDB, UniProt
from Bio import SeqIO
from Bio.Data.IUPACData import protein_letters_3to1
import logging
import luigi
import os
from os.path import join, basename, dirname
import sys

# creates a symlink to wherever the run directory is
RUN_DIR = dirname(dirname(os.path.abspath(__file__)))
    
class parseFOSTA(luigi.ExternalTask):
    def run(self):
        FOSTA.download(join(databases.FOSTA_DIR, databases.FOSTA_XML_FILE))
        reader = FOSTA.SimpleReader()
        reader.process()
        
    def requires(self):
        return None
        
class parseMIM(luigi.ExternalTask):
    def run(self):
        UniProt.createMIMdir()
        
    def requires(self):
        return None
        
class parsePDs(luigi.ExternalTask):
    def run(self):
        fnames = os.listdir(databases.FEP_DIR)
        for fname in fnames:
            try:
                mim = UniProt.getMIM(fname)
                pds = OMIM.getPDs(mim)
                if len(pds) > 0:
                    with open(join(databases.PD_DIR,fname),"w") as fh:
                        for pd in pds:
                            fh.write(pd.string()+"\n")
            except Exception, e:
                logging.error(e)
                    
        def requires(self):
            return (parseMIM(), parseFOSTA())
                    
class parseFASTA(luigi.ExternalTask):
    def run(self):
        fnames = os.listdir(databases.PD_DIR)
        for fname in fnames:
            path = join(databases.FEP_DIR,fname)
            if not os.path.isfile(path):
                os.remove(path)
            else:
                proteins = []
                proteins.append(fname)
                with open(join(databases.FEP_DIR,fname), "r") as fh:
                    for line in fh:
                        proteins.append(line.strip())
                fastas = []
                for protein in proteins:
                    fasta = UniProt.getFASTA(protein)
                    fastas.append(fasta)
                del proteins
                with open(join(databases.ALIGN_DIR,fname), "w") as fh:
                    for fasta in fastas:
                        fh.write(fasta)
                        
    def requires(self):
            return parsePDs()
    
class alignFASTA(luigi.ExternalTask):
    def run(self):
        fnames = os.listdir(databases.FASTA_DIR)
        ClustalOmega.align(fnames)
            
    def requires(self):
        return parseFASTA()
    
class parseCPD(luigi.ExternalTask):
    def run(self):
        fnames = os.listdir(databases.FASTA_DIR)
        for fname in fnames:
            cpds = []
            with open(join(databases.FASTA_DIR, fname), "r") as fh1, open(join(databases.PD_DIR, fname), "r") as fh2:
                fasta = SeqIO.parse(fh1, "fasta")
                for line in fh2:
                    line = line.rstrip()
                    mutation = protein_letters_3to1[line[-3:]]
                    position = mutation[3:-3] - 1
                    for animalProtein in fasta:
                        if mutation in animalProtein.seq[position]:
                            cpds.append((line, animalProtein))
            with open(join(databases.CPD_DIR,fname), "w") as fh:
                for (original, mutated) in cpds:
                    fh.write(original + " " + mutated + "\n")
                    
    def requires(self):
        return alignFASTA()
                    
class parsePDB(luigi.ExternalTask):
    def run(self):
        raise NotImplementedError
    
    def requires(self):
        return parseCPD()

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stderr,
        format="%(created)f %(filename)s:%(lineno)s [%(funcName)s] %(message)s",
        level=logging.DEBUG)
        
    luigi.run()
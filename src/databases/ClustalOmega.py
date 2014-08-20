'''
Created on Aug 20, 2014

@author: Michael
'''
from Bio.Align.Applications import ClustalOmegaCommandline
import databases
import os
from os.path import join

def align(fnames):
    os.chdir(databases.CLUSTAL_OMEGA)
    for fname in fnames:
        in_file = join(databases.FASTA_DIR, fname)
        out_file = join(databases.ALIGN_DIR, fname)
        clustalomega_cline = ClustalOmegaCommandline(infile=in_file, outfile=out_file, seqtype="Protein", verbose=True, auto=True, force=True)
        clustalomega_cline()
from os.path import join

# Constants for resolving file locations
BASE_DIR = "./data/"
FEP_DIR = join(BASE_DIR,"proteins/FEP/")
PD_DIR = join(BASE_DIR,"proteins/PD/")
FOSTA_DIR = join(BASE_DIR,"proteins/FOSTA/")
FASTA_DIR = join(BASE_DIR,"proteins/FASTA/")
OMIM_DIR = join(BASE_DIR,"proteins/OMIM/")
CPD_DIR = join(BASE_DIR,"proteins/CPD/")
ALIGN_DIR = join(BASE_DIR,"proteins/align/")
FOSTA_XML_FILE = join(FOSTA_DIR, "fosta.xml")
MIM_TO_SP_FILE = join(BASE_DIR, "mimtosp.txt")
PDB_TO_SP_FILE = join(BASE_DIR, "pdbtosp.txt")
OMIM_SPROT_FILE = join(OMIM_DIR, "omim_sprot.xml")
OMIM_DICT_FILE = join(OMIM_DIR, "omim_dict.txt")
UNIPROT_DICT_FILE = join(OMIM_DIR, "uniprot_dict.txt")

#Later on I will find a way to do this more cleanly
CLUSTAL_OMEGA = "C:\\clustal-omega-1.2.0-win32"
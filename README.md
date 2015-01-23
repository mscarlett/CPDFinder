# CPDFinder
Pipeline for obtaining compensated pathogenic deviations from public databases and performing machine learning.

Note: I began this project several months ago but did a very sloppy job, so at some point I hope to redo everything when my semester is over.

The goal of this project is to use machine learning to analyze which features are most important for predicting whether disease-causing mutations in human proteins occur as the most common allelic variant in nonhuman proteins which have similar functionality (in which case the mutation is said to ba a compensated pathogenic deviation) or if this compensation does not occur.

The pipeline is as roughly as follows:
1.) For human proteins in UniProt, acquire the functionally equivalent animal proteins associated with each human protein from the <a href="http://www.bioinf.org.uk/fosta/">FOSTA</a> website
--1a.) Download the FOSTA XML file (which can be found at <a href="http://www.bioinf.org.uk/fosta/fosta.xml.gz">this link</a>)
--1b.) For each human protein, which is delimited by <root></root>, parse all of the animal proteins, which are delimited by <fep></fep> tags
--1c.) Using SQLite, create a table containing all human protein-animal protein mappings
2.) Download the FASTA files for all human and animal proteins directly from UniProt and store in SQLite
3.) For all proteins in UniProt with functionally equivalent animal proteins, acquire the disease-causing misssense mutations associated with the protein and the amino acid position at which the mutation occurs
--3a.) Select all human proteins from the SQLite database
--3b.) From dbSNP and ClinVar, download the disease-causing mutations associated with each protein and store in SQLite
4.) Aligh the animal proteins with their associated human proteins using the ClustalW algorithm, then store in SQLite. This uses the BioPython module at <a href="http://biopython.org/DIST/docs/_api_158/Bio.Clustalw-module.html">this link</a> and step requires downloading the clustalw command-line client at <a href="ftp://ftp-igbmc.u-strasbg.fr/pub/ClustalW/">ftp://ftp-igbmc.u-strasbg.fr/pub/ClustalW/</a>.
5.) For each mutation in the human protein and the amino acid position at which the mutation occurs
--5a.) Obtain list of human proteins from SQLite
--5b.) For each human protein, obtain mutations and multiple sequence alignment from SQLite
--5c.) For each mutation, search the list of animal proteins at that exact position and get a list of all animal proteins for which the mutation is found as a normal allelic variant
--5d.) Store the mutation-animal protein pairs in SQLite
6.) For each mutation in human proteins, create a feature vector containing its structural and amino acid properties and store in SQLite.
7.) Use machine learning to predict the extent to which a particular mutation occurs as the normal allelic variant in animal protein.
--7a.) Select the feature vectors corresponding to the mutations of the human protein from SQLite
--7b.) For particular human proteins, compute the average number of times that an amino acid in the animal protein differs from the human protein so that the counts for compensated pathogenic deviations are normalized by the probability that an animo acid differs at random. This means that a compensated pathogenic deviation will be less relevant when it is found in an animal protein that differs significantly.
--7c.) Use cross-validation to train a SVM classifier using the computed metric
--7d.) Predict the probability that a particular mutation in human protein occurs as a natural allelic variant in animal proteins using the SVM classifier.
--7e.) Store results in SQLite
8.) Perform data visualization to analyze results by analyzing which features were most important for classifier accuracy.

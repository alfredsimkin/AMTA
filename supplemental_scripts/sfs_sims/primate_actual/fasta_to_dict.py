#takes primate fasta entries and stores them as a nested dictionary suitable for pattern_distributions.py
import sys
import custom
import cPickle
fasta_file=sys.argv[1]
fasta_lists=custom.read_fasta(fasta_file)
gene_dict={}
gene_dict['fake_gene']={}
for species in fasta_lists:
	gene_dict['fake_gene'][species[0]]=species[1]
cPickle.dump(gene_dict, open('sim_parsimony_dict', 'w'))


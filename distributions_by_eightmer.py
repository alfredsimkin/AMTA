#total, gain_count, loss_count, targeting_gain_count, targeting_loss_count, site_inc_count, site_dec_count, site_shift_count=0,0,0,0,0,0,0,0

import cPickle
import custom
import glob
import sys
data_folder=sys.argv[1]
eightmer_dict={}
output_file=open(data_folder+'distributions_by_eightmer', 'w')
eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
#species_list=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon', '1', '2', '3']
file_list=sorted(glob.glob(data_folder+'ind_turnover_counts/*'))

for dict_number, dict_name in enumerate(file_list):
	print 'progress is', dict_number, '/', len(file_list), 'or', float(dict_number)/len(file_list)
	gene_dict=cPickle.load(open(dict_name))
	if dict_number==0:
		species_list=gene_dict[gene_dict.keys()[0]].keys()
	for eightmer in eightmer_list:
#		print eightmer
		if eightmer not in eightmer_dict:
			eightmer_dict[eightmer]={}
		for gene in gene_dict:
#			print gene
			for species in species_list:
				if eightmer not in gene_dict[gene][species]:
					l='[0,0,0]'
				else:
					l=str(gene_dict[gene][species][eightmer])
				if species not in eightmer_dict[eightmer]:
					eightmer_dict[eightmer][species]={}
				if l not in eightmer_dict[eightmer][species]:
					eightmer_dict[eightmer][species][l]=0
				eightmer_dict[eightmer][species][l]+=1
	print eightmer_dict['GGTAAATT']
cPickle.dump(eightmer_dict, output_file)

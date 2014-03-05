#total, gain_count, loss_count, targeting_gain_count, targeting_loss_count, site_inc_count, site_dec_count, site_shift_count=0,0,0,0,0,0,0,0

import cPickle
import custom
ninemer_dict={}
output_file=open('distributions_by_ninemer', 'w')
ninemer_list=custom.count_in_base('AAAAAAAAA', 4, 'ACGTz')
species_list=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon', '1', '2', '3']

for number in range(1,620):
	print 'loading', number
	gene_dict=cPickle.load(open('full_9mer_counts'+str(number)))
	print 'loaded', number
	for ninemer in ninemer_list:
#		print ninemer
		if ninemer not in ninemer_dict:
			ninemer_dict[ninemer]={}
		for gene in gene_dict:
#			print gene
			for species_number, species in enumerate(species_list):
				if ninemer not in gene_dict[gene][species]:
					l='[0,0,0]'
				else:
					l=str(gene_dict[gene][species][ninemer])
				if species not in ninemer_dict[ninemer]:
					ninemer_dict[ninemer][species]={}
				if l not in ninemer_dict[ninemer][species]:
					ninemer_dict[ninemer][species][l]=0
				ninemer_dict[ninemer][species][l]+=1
cPickle.dump(ninemer_dict, output_file)

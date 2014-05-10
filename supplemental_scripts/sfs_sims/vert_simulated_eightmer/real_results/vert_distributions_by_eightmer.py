#total, gain_count, loss_count, targeting_gain_count, targeting_loss_count, site_inc_count, site_dec_count, site_shift_count=0,0,0,0,0,0,0,0

import cPickle
import custom
eightmer_dict={}
output_file=open('vert_distributions_by_eightmer', 'w')
eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
species_list=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']

for number in range(1,2):
	print 'loading', number
	gene_dict=cPickle.load(open('full_8mer_counts'+str(number)))
	print 'loaded', number
	for eightmer in eightmer_list:
#		print eightmer
		if eightmer not in eightmer_dict:
			eightmer_dict[eightmer]={}
		for gene in gene_dict:
#			print gene
			for species_number, species in enumerate(species_list):
				if eightmer not in gene_dict[gene][species]:
					l='[0,0,0]'
				else:
					l=str(gene_dict[gene][species][eightmer])
				if species not in eightmer_dict[eightmer]:
					eightmer_dict[eightmer][species]={}
				if l not in eightmer_dict[eightmer][species]:
					eightmer_dict[eightmer][species][l]=0
				eightmer_dict[eightmer][species][l]+=1
cPickle.dump(eightmer_dict, output_file)

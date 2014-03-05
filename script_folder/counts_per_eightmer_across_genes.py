#total, gain_count, loss_count, targeting_gain_count, targeting_loss_count, site_inc_count, site_dec_count, site_shift_count=0,0,0,0,0,0,0,0

import cPickle
import custom
eightmer_dict={}
#gene_dict=cPickle.load(open('full_8mer_counts1'))
for number in range(1,2):
	print 'loading', number
	gene_dict=cPickle.load(open('full_8mer_counts_new'+str(number)))
	print 'loaded', number
	eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
	species_list=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon', '1', '2', '3']
	for eightmer in eightmer_list:
		print eightmer
		if eightmer not in eightmer_dict:
			eightmer_dict[eightmer]={}
		for gene in gene_dict:
#			print gene
			for species_number, species in enumerate(species_list):
				results=[0,0,0,0,0,0,0,0]
				if eightmer in gene_dict[gene][species]:
					l=gene_dict[gene][species][eightmer]
					if gene=='NM_001003800' and species=='human' and eightmer=='AAAAAAAA':
						print l
					results[0]+=l[0]
					if l[1]>0:
						results[1]+=l[1]
						if l[2]==0 and l[1]==l[0]:
							results[3]+=1
						elif l[1]>l[2]:
							results[5]+=1
						elif l[1]==l[2]:
							results[7]+=1
					if l[2]>0:
						results[2]+=l[2]
						if l[0]==0:
							results[4]+=1
						elif l[2]>l[1]:
							results[6]+=1
				if species not in eightmer_dict[eightmer]:
					eightmer_dict[eightmer][species]=[0,0,0,0,0,0,0,0]
				full_results=eightmer_dict[eightmer][species]
				if eightmer=='AAAAAAAA' and (species=='human' or species=='3'):
					print 'cumulative before current', species, full_results
					print 'current', species, results
				eightmer_dict[eightmer][species]=[full_results[result_number]+result for result_number, result in enumerate(results)]
			of_interest=eightmer_dict['AAAAAAAA']
			if of_interest['human'][0]!=of_interest['3'][0]+of_interest['human'][1]-of_interest['human'][2]:
				print of_interest
				exit()
print eightmer_dict['ACCAAAGA']
print 'AAAAAAAA'
print eightmer_dict['AAAAAAAA']

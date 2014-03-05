import cPickle
ancestor_dict={'human':'3', 'chimp':'3', '3':'2', 'gorilla':'2', '2':'1', 'orangutan':'1', 'gibbon':'1'}
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
gene_dict=cPickle.load(open('final_utr_dictionary_nogaps'))
species_list=['3', '2', '1']
good_list=['A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
for species in species_list:
	descendants=descendant_dict[species]
	for descendant in descendants:
		mutation_dict={}
		for gene_number, gene in enumerate(gene_dict):
			if gene_number%100==0:
				print gene_number
			for letter_number, junk in enumerate(gene_dict[gene][species][:-7]):
				ancestor_eightmer=gene_dict[gene][species][letter_number:letter_number+8].upper()
				descendant_eightmer=gene_dict[gene][descendant][letter_number:letter_number+8].upper()
				not_equal=0
				good=True
				for letter_number in range(8):
					if ancestor_eightmer[letter_number] not in good_list or descendant_eightmer[letter_number] not in good_list:
						good=False
						break
					if ancestor_eightmer[letter_number]!=descendant_eightmer[letter_number]:
						not_equal+=1
				if good:
					if not_equal not in mutation_dict:
						mutation_dict[not_equal]=0
					mutation_dict[not_equal]+=1
		print species, descendant, mutation_dict

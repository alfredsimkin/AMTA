import cPickle
import custom
full_dict=cPickle.load(open('vert_dictionary'))
actual_species=['40', '39', '37', '35', '34', '32', '30', '27', '26', '24', '22', '20', '19', '15', '14', '12', '9', '7', '5', '4', '1']
title_list=['A         ', 'B         ', 'C         ', 'D         ', 'E         ', 'F         ', 'G         ', 'H         ', 'I         ', 'J         ', 'K         ', 'L         ', 'M         ', 'N         ', 'O         ', 'P         ', 'Q         ', 'R         ', 'S         ', 'T         ', 'U         ']
sequence_list=[]
for gene in full_dict:
	for species_number, species in enumerate(actual_species):
		sequence_list.append(full_dict[gene][species])
phylip_list=[actual_species, sequence_list]
custom.print_phylip(title_list, phylip_list, 'phylip_vert_sim')

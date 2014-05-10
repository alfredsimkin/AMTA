import cPickle
import custom
full_dict=cPickle.load(open('sim_ml_input_dict'))
actual_species=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon']
title_list=['human     ', 'chimp     ', 'gorilla   ', 'orangutan ', 'gibbon    ']
sequence_list=[]
for gene in full_dict:
	for species_number, species in enumerate(actual_species):
		sequence_list.append(full_dict[gene][species])
phylip_list=[actual_species, sequence_list]
custom.print_phylip(title_list, phylip_list, 'infile')

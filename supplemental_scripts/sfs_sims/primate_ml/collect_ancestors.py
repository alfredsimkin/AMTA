import cPickle
def collect_ancestors():
	species_dict, start_line={}, 100000
	for line_number, line in enumerate(open('outfile')):
		if 'Reconstructed' in line:
			start_line=line_number+2
		if line_number>=start_line:
			line=line.strip().split()
			if line:
				species_name=line[0]
				species_sequence=''.join(line[1:])
				if species_name not in species_dict:
					species_dict[species_name]=''
				species_dict[species_name]+=species_sequence.upper()
	return species_dict
old_values=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon', '3', '2', '1']
new_values=['human', 'chimp', 'gorilla', 'orangutan', 'gibbon', '3', '2', '1']

new_dict={}
old_dict=collect_ancestors()
for species_number, old_species in enumerate(old_values):
	new_dict[new_values[species_number]]=old_dict[old_species]
final_dict={}
final_dict['fake_gene']={}
for gene in final_dict:
	for species in new_dict:
		final_dict[gene][species]=new_dict[species]
cPickle.dump(final_dict, open('sim_ml_output_dict', 'w'))

print final_dict['fake_gene']['human']

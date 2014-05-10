import cPickle
def collect_ancestors():
	species_dict={}
	for line_number, line in enumerate(open('outfile')):
		if line_number>=115:
			line=line.strip().split()
			if line:
				species_name=line[0]
				species_sequence=''.join(line[1:])
				if species_name not in species_dict:
					species_dict[species_name]=''
				species_dict[species_name]+=species_sequence.upper()
	return species_dict
old_values=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
new_values=['40', '39', '37', '35', '34', '32', '30', '27', '26', '24', '22', '20', '19', '15', '14', '12', '9', '7', '5', '4', '1', '0', '6', '8', '10', '16', '28', '36', '38', '29', '31', '33', '17', '21', '23', '25', '18', '11', '13', '3']

new_dict={}
old_dict=collect_ancestors()
for species_number, old_species in enumerate(old_values):
	new_dict[new_values[species_number]]=old_dict[old_species]
final_dict={}
final_dict['fake_gene']={}
for gene in final_dict:
	for species in new_dict:
		final_dict[gene][species]=new_dict[species]
cPickle.dump(final_dict, open('ml_vert_dict', 'w'))

print final_dict['fake_gene']['0']

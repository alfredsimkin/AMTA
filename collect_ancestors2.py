def collect_ancestors():
	species_dict, treelist={}, []
	for line_number, line in enumerate(open('outfile')):
		if line_number>=51:
			line=line.strip().split()
			if line:
				species_name=line[0]
				species_sequence=''.join(line[1:])
				if species_name not in species_dict:
					species_dict[species_name]=''
				species_dict[species_name]+=species_sequence
	return species_dict

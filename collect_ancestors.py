def collect_ancestors():
	template_list=['+human\n', '+3\n', '+2+chimp\n', 
	'||\n', '|+gorilla\n', '|\n', '1orangutan\n', '|\n', '+gibbon\n']
	species_dict, treelist={}, []
	for line_number, line in enumerate(open('outfile')):
		if line_number>=17 and line_number<=25:
			line=line.replace('-', '')
			treelist.append(line.replace(' ', ''))
		if line_number>=51:
			line=line.strip().split()
			if line:
				species_name=line[0]
				species_sequence=''.join(line[1:])
				if species_name not in species_dict:
					species_dict[species_name]=''
				species_dict[species_name]+=species_sequence
	if treelist!=template_list:
		print "phylogeny changed"
		print '\n'.join(treelist)
		exit()
	return species_dict

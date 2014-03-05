species_dict={}
for line in open('multiz11way_trimmed.maf'):
	line=line.split()
	if len(line)>1:
		species=line[1].split('.')[0]
		if species not in species_dict:
			species_dict[species]=0
		species_dict[species]+=int(line[3])
for species in species_dict:
	print species+'\t'+str(species_dict[species])

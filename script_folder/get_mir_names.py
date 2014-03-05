final_list=[]
value_list=[line.strip().split() for line in open('values')]
mirlist=[line.strip().split() for line in open('enrich_depletion_results_lumped_vert_seeds')]
for value_line in value_list:
	for mirline in mirlist:
		if mirline[1].replace('U', 'T')==value_line[0] and value_line[0] not in final_list:
			print value_line[0], mirline[4:]
			final_list.append(value_line[0])
			

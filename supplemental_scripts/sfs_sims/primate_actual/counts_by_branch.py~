branch_dict={}
for line_number, line in enumerate(open('eightmer_sums_by_species')):
	if line_number>0:
		line=line.strip().split()
		branch_event=line[1]+' g'
		if branch_event not in branch_dict:
			branch_dict[branch_event]=0
		branch_dict[branch_event]+=int(line[3])
		branch_event=line[1]+' l'
		if branch_event not in branch_dict:
			branch_dict[branch_event]=0
		branch_dict[branch_event]+=int(line[4])
print branch_dict

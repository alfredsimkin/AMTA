#takes in total sites summed across genes, gains, and losses, 
#each line being an eightmer, species combination
#prints out eightmer, total sites, gains, losses, controlled 
#gains and controlled losses summed across all branches
inlist=[line.strip().split() for line in open('quick_out')]
eightmer_dict={}
for line in inlist:
	eightmer, species=line[:2]
	current_summary=map(int, line[2:])
	if eightmer not in eightmer_dict:
		eightmer_dict[eightmer]=[0,0,0]
	summed=eightmer_dict[eightmer]
	eightmer_dict[eightmer]=[summed_value+current_value for summed_value, current_value in zip(summed, current_summary)]
for eightmer in eightmer_dict:
	if eightmer_dict[eightmer][0]>0:
		print eightmer, ' '.join(map(str, eightmer_dict[eightmer])), float(eightmer_dict[eightmer][1])/eightmer_dict[eightmer][0], float(eightmer_dict[eightmer][2])/eightmer_dict[eightmer][0]
	else:
		print eightmer, ' '.join(map(str, eightmer_dict[eightmer])), 0, 0

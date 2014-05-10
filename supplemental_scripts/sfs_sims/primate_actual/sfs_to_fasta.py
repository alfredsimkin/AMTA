import sys
populations, input_file=sys.argv[1:]
#populations is total number of species including ancestors, numbered according to sfs_parameters
output_file=open(input_file+'.fa', 'w')
sfs_output=[line.strip().split(';') for line in open(input_file)][4:]
ancestor=sfs_output[0][0]
ancestor_list=[ancestor for number in range(int(populations))]
sfs_output=sfs_output[3:]
for line in sfs_output:
	for mutation in line:
		mutation=mutation.split(',')
		pop_dict={}
		for pop in mutation[12:]:
			pop=pop.split('.')
			if pop[0] not in pop_dict:
				pop_dict[pop[0]]=0
			pop_dict[pop[0]]+=1
			if pop[1]=='-1':
				old_string=ancestor_list[int(pop[0])]
				ancestor_list[int(pop[0])]=old_string[:int(mutation[2])]+mutation[6]+old_string[int(mutation[2])+1:]
		for pop in pop_dict:
			if pop_dict[pop]>6:
				old_string=ancestor_list[int(pop)]
				ancestor_list[int(pop)]=old_string[:int(mutation[2])]+mutation[6]+old_string[int(mutation[2])+1:]
for ancestor_number, ancestor in enumerate(ancestor_list):
	output_file.write('>'+str(ancestor_number)+'\n')
	output_file.write(ancestor+'\n')

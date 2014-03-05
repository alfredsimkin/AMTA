import custom
mirlist=[line.strip().split() for line in open('miRbase_18_mature.fa')]
mer_dict={}
for line in mirlist:
	mer=custom.revcom(line[-1][1:8])
	if mer not in mer_dict:
		mer_dict[mer]=[]
	mer_dict[mer].append(line[0])
for mer in mer_dict:
#	print mer_dict[mer]
	species_list=[mir[0:3] for mir in mer_dict[mer]]
	if 'hsa' in species_list and 'mmu' in species_list and 'dre' in species_list:# and 'dme' in species_list:
		print mer, mer_dict[mer]

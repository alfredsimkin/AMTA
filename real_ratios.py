print 'eightmer real_ratio'
annotation_list=[line for line in open('enrich_depletion_results_lumped_vert_seeds')]
ratio_list=[line.strip().split() for line in open('ratios')]
eightmer_set=set([])
for line in annotation_list:
	if 'hsa' in line and 'ggo' in line and 'ppy' in line and 'ptr' in line:
		eightmer_set.add(line.split()[1].replace('U', 'T'))
real_ratios=[ratio_line for eightmer in eightmer_set for ratio_line in ratio_list if ratio_line[0]==eightmer]
for line in real_ratios:
	print ' '.join(line)

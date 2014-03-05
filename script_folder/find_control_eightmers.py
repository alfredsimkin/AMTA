import custom
eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
status_list=[line.strip().split('\t') for line in open('enrich_depletion_results_lumped_vert_seeds')]
status_list=status_list[1:]
real_mirs={}

def twomer_counts(eightmer):
	eightmer_dict={}
	for letter_number in range(7):
		twomer=eightmer[letter_number:letter_number+2]
		if twomer not in eightmer_dict:
			eightmer_dict[twomer]=0
		eightmer_dict[twomer]+=1
	return eightmer_dict


for line in status_list:
	joined_line=''.join(line)
	if len(line)>4 and ('hsa' in joined_line or 'ptr' in joined_line or 'ggo' in joined_line or 'ppy' in joined_line):
		real_mirs[line[1][1:-1]]=[]
print len(real_mirs)

for real_mir in real_mirs:
	real_dict=twomer_counts(real_mir)
	for eightmer in eightmer_list:
		eightmer_dict={}
		test_dict=twomer_counts(eightmer)
		if test_dict==real_dict and eightmer[1:-1] not in real_mirs:
			real_mirs[real_mir].append(eightmer)
	print real_mir, len(real_mirs[real_mir])

final_probs=[line.strip().split() for line in open('eightmer_nearest_neighbor_values')]
output_file=open('real_eightmer_ranked_results', 'w')
real_dict={}
mer_length=8
for line in open('real_eightmers_human_mouse_fish'):
	real_dict[line[:mer_length]]=eval(line[mer_length+1:])

for line in final_probs:
	for mer in real_dict:
		if line[0]==mer:
			output_file.write('\t'.join(line)+'\t'+'/'.join(real_dict[mer])+'\n')

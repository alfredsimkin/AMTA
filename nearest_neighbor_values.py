import sys
data_folder=sys.argv[1]
output_file=open(data_folder+'eightmer_nearest_neighbor_values', 'w')
eightmer_list=[line.strip().split() for line in open(data_folder+'eightmer_sums_across_species')]
eightmer_dict={}
for eightmer_line in eightmer_list[1:]:
	eightmer_dict[eightmer_line[0]]=eightmer_line

choices='ACGT'

def sort_by_total(line_list):
	return int(line_list[1])
def sort_by_gains(line_list):
	return float(line_list[4])
def sort_by_losses(line_list):
	return float(line_list[5])
for mirseed in sorted(eightmer_dict.keys()):
	sorting_list=[]
	mir_value=eightmer_dict[mirseed]
	sorting_list.append(mir_value)
	for pos in range(len(mirseed)):
		for choice in choices:
			if choice!=mirseed[pos]:
				one_off=mirseed[:pos]+choice+mirseed[pos+1:]
				sorting_list.append(eightmer_dict[one_off])
	sorting_list.sort(key=sort_by_total, reverse=True)
	total_rank=sorting_list.index(mir_value)
	sorting_list.sort(key=sort_by_gains)
	gain_rank=sorting_list.index(mir_value)
	sorting_list.sort(key=sort_by_losses)
	loss_rank=sorting_list.index(mir_value)
	mir_value.extend([str(total_rank+1), str(gain_rank+1), str(loss_rank+1)])
	output_file.write('\t'.join(mir_value)+'\n')

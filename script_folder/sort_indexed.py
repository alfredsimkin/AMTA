import sys
data_folder=sys.argv[1]
output_file=open(data_folder+'exactly_once_indices_sorted', 'w')
def sort_by_species(index_summary):
	ref_list=index_summary.split(':')[1].split('\t')[0].split(',')
	ref_list[1], ref_list[2]=int(ref_list[1]), int(ref_list[2])
	return ref_list
#old input was indexed_all_chunks
full_index=[line for line in open(data_folder+'exactly_once_chunk_indices')]
#print "indexed, sorting"
full_index.sort(key=sort_by_species)
#print "sorted"
for line in full_index:
	output_file.write(line)

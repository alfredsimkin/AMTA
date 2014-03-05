def get_human_boundaries(line):
	gene_name, chrom, three_prime=line[0], line[1], int(line[-1].split(',')[-1])
	if line[3]:
		five_prime=int(line[3].split(',')[0])
	else:
		five_prime=int(line[5].split(',')[0])
	if five_prime<three_prime:
		small, big=five_prime, three_prime
	else:
		small, big=three_prime, five_prime
	return [chrom, small, big, gene_name]

def advance_chunk(chunk_file):
	chunk_line=chunk_file.readline()
	if chunk_line:
		maf_line=chunk_line.split(']], [[')[1].split(', ')
		maf_line[0]=maf_line[0][1:-1]
		maf_line[1:]=[int(value) for value in maf_line[1:]]
		return chunk_line, maf_line
	else:
		print "starting loop"
		for filtered_coder in total_coders:
			filtered_coder_file.write(coding_dict[filtered_coder])
		exit()

coding_list=open('converted_coords_single_3UTRexon').readlines()[1:]
coding_dict, coding_summary, coding_number, total_coders={}, [], 0, set([])
for line in coding_list:
	split_line=line.strip().split('\t')
	coding_summary.append(get_human_boundaries(split_line))
	if split_line[0] not in coding_dict:
		coding_dict[split_line[0]]=line
	else:
		print 'duplicate', split_line[0]
coding_summary.sort()

chunk_file=open('exactly_once_indices_sorted')
filtered_maf_file=open('putatively_filtered_maf_coords', 'w')
filtered_coder_file=open('putatively_filtered_coding_genes', 'w')

chunk_line, maf_line=advance_chunk(chunk_file)
coding_line=coding_summary[coding_number]

while chunk_line:
	#if chromosome is the same, check if the maf coordinates are beyond the coding gene
	#if they are, get the next coding gene, if not, check if they overlap. If they overlap, print
	#the maf entry. If they overlap or the maf is smaller, get the next maf entry
	if maf_line[0]==coding_line[0]:
		if maf_line[1]>coding_line[2]:
			coding_number+=1
			coding_line=coding_summary[coding_number]
		else:
			if maf_line[1]<coding_line[2] and maf_line[2]>coding_line[1]:
				filtered_maf_file.write(chunk_line)
				total_coders.add(coding_line[3])
			chunk_line, maf_line=advance_chunk(chunk_file)
	#if the chromosomes don't overlap get the next line from the smaller chromosome
	elif maf_line[0]>coding_line[0]:
		coding_number+=1
		coding_line=coding_summary[coding_number]
	elif maf_line[0]<coding_line[0]:
		chunk_line, maf_line=advance_chunk(chunk_file)

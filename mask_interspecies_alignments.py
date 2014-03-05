#this program takes a summarized maf file, reports
#locations in the human genome that align to multiple maf
#alignments as a mask, and removes human genes that overlap
#with these locations from analysis

def try_next(test_list, current_number):
	current_number+=1
	try:
		out_line=test_list[current_number]
		return out_line, current_number
	except IndexError:
		return '', current_number

def get_overlappers (list1, list2):
	#goes through every element of two lists of the 
	#form chrom, start, end, and returns elements
	#with overlap. Only overlappers to list1 are exhaustive
	list1.sort()
	list2.sort()
	list1_number, list2_number, chrom, start, end, outlist1, outlist2=0,0,0,1,2,[],[]
	one_line, two_line=list1[list1_number], list2[list2_number]
	while list1_number<len(list1) and list2_number<len(list2):
		if one_line[chrom]==two_line[chrom]:
			if one_line[start]>two_line[end]:
				two_line, list2_number=try_next(list2, list2_number)
			elif two_line[start]>one_line[end]:
				one_line, list1_number=try_next(list1, list1_number)
			else:
				outlist1.append(one_line)
				outlist2.append(two_line)
				two_line, list2_number=try_next(list2, list2_number)
		elif one_line[chrom]>two_line[chrom]:
			two_line, list2_number=try_next(list2, list2_number)
		elif two_line[chrom]>one_line[chrom]:
			one_line, list1_number=try_next(list1, list1_number)
	return outlist1, outlist2

def condense_overlappers(sorted_chunks):
	print 'starting'
	mask_list=[]
	sorted_chunks.sort()
	mask_check=sorted_chunks[0]
	for coord_number, smaller in enumerate(sorted_chunks[:-1]):
		bigger=sorted_chunks[coord_number+1]
		if mask_check[0]==bigger[0]:
			if mask_check[2]>=bigger[1]:
				if bigger[2]>mask_check[2]:
					mask_check[2]=bigger[2]
					mask_list.append(mask_check)
			else:
				mask_list.append(mask_check)
				mask_check=bigger
		else:
			mask_list.append(mask_check)
			mask_check=bigger
	mask_list.append(bigger)
	mask_list.sort()
	print 'finishing'
	return mask_list

#this definition sorts a list of coordinate sets (primarily
#by the smaller coordinate). If the smaller coordinate set
#overlaps the larger coordinate set, the overlapping 
#portion is appended to a mask and the two sets are merged
#to form the basis of the next search. Otherwise the
#larger coordinate set becomes the basis of the smaller set
def find_overlappers(sorted_chunks):
	mask_list=[]
	sorted_chunks.sort()
	mask_check=sorted_chunks[0]
	for coord_number, smaller in enumerate(sorted_chunks[:-1]):
		bigger=sorted_chunks[coord_number+1]
		if mask_check[0]==bigger[0]:
			if mask_check[2]>bigger[1]:
				if bigger[2]>mask_check[2]:
					mask_item=[mask_check[0], bigger[1], mask_check[2]]
					mask_check[2]=bigger[2]
				else:
					mask_item=bigger
				mask_list.append(mask_item)
			else:
				mask_check=bigger
		else:
			mask_check=bigger
	return mask_list

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
	try:
		maf_summary=chunk_line.split(']], [[')[1].split(', ')
		maf_summary[0]=maf_summary[0][1:-1]
		maf_summary[1:]=[int(value) for value in maf_summary[1:]]
		return chunk_line, maf_summary
	except IndexError:
		return chunk_line, ''
output_file=open('nonduplicated', 'w')
coding_list=open('putatively_filtered_coding_genes').readlines()
coding_dict, coding_summary_list, sorted_chunks={}, [], []
for line in coding_list:
	split_line=line.strip().split('\t')
	coding_summary_list.append(get_human_boundaries(split_line))
	if split_line[0] not in coding_dict:
		coding_dict[split_line[0]]=line
	else:
		print 'duplicate', split_line[0]
coding_summary_list.sort()

chunk_file=open('indexed_all_chunks_sorted')
chunk_line, maf_summary=advance_chunk(chunk_file)
thing_number=0
while chunk_line:
	if thing_number%100000==0:
		print thing_number
	sorted_chunks.append(maf_summary)
	chunk_line, maf_summary=advance_chunk(chunk_file)
	thing_number+=1
sorted_mask=find_overlappers(sorted_chunks)
new_length=len(sorted_mask)
old_length='b'
while new_length<old_length:
	print new_length, old_length
	sorted_mask=condense_overlappers(sorted_mask)
	old_length=new_length
	new_length=len(sorted_mask)
junk_mask, filtered_coding_list=get_overlappers(sorted_mask, coding_summary_list)
filtered_coding_list=[line[3] for line in filtered_coding_list]
for line in coding_list:
	gene=line.split('\t')[0]
	if gene not in filtered_coding_list:
		output_file.write(line)

input_list=[line.strip().split('\t') for line in open('nonduplicated')]
minimum=9000000
maximum=0
for line in input_list:
	starts=line[5].split(',')
	ends=line[6].split(',')
	length=0
	for start_number, start in enumerate(starts):
		length=length+(int(ends[start_number])-int(start))
	if length>maximum:
		maximum=length
		maximum_gene=line[0]
	if length<minimum:
		minimum=length
		minimum_gene=line[0]
print maximum_gene, maximum
print minimum_gene, minimum

gene_list=[line.strip().split('\t') for line in open('human_refseq_all')]

def extract_boundaries(gene):
	genomic_start, genomic_end=int(gene[1]), int(gene[2])
	strand, coding_start, coding_end=gene[5], int(gene[6]), int(gene[7])
	gene_name, gene_chrom, UTR_3_coords=gene[3], gene[0], []
	if 'hap' not in gene_chrom and coding_start<coding_end:
		starts_list=[int(start)+genomic_start for start in gene[11].split(',')[:-1]]
		lengths_list=[int(length) for length in gene[10].split(',')[:-1]]
		for start_number, start in enumerate(starts_list):
			end=start+lengths_list[start_number]
			if end>coding_start and start<coding_start:
				if strand=='-':
					UTR_3_coords.append([start, coding_start])
			if end>coding_end and start<coding_end:
				if strand=='+':
					UTR_3_coords.append([coding_end, end])
			if (end<=coding_start and strand=='-') or (start>=coding_end and strand=='+'):
				UTR_3_coords.append([start, end])
		return [gene_name, UTR_3_coords]

unique_set, non_unique_set, gene_dict=set([]), set([]), {}

for gene in gene_list:
	try:
		returned_gene, returned_UTR=extract_boundaries(gene)
		if returned_gene not in gene_dict:
			gene_dict[returned_gene]=[]
		gene_dict[returned_gene].append(returned_UTR)
		if returned_gene=='NM_178491':
			print returned_gene
			print gene_dict[returned_gene]
	except TypeError:
		pass
for gene in gene_dict:
	if len(gene_dict[gene])==1 and len(gene_dict[gene][0])==1:
		pass
#		print gene

import sys
import custom
data_folder, refseq_input_bed, refseq_input_fasta=sys.argv[1:]
BED_gene_list=[line.strip().split('\t') for line in open(sys.argv[1]+sys.argv[2])]
fasta_gene_list=custom.read_fasta(sys.argv[1]+sys.argv[3])
def extract_boundaries(gene):
	gene_length=0
	genomic_start, genomic_end=gene[1:3]
	strand, coding_start, coding_end=gene[5:8]
	has_UTR, coding_coords, UTR_5_coords, UTR_3_coords=0, [], [], []
	gene_name, gene_chrom=gene[3], gene[0]
	if coding_end>coding_start:
		if strand=='-' and genomic_start<coding_start:
			has_UTR='yes'
		if strand=='+' and genomic_end>coding_end:
			has_UTR='yes'
	if has_UTR and 'hap' not in gene_chrom and coding_end>coding_start:
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
			gene_length+=(end-start)
	return [gene_name, gene_chrom, strand, UTR_3_coords, gene_length]

def convert_to_int(str_list):
	for string_number, string in enumerate(str_list):
		try:
			str_list[string_number]=int(str_list[string_number])
		except ValueError:
			pass
	return str_list

unique_set, non_unique_set, converted_list, good_genes, filtered_list=set([]), set([]), [], set([]), []

for gene in BED_gene_list:
	gene=convert_to_int(gene)
	gene_attributes=extract_boundaries(gene)
	gene_name, UTR_coords=gene_attributes[0], gene_attributes[3]
	if UTR_coords:
		converted_list.append(gene_attributes)
		if gene_name not in unique_set:
			unique_set.add(gene_name)
		else:
			non_unique_set.add(gene_name)
for fasta_entry in fasta_gene_list:
	if 'hap' not in fasta_entry[0]:
		fasta_entry[0]='_'.join(fasta_entry[0].split(' ')[0].split('_')[-2:])
		fasta_entry[1]=fasta_entry[1].upper()
fasta_gene_dict=dict(fasta_gene_list)

for converted_gene in converted_list:
	gene_name, gene_chrom, strand, UTR_3, gene_length=converted_gene
	if gene_name not in non_unique_set and len(UTR_3)==1:# and len(fasta_gene_dict[gene_name])==gene_length:
		good_genes.add(gene_name)
		filtered_list.append([gene_name, fasta_gene_dict[gene_name]])
print len(good_genes)
custom.print_fasta(filtered_list, sys.argv[1]+sys.argv[3]+'_filtered', 'w')

filtered_bed=open(sys.argv[1]+sys.argv[2]+'_filtered', 'w')
for BED_entry in BED_gene_list:
	if BED_entry[3] in good_genes:
		filtered_bed.write('\t'.join(map(str, BED_entry))+'\n')

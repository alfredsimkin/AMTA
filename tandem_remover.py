import copy
gene_list=[line.strip().split('\t') for line in open('/home/alfred/Downloads/human ensembl')]
dup_list=[line.strip().split('\t')[1:] for line in open('/home/alfred/Downloads/segmental dups')]
dup_list.sort()
gene_list.sort()
new_gene_list=copy.deepcopy(gene_list)
dup_number, gene_number=0,0
tandem_out=open('ensembl_genes_in_tandems', 'w')
non_tandem_out=open('ensembl_genes_not_tandems', 'w')

while dup_number<len(dup_list) and gene_number<len(gene_list):
	dup=dup_list[dup_number]
	gene=gene_list[gene_number]
	if dup[0]<gene[0] or int(dup[2])<int(gene[1]):
		dup_number+=1
	elif dup[0]>gene[0] or int(dup[1])>int(gene[2]):
		gene_number+=1
	else:
		tandem_out.write('\t'.join(gene)+'\n')
		new_gene_list.remove(gene)
		print gene[0]
		gene_number+=1
for line in new_gene_list:
	non_tandem_out.write('\t'.join(line)+'\n')

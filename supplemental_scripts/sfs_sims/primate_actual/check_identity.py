import cPickle
gene_dict=cPickle.load(open('sim_parsimony_dict'))
id_count=0
non_id_count=0
for gene in gene_dict:
	human=gene_dict[gene]['7']
	chimp=gene_dict[gene]['8']
	for pos_number, pos in enumerate(human):
		if chimp[pos_number]==pos:
			id_count+=1
		else:
			non_id_count+=1
print id_count, non_id_count
print float(non_id_count)/(non_id_count+id_count)
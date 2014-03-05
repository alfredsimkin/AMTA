import cPickle
import sys
data_folder=sys.argv[1]
bed_file=sys.argv[2]
gene_set=cPickle.load(open(data_folder+'lastz_species_intersection'))
gene_list=list(gene_set)
gene_set=set(gene_list)
output_file=open(data_folder+bed_file+'filtered_lastz', 'w')
for line in open(data_folder+bed_file+'_filtered'):
	gene_name=line.split('\t')[3]
#	print gene_name
	if gene_name in gene_set:
		output_file.write(line)

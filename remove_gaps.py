import custom
import cPickle
import copy
import sys
data_folder=sys.argv[1]
species_list=eval(sys.argv[2])
input_dict=sys.argv[3]
gene_dict=cPickle.load(open(data_folder+input_dict))
new_dict=copy.deepcopy(gene_dict)
good_set=set(['A', 'C', 'G', 'T', 'a', 'c', 'g', 't'])
for gene in gene_dict:
	unzipped_list=[]
#	print gene_dict[gene]
#	print species_list
	for species in species_list:
#		print gene_dict[gene][species]
		unzipped_list.append(gene_dict[gene][species])
#		species_list.append(species)
	zipped_list=[''.join(char) for char in zip(*unzipped_list)]
	pos_number=0
	while pos_number+1<len(zipped_list):
		reset_pos=False
		if len(set(zipped_list[pos_number])-good_set)>0:
			if len(set(zipped_list[pos_number+1])-good_set)>0:
				del zipped_list[pos_number]
				reset_pos=True
			else:
				zipped_list[pos_number]='N'*len(zipped_list[pos_number])
		if not reset_pos:
			pos_number+=1
	if len(set(zipped_list[-1])-good_set)>0:
		zipped_list[-1]='N'*len(zipped_list[pos_number])
	new_alignment=[''.join(char) for char in zip(*zipped_list)]
#	print new_alignment
#	exit()
	for species_number, species in enumerate(species_list):
		new_dict[gene][species]=new_alignment[species_number]
cPickle.dump(new_dict, open(data_folder+input_dict+'_nogaps', 'w'))

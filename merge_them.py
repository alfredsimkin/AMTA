import sys
import cPickle
species_list=eval(sys.argv[1])
data_folder=sys.argv[2]
old_set=set([])
lastz_out=open(data_folder+'lastz_species_intersection', 'w')
for species_number, species in enumerate(species_list):
	print species
	current_dict=cPickle.load(open(species+'pickled_good_gene_dict'))
	current_set=set(current_dict.keys())
	if species_number==0:
		old_full=current_set
	full_set=old_full&current_set
	print 'before', len(current_set), 'after', len(full_set)
	old_full=full_set
print len(full_set)
cPickle.dump(full_set, lastz_out)

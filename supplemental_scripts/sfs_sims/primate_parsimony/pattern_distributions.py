import cPickle
count_dict={}
full_dict=cPickle.load(open('sim_parsimony_dict'))
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
without_descendants='human', 'chimp', 'gorilla', 'orangutan', 'gibbon'
output_file=open('pattern_list', 'w')
#for gene in full_dict:
#	for species in full_dict[gene]:
#		print species
#		print full_dict[gene][species]

for gene in full_dict:
	all_species=set(full_dict[gene].keys())
	with_descendants=set(descendant_dict.keys())
#	without_descendants=sorted(list(all_species-with_descendants), reverse=True, key=int)	
#	print without_descendants
	for position in range(len(full_dict[gene]['gibbon'])-7):
		mer_dict={}
		for species in without_descendants:
			mer=full_dict[gene][species][position:position+8]
			if 'N' in mer:
				if len(mer_dict)>0:
					print position
					print full_dict[gene]
#					print 'error'
#					exit()
				break
			if mer not in mer_dict:
				mer_dict[mer]=''
		for mer in mer_dict:
			for species in without_descendants:
				if full_dict[gene][species][position:position+8]==mer:
					mer_dict[mer]+='1'
				else:
					mer_dict[mer]+='0'
#			print mer, position, mer_dict[mer]
		for mer in mer_dict:
			if mer_dict[mer] not in count_dict:
				count_dict[mer_dict[mer]]=0
			count_dict[mer_dict[mer]]+=1
#print len(count_dict)
for pattern in count_dict:
	output_file.write(pattern+'\t'+str(count_dict[pattern])+'\n')
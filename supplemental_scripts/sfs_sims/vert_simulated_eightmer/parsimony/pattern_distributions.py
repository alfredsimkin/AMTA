import cPickle
count_dict={}
full_dict=cPickle.load(open('vert_dictionary'))
descendant_dict={'11': ['12', '13'], '10': ['11', '16'], '13': ['14', '15'], '38': ['39', '40'], '21': ['22', '23'], '17': ['18', '21'], '16': ['17', '28'], '33': ['34', '35'], '18': ['19', '20'], '31': ['32', '33'], '23': ['24', '25'], '28': ['29', '36'], '29': ['30', '31'], '36': ['37', '38'], '0': ['1', '2'], '3': ['4', '5'], '2': ['3', '6'], '25': ['26', '27'], '6': ['7', '8'], '8': ['9', '10']}

for gene in full_dict:
	for species in full_dict[gene]:
		print species
		print full_dict[gene][species]

for gene in full_dict:
	all_species=set(full_dict[gene].keys())
	with_descendants=set(descendant_dict.keys())
	without_descendants=sorted(list(all_species-with_descendants), reverse=True, key=int)	
	print without_descendants
	for position in range(len(full_dict[gene]['0'])-7):
		mer_dict={}
		for species in without_descendants:
			mer=full_dict[gene][species][position:position+8]
			if mer not in mer_dict:
				mer_dict[mer]=''
		for mer in mer_dict:
			for species in without_descendants:
				if full_dict[gene][species][position:position+8]==mer:
					mer_dict[mer]+='1'
				else:
					mer_dict[mer]+='0'
			print mer, position, mer_dict[mer]
		for mer in mer_dict:
			if mer_dict[mer] not in count_dict:
				count_dict[mer_dict[mer]]=0
			count_dict[mer_dict[mer]]+=1
print len(count_dict)
for pattern in count_dict:
	print pattern+'\t'+str(count_dict[pattern])

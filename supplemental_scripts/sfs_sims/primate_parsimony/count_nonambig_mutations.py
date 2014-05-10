import cPickle
output_dict, final_dict={}, {}
dict_list=[]
real_list=[line.strip().split() for line in open('pattern_list')]
def get_changes(step_number, pattern, existing_set):
	full_dict=dict_list[step_number-1]
	existing_set=existing_set|set(full_dict[pattern].keys())
	for change in full_dict[pattern]:
		new_pattern=full_dict[pattern][change]
		if step_number!=1:
			existing_set=get_changes(step_number-1, new_pattern, existing_set)
	return existing_set

for number in range(1, 4):
	print 'step is', number
	input_file=open(str(number)+'_step,dict_ambigs')
	full_dict=cPickle.load(input_file)
	print 'loaded pickle'
	dict_list.append(full_dict)
	input_file.close()
for real_pattern in real_list:
	for step_number, step in enumerate(dict_list):
		if real_pattern[0] in step:
			existing_set=get_changes(step_number+1, real_pattern[0], set([]))
			if len(existing_set)==step_number+1:
				mutation_tuple=tuple(sorted(tuple(existing_set)))
				for individual_tuple in mutation_tuple:
					if individual_tuple not in final_dict:
						final_dict[individual_tuple]=0
					final_dict[individual_tuple]+=int(real_pattern[1])
print final_dict

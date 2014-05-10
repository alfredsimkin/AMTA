import custom
import copy
import cPickle
import time
change_coords=((0,1), (1,2), (2,3), (3,4), (4,5), (0,2), (0,3))
patterns=set(custom.count_in_base('00000', 2, '01z'))
patterns.discard('00000')
patterns.discard('11111')
def populate_step(current_step, previous_step_dict, previous_ambig_set, patterns):
	current_step_dict, ambig_set={}, set([])
	patterns_copy=copy.deepcopy(patterns)
	print len(patterns), current_step
	for pattern_number, pattern in enumerate(patterns):
		if pattern_number%200000==0:
			print pattern_number/float(len(patterns))
		for change in change_coords:
			types=set(pattern[change[0]:change[1]])
			if len(types)==1:
				if '1' in types:
					addition=(change[1]-change[0])*'0'
					change_new=change+('g','g')
				elif '0' in types:
					addition=(change[1]-change[0])*'1'
					change_new=change+('l','l')
				new_pattern=pattern[:change[0]]+addition+pattern[change[1]:]
				if current_step==1:
					if len(set(new_pattern))==1:
						if pattern not in current_step_dict:
							current_step_dict[pattern]={}
						current_step_dict[pattern][change_new]=new_pattern
						patterns_copy.discard(pattern)
				elif new_pattern in previous_step_dict:
					if new_pattern in previous_ambig_set:
						ambig_set.add(pattern)
					if pattern not in current_step_dict:
						current_step_dict[pattern]={}
					current_step_dict[pattern][change_new]=new_pattern
					patterns_copy.discard(pattern)
		if pattern in current_step_dict and len(current_step_dict[pattern])>current_step:
			ambig_set.add(pattern)
	return current_step_dict, ambig_set, patterns_copy
def print_to_pickle(step_number, step_dict, ambig_set):
	pickle_file=open(str(step_number)+'_step,dict_ambigs', 'w')
	cPickle.dump(step_dict, pickle_file)
	cPickle.dump(ambig_set, pickle_file)

step_dict=None
step_number=1
ambig_set=set([])
while step_number<2 or len(step_dict)>0:
	step_dict, ambig_set, patterns=populate_step(step_number, step_dict, ambig_set, patterns)
	print 'full len is\n', len(step_dict.keys()), '\n ambigs are\n', len(ambig_set)
	print_to_pickle(step_number, step_dict, ambig_set)
	step_number+=1

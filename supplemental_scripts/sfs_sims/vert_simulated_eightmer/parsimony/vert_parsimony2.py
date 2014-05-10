import custom
import copy
import cPickle
import time
change_coords=((0,2), (0,3), (3,5), (3,6), (3,7), (0,7), (7,9), (7,10), (7,11), (11,13), (7,13), (0,13), (13,15), (13,16), (0,16), (0,17), (0,18), (18,20), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21))
patterns=set(custom.count_in_base('000000000000000000000', 2, '01z'))
patterns.discard('000000000000000000000')
patterns.discard('111111111111111111111')
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
while step_number<12:
	step_dict, ambig_set, patterns=populate_step(step_number, step_dict, ambig_set, patterns)
	print 'full len is\n', len(step_dict.keys()), '\n ambigs are\n', len(ambig_set)
	print_to_pickle(step_number, step_dict, ambig_set)
	step_number+=1

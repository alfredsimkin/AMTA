import cPickle
import custom
import copy

def list_one_offers(mirseed):
	one_off_list=[]
	choices='ACGT'
	for pos in range(len(mirseed)):
		for choice in choices:
			if choice!=mirseed[pos]:
				one_off_list.append(mirseed[:pos]+choice+mirseed[pos+1:])
	return one_off_list

def end_probs(prob_dict):
	dinucleotides=custom.count_in_base('AA', 4, 'ACGTz')
	choices='ACGT'
	empty_dict={}
	for anc in choices:
		if anc not in empty_dict:
			empty_dict[anc]={}
		for desc in choices:
			if desc not in empty_dict[anc]:
				empty_dict[anc][desc]={'left':[], 'right':[]}
	end_probs=copy.deepcopy(empty_dict)
	for ancestor in dinucleotides:
		end_dict=copy.deepcopy(empty_dict)
		for descendant in dinucleotides:
			if ancestor[0]==descendant[0] or ancestor[1]==descendant[1]:
				end_dict[ancestor[1]][descendant[1]]['left'].append(prob_dict[ancestor][descendant])
				end_dict[ancestor[0]][descendant[0]]['right'].append(prob_dict[ancestor][descendant])
		for ancestor_letter in end_dict:
			for descendant_letter in end_dict[ancestor_letter]:
				for side in end_dict[ancestor_letter][descendant_letter]:
					if len(end_dict[ancestor_letter][descendant_letter][side])>=1:
						end_probs[ancestor_letter][descendant_letter][side].append(sum(end_dict[ancestor_letter][descendant_letter][side]))
	for ancestor_letter in end_probs:
		for descendant_letter in end_probs[ancestor_letter]:
			for side in end_probs[ancestor_letter][descendant_letter]:
				current_list=end_probs[ancestor_letter][descendant_letter][side]
				end_probs[ancestor_letter][descendant_letter][side]=sum(current_list)/len(current_list)
	return end_probs

def eightmer_prob(ancestor, descendant, prob_dict, end_dict):
	unchangers, changers=1.0, []
	change_prob=0.0
	if ancestor[0]!=descendant[0]:
		changers.append(end_dict[ancestor[0]][descendant[0]]['left']*prob_dict[ancestor[0:2]][ancestor[0:2]])
		changers.append(end_dict[ancestor[0]][ancestor[0]]['left']*prob_dict[ancestor[0:2]][descendant[0:2]])
	else:
		unchangers=unchangers*end_dict[ancestor[0]][descendant[0]]['left']
	for start in range(len(ancestor)-2):
		ancestor_di=ancestor[start:start+2]
		descendant_di=descendant[start:start+2]
		next_ancestor=ancestor[start+1:start+3]
		next_descendant=descendant[start+1:start+3]
		if ancestor_di[1]!=descendant_di[1]:
			changers.append(prob_dict[ancestor_di][descendant_di]*prob_dict[next_ancestor][next_ancestor])
			changers.append(prob_dict[ancestor_di][ancestor_di]*prob_dict[next_ancestor][next_descendant])
		elif ancestor_di==descendant_di:
			unchangers=unchangers*prob_dict[ancestor_di][ancestor_di]
	if ancestor[-2:]==descendant[-2:]:
		unchangers=unchangers*prob_dict[ancestor[-2:]][descendant[-2:]]
	if ancestor[-1]!=descendant[-1]:
		changers.append(end_dict[ancestor[-1]][descendant[-1]]['right']*prob_dict[ancestor[-2:]][ancestor[-2:]])
		changers.append(end_dict[ancestor[-1]][ancestor[-1]]['right']*prob_dict[ancestor[-2:]][descendant[-2:]])

	else:
		unchangers=unchangers*end_dict[ancestor[-1]][descendant[-1]]['right']
	for changer in changers:
		change_prob=change_prob+changer*unchangers
	return change_prob

def calculate_final_probability(ancestor, descendant, final_probs, prob_dict, end_dict):
	three_number_dict={}
	three_number_summaries=[line.strip().split() for line in open('quick_out')]
	for line in three_number_summaries:
		if line[1] not in three_number_dict:
			three_number_dict[line[1]]={}
		three_number_dict[line[1]][line[0]]=line[2:]	
	eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
	for eightmer in eightmer_list:
		if eightmer not in final_probs[ancestor][descendant]:
			final_probs[ancestor][descendant][eightmer]=[[], [0.0]]
	for eightmer in eightmer_list:
		one_offer_list=list_one_offers(eightmer)
		for one_offer in one_offer_list:
			change_prob=(eightmer_prob(eightmer, one_offer, prob_dict, end_dict))/2
			final_probs[ancestor][descendant][eightmer][1][0]+=change_prob
			final_probs[ancestor][descendant][one_offer][0].append([change_prob, int(three_number_dict[ancestor][eightmer][0])])
		final_probs[ancestor][descendant][eightmer][1].append(int(three_number_dict[ancestor][eightmer][0]))
	for eightmer in eightmer_list:
		expected_gains, gain_substrates=0, 0
		for gain_pair in final_probs[ancestor][descendant][eightmer][0]:
			expected_gains+=gain_pair[0]*gain_pair[1]
			gain_substrates+=gain_pair[1]
		avg_gain_prob=expected_gains/gain_substrates
		gain_pair=map(str, [avg_gain_prob, gain_substrates])
		loss_pair=final_probs[ancestor][descendant][eightmer][1]
		expected_gains=str(expected_gains)
		expected_losses=str(loss_pair[0]*loss_pair[1])
		loss_pair=map(str, loss_pair)
		output_file.write(eightmer+'\t'+'\t'.join(three_number_dict[descendant][eightmer][1:]))
		output_file.write('\t'+expected_gains+'\t'+expected_losses+'\t')
		output_file.write('\t'.join(gain_pair)+'\t'+'\t'.join(loss_pair)+'\n')

ancestor_dict={'human':'3', 'chimp':'3', '3':'2', 'gorilla':'2', '2':'1', 'orangutan':'1', 'gibbon':'1'}
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
gene_dict=cPickle.load(open('final_utr_dictionary_nogaps'))
species_list=['3', '2', '1']
good_list=['A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
probability_dict={}
dinucleotides=custom.count_in_base('AA', 4, 'ACGTz')
prob_dict, final_probs={}, {}
for ancestor_di in dinucleotides:
	prob_dict[ancestor_di]={}
	for descendant_di in dinucleotides:
		prob_dict[ancestor_di][descendant_di]=0.0
for ancestor in species_list:
	if ancestor not in final_probs:
		final_probs[ancestor]={}
	descendants=descendant_dict[ancestor]
	for descendant in descendants:
		if descendant not in final_probs[ancestor]:
			final_probs[ancestor][descendant]={}
		mutation_dict={}
		for gene in gene_dict:
			for letter_number, junk in enumerate(gene_dict[gene][ancestor][:-1]):
				ancestor_di=gene_dict[gene][ancestor][letter_number:letter_number+2].upper()
				descendant_di=gene_dict[gene][descendant][letter_number:letter_number+2].upper()
				if ancestor_di[0] in good_list and ancestor_di[1] in good_list and descendant_di[0] in good_list and descendant_di[1] in good_list:
					if ancestor_di not in mutation_dict:
						mutation_dict[ancestor_di]={}
					if descendant_di not in mutation_dict[ancestor_di]:
						mutation_dict[ancestor_di][descendant_di]=0
					mutation_dict[ancestor_di][descendant_di]+=1
		print ancestor, descendant
		output_file=open('full_probs'+ancestor+descendant, 'w')
		output_file.write('eightmer\tgains\tlosses\texp_gains\texp_losses\tgain_prob\tgain_flips\tloss_prob\tloss_flips\n')
		for ancestor_di in sorted(mutation_dict.keys()):
			total_events=0
			for descendant_di in mutation_dict[ancestor_di]:
				total_events+=mutation_dict[ancestor_di][descendant_di]
			for descendant_di in sorted(mutation_dict[ancestor_di]):
				prob_dict[ancestor_di][descendant_di]=float(mutation_dict[ancestor_di][descendant_di])/total_events
		end_dict=end_probs(prob_dict)
		calculate_final_probability(ancestor, descendant, final_probs, prob_dict, end_dict)

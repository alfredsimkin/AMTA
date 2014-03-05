import cPickle
import custom
import copy
ancestor_dict={'human':'3', 'chimp':'3', '3':'2', 'gorilla':'2', '2':'1', 'orangutan':'1', 'gibbon':'1'}
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
gene_dict=cPickle.load(open('final_utr_dictionary_nogaps'))
species_list=['3', '2', '1']
good_list=['A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
dinucleotides=custom.count_in_base('AA', 4, 'ACGTz')
probability_dict={}

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
		print 'N'+ancestor[0], 'N'+descendant[0], end_dict[ancestor[0]][descendant[0]]['left'], ancestor[0:2], ancestor[0:2], prob_dict[ancestor[0:2]][ancestor[0:2]]
		print 'N'+ancestor[0], 'N'+ancestor[0], end_dict[ancestor[0]][ancestor[0]]['left'], ancestor[0:2], descendant[0:2], prob_dict[ancestor[0:2]][descendant[0:2]]
	else:
		unchangers=unchangers*end_dict[ancestor[0]][descendant[0]]['left']
		print 'N'+ancestor[0], 'N'+descendant[0], end_dict[ancestor[0]][descendant[0]]['left']
	for start in range(len(ancestor)-2):
		ancestor_di=ancestor[start:start+2]
		descendant_di=descendant[start:start+2]
		next_ancestor=ancestor[start+1:start+3]
		next_descendant=descendant[start+1:start+3]
		if ancestor_di[1]!=descendant_di[1]:
			changers.append(prob_dict[ancestor_di][descendant_di]*prob_dict[next_ancestor][next_ancestor])
			changers.append(prob_dict[ancestor_di][ancestor_di]*prob_dict[next_ancestor][next_descendant])
			print ancestor_di, descendant_di, prob_dict[ancestor_di][descendant_di], 'and', next_ancestor, next_ancestor, prob_dict[next_ancestor][next_ancestor], 'or'
			print ancestor_di, ancestor_di, prob_dict[ancestor_di][ancestor_di], next_ancestor, next_descendant, prob_dict[next_ancestor][next_descendant]
		elif ancestor_di==descendant_di:
			unchangers=unchangers*prob_dict[ancestor_di][ancestor_di]
			print ancestor_di, descendant_di, prob_dict[ancestor_di][ancestor_di]
	if ancestor[-2:]==descendant[-2:]:
		unchangers=unchangers*prob_dict[ancestor[-2:]][descendant[-2:]]
		print ancestor[-2:], descendant[-2:], prob_dict[ancestor[-2:]][descendant[-2:]]
	if ancestor[-1]!=descendant[-1]:
		changers.append(end_dict[ancestor[-1]][descendant[-1]]['right']*prob_dict[ancestor[-2:]][ancestor[-2:]])
		changers.append(end_dict[ancestor[-1]][ancestor[-1]]['right']*prob_dict[ancestor[-2:]][descendant[-2:]])
		print ancestor[-2:], ancestor[-2:], prob_dict[ancestor[-2:]][ancestor[-2:]], ancestor[-1]+'N', descendant[-1]+'N', end_dict[ancestor[-1]][descendant[-1]]['right']
		print ancestor[-2:], descendant[-2:], prob_dict[ancestor[-2:]][descendant[-2:]], ancestor[-1]+'N', ancestor[-1]+'N', end_dict[ancestor[-1]][ancestor[-1]]['right']

	else:
		unchangers=unchangers*end_dict[ancestor[-1]][descendant[-1]]['right']
		print ancestor[-1]+'N', descendant[-1]+'N', end_dict[ancestor[-1]][descendant[-1]]['right']
	for changer in changers:
		change_prob=change_prob+changer*unchangers
	return change_prob

dinucleotides=custom.count_in_base('AA', 4, 'ACGTz')
prob_dict, final_probs={}, {}

for ancestor_di in dinucleotides:
	prob_dict[ancestor_di]={}
	for descendant_di in dinucleotides:
		prob_dict[ancestor_di][descendant_di]=0.0
for species in species_list:
	if species not in final_probs:
		final_probs[species]={}
	descendants=descendant_dict[species]
	for descendant in descendants:
		if descendant not in final_probs[species]:
			final_probs[species][descendant]={}
		mutation_dict={}
		for gene in gene_dict:
			for letter_number, junk in enumerate(gene_dict[gene][species][:-1]):
				ancestor_di=gene_dict[gene][species][letter_number:letter_number+2].upper()
				descendant_di=gene_dict[gene][descendant][letter_number:letter_number+2].upper()
				if ancestor_di[0] in good_list and ancestor_di[1] in good_list and descendant_di[0] in good_list and descendant_di[1] in good_list:
					if ancestor_di not in mutation_dict:
						mutation_dict[ancestor_di]={}
					if descendant_di not in mutation_dict[ancestor_di]:
						mutation_dict[ancestor_di][descendant_di]=0
					mutation_dict[ancestor_di][descendant_di]+=1
		print species, descendant
		for ancestor_di in sorted(mutation_dict.keys()):
			total_events=0
			for descendant_di in mutation_dict[ancestor_di]:
				total_events+=mutation_dict[ancestor_di][descendant_di]
			for descendant_di in sorted(mutation_dict[ancestor_di]):
				prob_dict[ancestor_di][descendant_di]=float(mutation_dict[ancestor_di][descendant_di])/total_events
				print ancestor_di, descendant_di, str(mutation_dict[ancestor_di][descendant_di])+'/'+str(total_events), prob_dict[ancestor_di][descendant_di]
		end_dict=end_probs(prob_dict)
		eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
		for eightmer in eightmer_list:
			if eightmer not in final_probs[species][descendant]:
				final_probs[species][descendant][eightmer]=[[], 0.0]
#		for eightmer in eightmer_list:
		demo_list=['ACCAAAGA']
		demo_list.extend(list_one_offers('ACCAAAGA'))
		for eightmer in demo_list:
			one_offer_list=list_one_offers(eightmer)
			for one_offer in one_offer_list:
				print eightmer, one_offer
				change_prob=eightmer_prob(eightmer, one_offer, prob_dict, end_dict)
				final_probs[species][descendant][one_offer][0].append(change_prob)
				final_probs[species][descendant][eightmer][1]+=change_prob
				print 'total prob of', eightmer, 'becoming', one_offer, 'is', change_prob, '\n\n'
		for eightmer in final_probs[species][descendant]:
			final_probs[species][descendant][eightmer][0]=sorted(final_probs[species][descendant][eightmer][0])
		print final_probs[species][descendant]['ACCAAAGA']
#		print final_probs
		exit()
		

#			find empirical probabilities of every dinucleotide change
#			print any dinucleotides with multiple mutations
#		normalize each change probability by sum across each starting dinucleotide
#		for eightmer in current ancestor:
#			look at ancestors eightmer, descendants eightmer
#			print eightmers with multiple mutations
#			make list of possible one step away sequences (24 of these)
#			for one_step_away in one_step_away_list:
#				calculate p of 8 non-changing dinucleotides with the emprical probabilities and one changing dinucleotide
#				Do this again, allowing the other dinucleotide containing the changing base to vary instead. 
#				Add the two p values.
#				add summed p-value to losing ancestor list and to gaining descendant list
#	for eightmer in eightmerlist:
#		calculate expected number of gains and losses (sum of gain and loss p-values)
#		compare to actual number of gains and losses
#		find minimum probability
#		find maximum probability
#		calculate prob of same or more gains, same or more losses
#		calculate prob of same or fewer gains, same or fewer losses
#		do again with max or min probability
#	full_probs.append(current_eightmer)

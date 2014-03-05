import cPickle
import copy

ancestor_dict={'human':'3', 'chimp':'3', '3':'2', 'gorilla':'2', '2':'1', 'orangutan':'1', 'gibbon':'1'}
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
good_set=set(['A','C','G','T','a','c','g','t'])
output_string='full_9mer_counts_new_single_Ns'
full_dict=cPickle.load(open('final_utr_dictionary_nogaps_single_Ns'))
#full_dict=cPickle.load(open('NM_001080825'))
output_dict={}
count, outnumber=0,0
for gene in full_dict:
	print gene, count
	count+=1
#	for species in full_dict[gene]:
#		print species, full_dict[gene][species]
	output_dict[gene]={'human':{}, 'gibbon':{}, 'chimp':{}, 'gorilla':{}, 'orangutan':{}, '3':{}, '2':{}, '1':{}}
	for species in full_dict[gene]:
		for basepair in range(len(full_dict[gene]['1'])-8):
			position, ninemer=0, ''
			sequence=full_dict[gene][species][basepair:]
			while len(ninemer)<9 and position<len(sequence):
				if ninemer=='' or sequence[position]!='-':
					if sequence[position] not in good_set:
						break
					ninemer=ninemer+sequence[position]
				position+=1
			if len(ninemer)==9:
				ninemer=ninemer.upper()
#				print output_dict['NM_001080825']
				if ninemer not in output_dict[gene][species]:
					output_dict[gene][species][ninemer]=[0,0,0]
				output_dict[gene][species][ninemer][0]+=1
				start, end=basepair, basepair+position
				try:
					ancestor=ancestor_dict[species]
					if full_dict[gene][ancestor][start:end].upper()!=ninemer:
						output_dict[gene][species][ninemer][1]+=1
				except KeyError:
					pass
				try:
					descendants=descendant_dict[species]
				except KeyError:
					descendants=[]
				for descendant in descendants:
					if full_dict[gene][descendant][start:end].upper()!=ninemer:
						if ninemer not in output_dict[gene][descendant]:
							output_dict[gene][descendant][ninemer]=[0,0,0]
						output_dict[gene][descendant][ninemer][2]+=1
	if count%25==0:
		outnumber+=1
		cPickle.dump(output_dict, open(output_string+str(outnumber), 'w'))
		output_dict={}
if count%25!=0:
	outnumber+=1
	cPickle.dump(output_dict, open(output_string+str(outnumber), 'w'))

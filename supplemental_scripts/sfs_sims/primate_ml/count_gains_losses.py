import cPickle
import copy

ancestor_dict={'human':'3', 'chimp':'3', '3':'2', 'gorilla':'2', '2':'1', 'orangutan':'1', 'gibbon':'1'}
descendant_dict={'1':['gibbon', 'orangutan', '2'], '2':['3', 'gorilla'], '3':['chimp', 'human']}
good_set=set(['A','C','G','T','a','c','g','t'])
output_string='sim_ml_output_values'
full_dict=cPickle.load(open('sim_ml_output_dict'))
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
		for basepair in range(len(full_dict[gene]['1'])-7):
			position, eightmer=0, ''
			sequence=full_dict[gene][species][basepair:]
			while len(eightmer)<8 and position<len(sequence):
				if eightmer=='' or sequence[position]!='-':
					if sequence[position] not in good_set:
						break
					eightmer=eightmer+sequence[position]
				position+=1
			if len(eightmer)==8:
				eightmer=eightmer.upper()
#				print output_dict['NM_001080825']
				if eightmer not in output_dict[gene][species]:
					output_dict[gene][species][eightmer]=[0,0,0]
				output_dict[gene][species][eightmer][0]+=1
				start, end=basepair, basepair+position
				try:
					ancestor=ancestor_dict[species]
					if full_dict[gene][ancestor][start:end].upper()!=eightmer:
						output_dict[gene][species][eightmer][1]+=1
				except KeyError:
					pass
				try:
					descendants=descendant_dict[species]
				except KeyError:
					descendants=[]
				for descendant in descendants:
					if full_dict[gene][descendant][start:end].upper()!=eightmer:
						if eightmer not in output_dict[gene][descendant]:
							output_dict[gene][descendant][eightmer]=[0,0,0]
						output_dict[gene][descendant][eightmer][2]+=1
	if count%100==0:
		outnumber+=1
		cPickle.dump(output_dict, open(output_string+str(outnumber), 'w'))
		output_dict={}
if count%100!=0:
	outnumber+=1
	cPickle.dump(output_dict, open(output_string+str(outnumber), 'w'))

#	for species in output_dict[gene]:
#		print species, output_dict[gene][species]
#	exit()


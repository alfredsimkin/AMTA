import cPickle
import copy

ancestor_dict={'24': '23', '25': '23', '26': '25', '27': '25', '20': '18', '21': '17', '22': '21', '23': '21', '28': '16', '29': '28', '40': '38', '1': '0', '3': '2', '2': '0', '5': '3', '4': '3', '7': '6', '6': '2', '9': '8', '8': '6', '39': '38', '38': '36', '11': '10', '10': '8', '13': '11', '12': '11', '15': '13', '14': '13', '17': '16', '16': '10', '19': '18', '18': '17', '31': '29', '30': '29', '37': '36', '36': '28', '35': '33', '34': '33', '33': '31', '32': '31'}
descendant_dict={'11': ['12', '13'], '10': ['11', '16'], '13': ['14', '15'], '38': ['39', '40'], '21': ['22', '23'], '17': ['18', '21'], '16': ['17', '28'], '33': ['34', '35'], '18': ['19', '20'], '31': ['32', '33'], '23': ['24', '25'], '28': ['29', '36'], '29': ['30', '31'], '36': ['37', '38'], '0': ['1', '2'], '3': ['4', '5'], '2': ['3', '6'], '25': ['26', '27'], '6': ['7', '8'], '8': ['9', '10']}
good_set=set(['A','C','G','T','a','c','g','t'])
output_string='full_8mer_counts'
full_dict=cPickle.load(open('vert_dictionary'))
#full_dict=cPickle.load(open('NM_001080825'))
output_dict={}
count, outnumber=0,0
for gene in full_dict:
	print gene, count
	count+=1
#	for species in full_dict[gene]:
#		print species, full_dict[gene][species]
	output_dict[gene]={'0':{}, '1':{}, '2':{}, '3':{}, '4':{}, '5':{}, '6':{}, '7':{}, '8':{}, '9':{}, '10':{}, '11':{}, '12':{}, '13':{}, '14':{}, '15':{}, '16':{}, '17':{}, '18':{}, '19':{}, '20':{}, '21':{}, '22':{}, '23':{}, '24':{}, '25':{}, '26':{}, '27':{}, '28':{}, '29':{}, '30':{}, '31':{}, '32':{}, '33':{}, '34':{}, '35':{}, '36':{}, '37':{}, '38':{}, '39':{}, '40':{}}
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


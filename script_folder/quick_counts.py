#import cPickle
#eightmer_dict=cPickle.load(open('distributions_by_eightmer'))
#for eightmer in eightmer_dict:
#	for species in eightmer_dict[eightmer]:
#		total_sum, gain_sum, loss_sum=0,0,0
#		for dist in eightmer_dict[eightmer][species]:
#			count=eightmer_dict[eightmer][species][dist]
#			values=eval(dist)
#			values=map(int, values)
#			total_sites, total_gains, total_losses=values[0]*count, values[1]*count, values[2]*count
#			total_sum+=total_sites
#			gain_sum+=total_gains
#			loss_sum+=total_losses
#		print eightmer, species, total_sum, gain_sum, loss_sum
inlist=[line.strip().split() for line in open('quick_out')]
eightmer_dict={}
for line in inlist:
	eightmer, species=line[:2]
	total, gain, loss=map(int, line[2:])
	if eightmer not in eightmer_dict:
		eightmer_dict[eightmer]=[0,0,0]
	eightmer_dict[eightmer]=[eightmer_dict[eightmer][summary_number]+summary for summary_number, summary in enumerate([total, gain, loss])]

for eightmer in eightmer_dict:
	if eightmer_dict[eightmer][2]>0:
		print eightmer, float(eightmer_dict[eightmer][1])/eightmer_dict[eightmer][2]
	else:
		print eightmer, 'no losses'

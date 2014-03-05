#output stored as 'final_probs'
name_list=['full_probs3chimp', 'full_probs3human', 'full_probs23', 'full_probs2gorilla', 'full_probs1gibbon', 'full_probs1orangutan', 'full_probs12']
import custom
from scipy.stats import binom
eightmer_list=custom.count_in_base('AAAAAAAA', 4, 'ACGTz')
eightmer_dict={}
for file_name in name_list:
	if file_name[10:] not in eightmer_dict:
		eightmer_dict[file_name[10:]]={}
for file_name in name_list:
	for line in open(file_name):
		line=line.strip().split('\t')
		if line[0]!='eightmer':
			eightmer_dict[file_name[10:]][line[0]]=line

for eightmer in eightmer_list:
	sums=[0,0,0,0,0,0,0,0]
	for file_name in name_list:
		line_list=map(float, eightmer_dict[file_name[10:]][eightmer][1:])
		sums=[sums+values for sums, values in zip(sums, line_list)]
	if sums[5]>0:
		sums[4]=sums[2]/sums[5] 
	else:
		sums[4]=0.0
	if sums[7]>0:
		sums[6]=sums[3]/sums[7]
	else:
		sums[6]=0.0
	gain_prob=binom.cdf(sums[0], sums[5], sums[4])
	loss_prob=binom.cdf(sums[1], sums[7], sums[6])
	sums=map(str, sums)
	print eightmer+'\t'+str(gain_prob)+'\t'+str(loss_prob)+'\t'+'\t'.join(sums)
#	print eightmer, sums

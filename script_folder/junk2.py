final_probs=[line.strip().split() for line in open('final_probs')]
real_eightmers=[line.strip().split() for line in open('real_eightmers')]


for line in final_probs:
	for eightmer in real_eightmers:
		if line[0]==eightmer[-1]:
			print '\t'.join(line)+'\t'+'\t'.join(eightmer[:-1])

full_file=open('gorilla_test', 'w')
real_file=open('real_gorilla_test', 'w')
real_list=[line.split()[0] for line in open('real_gain_loss_by_total')]
inlist=[line.strip().split() for line in open('quick_out')]
eightmer_dict={}
for line in inlist:
	eightmer, species=line[:2]
	current_summary=map(int, line[2:])
	if eightmer not in eightmer_dict:
		eightmer_dict[eightmer]={}	
	eightmer_dict[eightmer][species]=current_summary
for eightmer in eightmer_dict:
	outlist=eightmer_dict[eightmer]['gorilla']
	print eightmer, outlist
	full_file.write(eightmer+' '+' '.join(map(str, outlist))+' ')
	if eightmer in real_list:
		real_file.write(eightmer+' '+' '.join(map(str, outlist))+' ')
	if outlist[0]>0:
		full_file.write(str(float(outlist[1])/outlist[0])+' '+str(float(outlist[2])/outlist[0])+'\n')
		if eightmer in real_list:
			real_file.write(str(float(outlist[1])/outlist[0])+' '+str(float(outlist[2])/outlist[0])+'\n')
	else:
		full_file.write('0 0\n')
		if eightmer in real_list:
			real_file.write('0 0\n')

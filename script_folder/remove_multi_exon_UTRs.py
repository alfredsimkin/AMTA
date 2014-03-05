for line in open('human_refseq_converted_coords'):
	line=line.strip()
	UTR_3list=line.split('\t')[8].split(',')
	if len(UTR_3list)==1:
		print line

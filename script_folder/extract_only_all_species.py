import sys
data_folder=sys.argv[1]
maf_input=sys.argv[2]
maf_species=sys.argv[3]
maf_file=open((data_folder+maf_input)[:-4]+'_trimmed.maf')
output_file=open(data_folder+'all_species_exactly_once.maf', 'w')
for byte_count in open(data_folder+'exactly_once_byte_counts'):
	outlist=[]
	for species in maf_species:
		outlist.append([])
	byte_count=int(byte_count.strip())
	maf_file.seek(byte_count)
	line=maf_file.readline()
	while line.strip():
		line=maf_file.readline().split()
		if line[1] in maf_species:
			position=maf_species.index(line[1])
			outlist[position]=line
		line=maf_file.readline()
	for line in outlist:
		output_file.write('\t'.join(line))
	output_file.write('\n')

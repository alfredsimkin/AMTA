maf_file=open('all_species_exactly_once.maf')

def get_maf(maf_file):
	maf_chunk=[]
	line=maf_file.readline().split()
	while line:
		maf_chunk.append(line)
		line=maf_file.readline().split()
	maf_chunk=zip(*maf_chunk[:5])
	if len(maf_chunk)>1:
		names=maf_chunk[1]
	else:
		names=[]
	return names

names=get_maf(maf_file)
species=['gorGor3', 'hg19', 'panTro3', 'ponAbe2', 'nomLeu1']
while names:
	for name_number, name in enumerate(names):
		if species[name_number] not in name:
			print name
	names=get_maf(maf_file)

import sys
data_folder=sys.argv[1]
maf_file=open(data_folder+'all_species_exactly_once.maf')
output_file=open(data_folder+'exactly_once_chunk_indices_sorted2', 'w')

def get_maf(maf_file, maf_dict):
	byte_count=maf_file.tell()
	maf_line=maf_file.readline()
	if not maf_line:
		return None
	elif not maf_line.strip():
		return 'empty_line'
	else:
		species_list=eval(sys.argv[2])
		coords=[]
		for species in species_list:
			coords.append([])
		species, chrom, start='', '', 0
		while maf_line.strip():
			split_line=maf_line.split()
			species, chrom=split_line[1].split('.')[:2]
			start, length, strand, total_length=int(split_line[2]), int(split_line[3]), split_line[4], int(split_line[5])
			end=start+length
			if strand=='-':
				start, end=total_length-end, total_length-start
			try:
				species_number=species_list.index(species)
				if coords[species_number]:
					print 'something is afoot:\nthe species', species, 'occurs twice in this chunk\nrun filter_for_all_species.py again'
					exit()
				coords[species_number]=','.join(map(str, [chrom,start,end]))
			except ValueError:
				pass
			maf_line=maf_file.readline()
		maf_key=coords[0].split(',')
		maf_key[1:3]=map(int, maf_key[1:3])
		if tuple(maf_key) not in maf_dict:
			maf_dict[tuple(maf_key)]=set([])
		maf_dict[tuple(maf_key)].add(str(byte_count)+':'+'\t'.join(coords))
		return maf_dict

maf_dict={}
maf_dict=get_maf(maf_file, maf_dict)
maf_result=True
while maf_result:
	maf_result=get_maf(maf_file, maf_dict)
	if maf_result:
		maf_dict=maf_result
keys=sorted(maf_dict.keys())
for key in keys:
	for value in maf_dict[key]:
		output_file.write(value+'\n')

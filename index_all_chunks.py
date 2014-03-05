import sys
data_folder=sys.argv[1]
maf_file=open(data_folder+'all_species_exactly_once.maf')
output_file=open(data_folder+'exactly_once_chunk_indices', 'w')
chunk_summaries=[]

def get_maf(maf_file):
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
		return str(byte_count)+':'+'\t'.join(coords)

chunk_summary=get_maf(maf_file)
while chunk_summary:
	if chunk_summary!='empty_line':
		output_file.write(chunk_summary+'\n')
	chunk_summary=get_maf(maf_file)

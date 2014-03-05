import sys

species_dict={}
data_folder=sys.argv[1]
maf_input=sys.argv[2]
species_list=eval(sys.argv[3])

finished_maf=open(data_folder+'all_species_exactly_once.maf', 'w')
'''
output_file=open((data_folder+maf_input)[:-4]+'_trimmed.maf', 'w')
for line in open(data_folder+maf_input):
	if line.startswith('s') or line.startswith('\n'):
		output_file.write(line)
print 'finished trimming'
'''
#maf_input=(data_folder+maf_input)[:-4]+'_trimmed.maf'
maf_input=(data_folder+maf_input)
maf_file=open(maf_input)
good_indices=open(data_folder+'exactly_once_byte_counts', 'w')
'''
maf_file.seek(-2,2)
penultimate_char=maf_file.read(1)
if penultimate_char!='\n':
	maf_file.close()
	new_maf=open(maf_input, 'a')
	new_maf.seek(0,2)
	new_maf.write('\n')
	new_maf.close()
	maf_file=open(maf_input)
maf_file.seek(0)
'''
def get_maf(maf_file):
	maf_entry=[]
	maf_line=maf_file.readline()
	while maf_line:
		if len(maf_line)>1:
			maf_entry.append(maf_line.split())
		elif len(maf_line)==1:
			if len(maf_entry)==0:
				maf_entry='extra internal blank'
			break
		maf_line=maf_file.readline()
	return maf_entry


byte_count, maf_entry=maf_file.tell(), get_maf(maf_file)
while maf_entry:
	outlist=[]
	for species in species_list:
		outlist.append([])
	for line in maf_entry:
		species=line[1].split('.')[0]
		if species in species_list and line[0]==('s'):
			species_number=species_list.index(species)
			if outlist[species_number]==[]:
				outlist[species_number]='\t'.join(line)+'\n'
			else:
				break
	good_outlist=True
	for item in outlist:
		if len(item)==0:
			good_outlist=False
	if good_outlist:
		good_indices.write(str(byte_count)+'\n')
		for maf_species in outlist:
			finished_maf.write(maf_species)
		finished_maf.write('\n')
	byte_count, maf_entry=maf_file.tell(), get_maf(maf_file)

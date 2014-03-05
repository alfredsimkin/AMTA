import custom
import collect_ancestors
import subprocess
import cPickle
import sys
def three_prime_start(line):
	if line[5]=='+':
		return [line[0], int(line[7]), int(line[2]), line[3], line[5]]
	if line[5]=='-':
		return [line[0], int(line[1]), int(line[6]), line[3], line[5]]

def advance_maf_file(maf_summary):
	summary_byte_count=maf_summary.tell()
	parsed_summary=maf_summary.readline().split(':')
	parsed_summary[1]=[species.split(',') for species in parsed_summary[1].split('\t')]
	parsed_summary[0]=[summary_byte_count, int(parsed_summary[0])]
	for entry_number, entry in enumerate(parsed_summary[1]):
		for column_number, column in enumerate(entry):
			try:
				column=int(column)
				parsed_summary[1][entry_number][column_number]=column
			except ValueError:
				pass
	return parsed_summary


def filter_overlappers(overlappers, total_species):
	good_utr=True
	for species_number in range(total_species):
		species_list=[]
		for overlapper in overlappers:
			human_start, human_end=overlapper[1][0][1:]
			species_list.append(overlapper[1][species_number])
		species_list.sort()
		old_end=0
#		print species_list
		for species_maf in species_list:
			species_start, species_end=species_maf[1:]
			if species_start<old_end:
				good_utr=False
			old_end=species_end
	return good_utr

def get_maf(maf_file, maf_byte_count, maf_species):
	maf_chunk, done=[], False
	maf_file.seek(maf_byte_count)
	line=maf_file.readline().split()
	while line:
		if line[1].split('.')[0]==maf_species[0]:
			strand=line[4]
		maf_chunk.append(line)
		line=maf_file.readline().split()
	maf_chunk=zip(*maf_chunk)
	sequence=maf_chunk[6]
	zipped_sequence=map(list, zip(*sequence))
	while not done:
		try:
			zipped_sequence.remove(list('-'*len(maf_species)))
		except ValueError:
			done=True
	sequence=zip(*zipped_sequence)
	sequence=[''.join(item) for item in sequence]
#	print sequence
	return strand, list(sequence)

def retrieve_basepairs(overlappers, gene_summary, total_species):
#	print overlappers
#	print gene_summary
	same_strand=True
	old_strand='hey'
	old_coords=''
	joiner=[]
	full_sequences=[]
	for species in range(total_species):
		joiner.append([])
		full_sequences.append('')
	for overlapper in overlappers:
		coords=[species[1:] for species in overlapper[1]]
		for species_number, coord in enumerate(coords):
			if old_coords and coord[0]>=old_coords[species_number][1]:
				if coord[0]>old_coords[species_number][1]:
					joiner[species_number]='NNNNN'
#					print 'forward discontinuous'
				elif coord[0]==old_coords[species_number][1]:
					joiner[species_number]='-----'
#				else:
#					print 'something_odd'
			if old_coords and coord[0]<old_coords[species_number][1]:
				if coord[1]==old_coords[species_number][0]:
					joiner[species_number]='-----'
				elif coord[1]<old_coords[species_number][0]:
#					print 'reverse discontinuous'
					joiner[species_number]='NNNNN'
#				else:
#					print 'something odd'
		old_coords=coords
		if 'NNNNN' not in joiner:
			joiner=['' for thing in joiner]
		utr_start, utr_end, gene_name, utr_strand=gene_summary[1:]
		human_start, human_end=coords[0]
		start_trim=utr_start-human_start
		end_trim=human_end-utr_end
#		print start_trim, end_trim
		human_strand, sequences=get_maf(maf_file, overlapper[0][1], maf_species)
		if start_trim>0:
			letter_count=0
			for actual_trim, letter in enumerate(sequences[1]):
				if letter!='-':
					letter_count+=1
				if letter_count==start_trim:
					break
			sequences=[sequence[actual_trim+1:] for sequence in sequences]
		if end_trim>0:
			letter_count=0
			for actual_trim, letter in enumerate(sequences[1][::-1]):
				if letter!='-':
					letter_count+=1
				if letter_count==end_trim:
					break
#			print actual_trim
			sequences=[sequence[:-(actual_trim+1)] for sequence in sequences]
		full_sequences=[full_sequences[seq_num]+joiner[seq_num]+sequences[seq_num] for seq_num, sequence in enumerate(full_sequences)]
		if human_strand!=old_strand and old_strand!='hey':
			same_strand=False
		old_strand=human_strand
	if human_strand!=utr_strand:
		full_sequences=[custom.revcom(full_sequence) for full_sequence in full_sequences]
	if same_strand and len(full_sequences[0])>1:
		return [gene_name, full_sequences]
#		print gene_name, full_sequences
data_folder=sys.argv[1]
refseq_bed_file=sys.argv[2]
sorted_gene_list=[line.strip().split('\t') for line in open(data_folder+refseq_bed_file+'filtered_lastz')]
sorted_gene_list.sort(key=three_prime_start)
maf_summary=open(data_folder+'exactly_once_chunk_indices_sorted2')
maf_file=open(data_folder+'all_species_exactly_once.maf')
final_output=open(data_folder+'final_utr_dictionary', 'w')
parsed_summary=advance_maf_file(maf_summary)
#parsed_summary after: [[index_byte, maf_byte], [[sp_one_chrom, sp_one_chunk_start, sp_one_chunk_end], [sp_two_triplet], [etc]]]
overlappers=[]
final_dict={}
species_string=sys.argv[3]
maf_species=eval(sys.argv[4])
gene_count=0
for gene_line in sorted_gene_list:
	gene_summary=three_prime_start(gene_line)
	gene_chrom, utr_start, utr_end, gene_name, gene_strand=gene_summary
	# gene_summary is: [chrom, utr_start, utr_end, gene_name, gene_strand]
#	print parsed_summary[1][0], "vs", gene_summary[:3]
	while parsed_summary[0]:
#		print parsed_summary[1][0], "vs", gene_summary[:3]
		if gene_chrom>parsed_summary[1][0][0] or utr_start>parsed_summary[1][0][2]:
#			print "gene is bigger"
			pass
		elif gene_chrom<parsed_summary[1][0][0] or utr_end<parsed_summary[1][0][1]:
#			print "gene is smaller"
			if overlappers:
				maf_summary.seek(overlappers[0][0][0])
				parsed_summary=advance_maf_file(maf_summary)
				if filter_overlappers(overlappers, len(maf_species)):
					finished_maf=retrieve_basepairs(overlappers, gene_summary, len(maf_species))
					if finished_maf:
						gene_count+=1
#						custom.print_phylip(common_species_list, finished_maf, data_folder+'infile') ****
						species_dict={}
						for species_number, common_species in enumerate(eval(species_string)):
							species_dict[common_species]=finished_maf[1][species_number]
						final_dict[finished_maf[0]]=species_dict
#						subprocess.call(["sh", "dnaml_script.sh"])
#						final_dict[gene_name]=collect_ancestors2.collect_ancestors()
#						if gene_count%101==100:
#							print final_dict
#							exit()
				overlappers=[]
			break
		else:
			overlappers.append(parsed_summary)
		parsed_summary=advance_maf_file(maf_summary)
cPickle.dump(final_dict, final_output)

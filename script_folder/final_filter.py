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


def filter_overlappers(overlappers, gene_summary, total_species):
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

def get_maf(maf_file, maf_byte_count):
	maf_chunk, done=[], False
	maf_file.seek(maf_byte_count)
	line=maf_file.readline().split()
	while line:
		if 'hg19' in line[1]:
			strand=line[4]
		maf_chunk.append(line)
		line=maf_file.readline().split()
#	print maf_chunk
	maf_chunk=zip(*maf_chunk[:5])
	sequence=maf_chunk[6]
	zipped_sequence=map(list, zip(*sequence))
	while not done:
		try:
			zipped_sequence.remove(['-', '-', '-', '-', '-'])
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
	for species in total_species:
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
		human_strand, sequences=get_maf(maf_file, overlapper[0][1])	
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
	if same_strand:
		return [gene_name, full_sequences]
#		print gene_name, full_sequences
data_folder=sys.argv[1]
refseq_bed_file=sys.argv[2]
sorted_gene_list=[line.strip().split('\t') for line in open(data_folder+refseq_bed_file)]
sorted_gene_list.sort(key=three_prime_start)
maf_summary=open(data_folder+'exactly_once_indices_sorted')
maf_file=open(data_folder+'all_species_exactly_once.maf')
final_output=open('final_utr_dictionary', 'w')
parsed_summary=advance_maf_file(maf_summary)
overlappers=[]
final_dict={}
species_string=sys.argv[3]
species_list=[]
for species_number, species in enumerate(eval(species_string)):
	species_list.append(species+' '*(10-len(species)))
gene_count=0
for gene_line in sorted_gene_list:
	print gene_line
	gene_summary=[gene_line[0], int(gene_line[-2]), int(gene_line[-1]), gene_line[0], gene_line[2]]
#	print parsed_summary[1][0], "vs", gene_summary[:3]
	while parsed_summary[0]:
#		print parsed_summary[1][0], "vs", gene_summary[:3]
		if gene_summary[0]>parsed_summary[1][0][0] or gene_summary[1]>parsed_summary[1][0][2]:
#			print "gene is bigger"
			pass
		elif gene_summary[0]<parsed_summary[1][0][0] or gene_summary[2]<parsed_summary[1][0][1]:
#			print "gene is smaller"
			if overlappers:
				maf_summary.seek(overlappers[0][0][0])
				parsed_summary=advance_maf_file(maf_summary)
				if filter_overlappers(overlappers, gene_summary, len(species_list)):
					finished_maf=retrieve_basepairs(overlappers, gene_summary, len(species_list))
					if finished_maf:
						gene_count+=1
						custom.print_phylip(species_list, finished_maf, 'infile')
						subprocess.call(["sh", "dnaml_script.sh"])
#						print gene_summary[3]
						final_dict[gene_summary[3]]=collect_ancestors.collect_ancestors()
#						if gene_count%101==100:
#							print final_dict
#							exit()
				overlappers=[]
			break
		else:
			overlappers.append(parsed_summary)
		parsed_summary=advance_maf_file(maf_summary)
cPickle.dump(final_dict, final_output)

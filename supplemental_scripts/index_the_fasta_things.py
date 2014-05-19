#working with custom.py, takes a fasta file having multiple entries and distributes the
#entries to 24 separate fasta files having approximately equal size to each other

import custom
import sys
output_list=[]
fasta_file=open(sys.argv[1])
line_count=4

def get_next_fasta(fasta_file):
	line_count=0
	title_start_byte=fasta_file.tell()
	putative_title=fasta_file.readline()
	if putative_title.startswith('>'):
		title=putative_title[1:-1]
		sequence=fasta_file.readline()
		while not sequence.startswith('>') and len(sequence)>0:
			line_count+=1
			rewind_byte_count=fasta_file.tell()
			sequence=fasta_file.readline()
		return line_count, title, title_start_byte, rewind_byte_count
	else:
		return 0,0,0,0

while line_count:
	line_count, title, title_start_byte, rewind_byte_count=get_next_fasta(fasta_file)
	fasta_file.seek(rewind_byte_count)
	if line_count:
		output_list.append([line_count+1, title, title_start_byte])
output_list.sort()
serp_list=custom.serpentine(output_list, 24)

for serp_file_number, serp_file in enumerate(serp_list):
	output_file=open('fasta_stuff'+str(serp_file_number), 'w')
	for fasta_entry in serp_file:
		fasta_file.seek(int(fasta_entry[2]))
		line_number=0
		while line_number<fasta_entry[0]:
			output_file.write(fasta_file.readline())
			line_number+=1

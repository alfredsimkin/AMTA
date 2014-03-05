import custom
output_list=[]
import sys
fasta_file=open(sys.argv[1])
line_count=4
sorted_file=open('sorted_fasta_entries', 'w')

def get_next_fasta(fasta_file):
	line_count=0
	title_start_byte=fasta_file.tell()
	sequence=fasta_file.readline()
	while sequence:
		if sequence.startswith('>'):
			title=sequence.strip()[1:]
			sequence=fasta_file.readline()
			while not sequence.startswith('>') and len(sequence)>0:
				line_count+=1
				rewind_byte_count=fasta_file.tell()
				sequence=fasta_file.readline()
			return line_count, title, title_start_byte, rewind_byte_count
			break
		else:
			sequence=fasta_file.readline()
while line_count:
	line_count, title, title_start_byte, rewind_byte_count=get_next_fasta(fasta_file)
	fasta_file.seek(rewind_byte_count)
	if line_count:
		output_list.append([line_count+1, title, title_start_byte])
output_list.sort()
for line in output_list:
	sorted_file.write('\t'.join([str(item) for item in line])+'\n')
serp_list=custom.serpentine(output_list, 24)
for serp_file_number, serp_file in enumerate(serp_list):
	output_file=open('fasta_stuff'+str(serp_file_number), 'w')
	for fasta_entry in serp_file:
		fasta_file.seek(int(fasta_entry[2]))
		line_number=0
		while line_number<fasta_entry[0]:
			output_file.write(fasta_file.readline())
			line_number+=1

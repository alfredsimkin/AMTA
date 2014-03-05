import sys
data_folder=sys.argv[1]
genome_folder=sys.argv[2]
refseq_fasta_file=sys.argv[3]
chromosome_list=[line.strip() for line in open(genome_folder+'chromosome_list')]
output=open(data_folder+'lastz_commands', 'a')
output_file_names=open(genome_folder+'result_paths', 'w')
for line_number, fasta_thing in enumerate(chromosome_list):
	output.write('lastz '+refseq_fasta_file+'[multiple] '+'../script_folder/'+genome_folder+fasta_thing+'[multiple] --match=1,3 --ambiguous=n --output=../script_folder/'+genome_folder+'refseq_reference_proteins_vs_'+fasta_thing+' --format=general\n')
	output_file_names.write('refseq_reference_proteins_vs_'+fasta_thing+'\n')

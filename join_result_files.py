import sys
genome_folder=sys.argv[1]
output_file=open(genome_folder+'all_results', 'w')
for input_path in open(genome_folder+'result_paths'):
	input_path=input_path.strip()
	input_file=open(genome_folder+input_path)
	for line_number, line in enumerate(input_file):
		if line_number>0:
			output_file.write(line)

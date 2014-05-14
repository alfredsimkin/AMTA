def count_in_base(string, base, valuestring):
	outlist=[]
	for count in range(base**len(string)):
		outlist.append(string)
		position=len(string)-1
		value=valuestring.index(string[position])
		string=string[:position]+valuestring[value+1]+string[position+1:]
		while value>=(base-1) and count<(base**len(string)):
			string=string[:position]+valuestring[0]+string[position+1:]
			position-=1
			value=valuestring.index(string[position])
			string=string[:position]+valuestring[value+1]+string[position+1:]
	return outlist

def revcom(sequence, sequence_type='DNA'):
	#the guts of this module are not of my creation
	#I've added some tweaks
	import string
	if sequence_type=='RNA':
		complement = string.maketrans('ACGTUN', 'UGCAAN')
	elif sequence_type=='DNA':
		complement = string.maketrans('ACGTUN', 'TGCAAN')
	return sequence.upper().translate(complement)[::-1]

def meanvar(value_list, vartype='sample'):
	import math
	n=len(value_list)
	total=math.fsum(value_list)
	square_sum=math.fsum([value**2 for value in value_list])
	mean=total/n
	second=2*mean*total
	third=mean**2*n
	if n>1 and vartype=='sample':
		variance=(square_sum-(2*mean*total)+(mean**2)*n)/(n-1)
	else:
		variance=(square_sum/n)-(mean**2)

	return [mean, variance]

def grabcolumn(path, column):
	outlist=[]
	for line in open(path):
		split_line=line.strip().split()
		outlist.append(split_line[column])
	return outlist

def gather_columns(path, columns=None, split_thing='\t'):
	newlist=[]
	for line in open(path):
		line_split=line.strip().split(split_thing)
		if columns==None:
			newline=line_split
		else:
			newline=[line_split[column] for column in columns]
		newlist.append(newline)
	return newlist

def read_fasta(fasta_file):
	seq, name_list, seq_list, seq_dict='', [], [], {}
	for line in open(fasta_file):
		line=line.strip()
		if '>' in line:
			name_list.append(line[1:])
			if len(seq)>0:
				seq_list.append(seq)
				seq=''
		else:
			seq=seq+line
	seq_list.append(seq)
#	for seq_number, name in enumerate(name_list):
#		seq_dict[name]=seq_list[seq_number]
	return [[name, seq_list[name_number]] for name_number, name in enumerate(name_list)]
def print_fasta(fasta_list, outfile, mode='a', line_chars=60):
	"""
	this program prints fasta paired lists to fasta format
	"""
	output=open(outfile, mode)
	for sequence in fasta_list:
		output.write(">"+sequence[0]+"\n")
		for char_number, char in enumerate(sequence[1]):
			output.write(char)
			if char_number%line_chars==line_chars-1 or char_number==(len(sequence[1]))-1:
				output.write("\n")
def print_phylip(species_names, sequence_list, phylipfile):
	#prints paired name/sequence pairs in sequence_list to an interleaved output file
	#(phylipfile) and names each with names from species_names. Unlike the paired
	#fasta_list, the paired sequence_list has len(species_names) sequences per
	#pairing instead of one
	output=open(phylipfile, 'w')
	total_length=len(sequence_list[1][0])
	output.write(str(len(species_names))+' '+str(total_length)+'\n')
	for species_number, species in enumerate(species_names):
		output.write(species_names[species_number])
		output.write(sequence_list[1][species_number]+'\n')
def print_alignment(fasta_thing, block_size=60):
	#reads an aligned fasta file and prints it 
	#interleaved in blocks of size block_size
	if type(fasta_thing) is str:
		fasta_thing=read_fasta(fasta_thing)
	else:
		fasta_list=fasta_thing
	for sequence in fasta_list:
		print sequence[0]
	for letter_number, letter in enumerate(fasta_list[0][1]):
		if letter_number%block_size==0:
			for sequence in fasta_list:
				print sequence[1][letter_number:letter_number+block_size]
			print "\n",

def split_to_nodes (nodes, unsplit_path, output_folder, master_path):
	import subprocess
	import math
	output_number=1
	new_master_command=open(master_path, 'w')
	unsplit_file=open(unsplit_path)
	job_list=unsplit_file.readlines()
	total_jobs=float(len(job_list))
	divisor=math.ceil(total_jobs/nodes)
	for number, line in enumerate(job_list):
		if number%divisor==0:
			outfile=open("{0}{1}.sh".format(output_folder, output_number), 'w')
			new_master_command.write("{0}{1}.sh\n".format(output_folder, output_number))
			output_number+=1
		if number%divisor==divisor-1 or number==total_jobs-1:
			subprocess.call(["chmod", "+x", "{0}{1}.sh".format(output_folder, output_number-1)])
		outfile.write(line)
	return output_number-1
	
def theta_w(individuals, segsites, sites_w_info):
	#this program takes the number of individuals in the sample,
	#the number of segregating sites in the sample,
	#and the number of total sites considered to calculate theta_w
	a_1=0
	S=float(segsites)/sites_w_info #bases theta on total sites considered rather than total sites in locus
	for value in range(1,individuals):
		a_1=a_1+1.0/value
	theta=S/a_1
	return theta

def replace_all(input_list, conversion_list):
	#this program replaces all first elements from
	#conversion_list found in input_list with all
	#second elements from conversion_list
	for converting_line in conversion_list:
		for in_number, in_line in enumerate(input_list):
			if converting_line[0] in in_line:
				input_list[in_number]=in_line.replace(converting_line[0], converting_line[1])
	return input_list

def overlapping_search(search, string):
	#this definition searches 'string' using search term 'search'
	#and returns the coordinates of all overlapping matches, allowing for gaps
	import re
	expression, starts, ends="", [], []
	gap="-*"
	for letter in search[:-1]:
		expression+=letter+gap
	expression+=search[-1]
	for m in re.finditer("(?="+expression+")", string):
		start=m.start()
		starts.append(start)
		ends.append((re.match(expression, string[start:])).end()+start)
	return [str(start)+':'+str(ends[start_number]) for start_number, start in enumerate(starts)]

def choose(n, r):
	#counts ways of choosing r things from a set of n
	import math
	from operator import mul
	from decimal import Decimal
	if n-r>r:
		factorial_divisor=r
	else:
		factorial_divisor=n-r
	num_list=range(1, n+1)[:-(factorial_divisor+1):-1]
	denominator=math.factorial(factorial_divisor)
	if r>0 and r<n:
		numerator=reduce(mul, num_list)
	else:
		numerator=denominator
	return Decimal(numerator/denominator)

def binomial_prob(prob, number_observed, number_draws):
	#calculates the binomial probability of seeing number_observed events in 
	#number_draws total events when the probability of a single event is prob
	from decimal import Decimal
	ways=Decimal(choose(number_draws, number_observed))
	return Decimal(str(prob**number_observed*(1-prob)**(number_draws-number_observed)))*Decimal(ways)

def check_overlap(start1, end1, start2, end2):
	#checks whether the start and end from the first two entries
	#overlaps with the start and end from the second two entries
	#returns "status" of overlap and start and end coordinates of overlapping bases
	if start1<=start2:
		bigger_small=start2
		status='smaller'
	else:
		bigger_small=start1
		status='bigger'
	if end1<=end2:
		smaller_big=end1
	else:
		smaller_big=end2
	if smaller_big>bigger_small:
		status='overlapping'
	return bigger_small, smaller_big, status

def serpentine(ranked_list, divisor):
	#takes a ranked list and distributes it to divisor
	#sub lists of approximately equal average ranks
	out_list, number=[], 0
	for element in range(divisor):
		out_list.append([])
	for rank_number, value in enumerate(ranked_list):
		if rank_number%divisor==0:
			step=0
		elif (rank_number/divisor)%2==0:
			step=1
		elif (rank_number/divisor)%2==1:
			step=-1
		number=number+step
		out_list[number].append(value)
	return out_list
def fasta_to_fastq(fasta_file_name):
	#converts fasta files into fastq, only works if 
	#each fasta entry is on a single line. All fastq 
	#entries are given a quality score of 'z'
	fastq_file=open(fasta_file+'.fq', 'w')
	for line_number, line in enumerate(open(fastq_file)):
		if line_number%2==0 and '>' in line:
			fastq_file.write('@'+line[1:])
		elif line_number%2==0 and '>' not in line:
			print 'bad fasta file for fastq conversion'
			exit()
		elif line_number%2==1:
			fastq_file.write(line)
			fastq_file.write('+\n')
			fastq_file.write('z'*(len(line)-1)+'\n')
def fastq_to_fasta(fastq_file):
	#converts fastq files to fasta
	fasta_file=open(fastq_file+'.fa', 'w')
	for line_number, line in enumerate(open(fastq_file)):
		if line_number%4==0 and '@' in line:
			fasta_file.write('>'+line[1:])
		elif line_number%4==0 and '@' not in line:
			print 'error'
			exit()
		elif line_number%4==1:
			fasta_file.write(line)
def locate_differences(file1, file2):
	#finds first line where two files differ
	file1=open(file1)
	file2=open(file2)
	file1_line=file1.readline()
	file2_line=file2.readline()
	line_number=0
	while file1_line==file2_line:
		file1_line=file1.readline()
		file2_line=file2.readline()
		line_number+=1
	print file1_line
	print file2_line
	print line_number
def compute_pi(sequences):
	#computes the popgen statistic pi for a list of DNA sequences
	good_nucs='ACGTacgt'
	diff_count, bad_count=0, 0
	for sequence_number, sequence_one in enumerate(sequences):
		for sequence_two in sequences[sequence_number+1:]:
			for bp_number, bp_one in enumerate(sequence_one):
				bp_two=sequence_two[bp_number]
				if bp_two!=bp_one and bp_one in good_nucs and bp_two in good_nucs:
					diff_count+=1
				if bp_one not in good_nucs or bp_two not in good_nucs:
					bad_count+=1
	total_comparisons=float(choose(len(sequences), 2))*len(sequences[0])
	if bad_count<total_comparisons:
		return diff_count/(total_comparisons-bad_count), total_comparisons-bad_count
	else:
		return -0.02, total_comparisons-bad_count
def compute_pi2(sequences):
	#computes the popgen statistic pi for a list of DNA sequences
	good_nucs='ACGTacgt'
	diff_count, bad_count=0, 0
	for sequence_number, sequence_one in enumerate(sequences):
		for sequence_two in sequences[sequence_number+1:]:
			for bp_number, bp_one in enumerate(sequence_one):
				bp_two=sequence_two[bp_number]
				if bp_two!=bp_one and bp_one in good_nucs and bp_two in good_nucs:
					diff_count+=1
				if bp_one not in good_nucs or bp_two not in good_nucs:
					bad_count+=1
	total_comparisons=float(choose(len(sequences), 2))*len(sequences[0])
	return diff_count, total_comparisons, bad_count

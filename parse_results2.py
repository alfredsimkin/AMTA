#remove identities below 95%
#make dict sorted by gene
#sort by strand
#group by increasing positions
#sum coverage by group
#sum self-overlap by group
#remove genes with transcripts that cover the same UTR material twice
import copy
import custom
import cPickle
import sys

def sort_by_genome_position(gene_line):
	return [gene_line[6], int(gene_line[9])]
def sort_by_coverage(group):
	return group[-2]

def make_transcripts(result_file, identity):
	gene_dict={}
	for line in open(result_file):
		line=line.split()
		if float(line[12][:-1])>=identity:
			if line[1] not in gene_dict:
				gene_dict[line[1]]=[]
			gene_dict[line[1]].append(line)
	for gene in gene_dict:
		gene_list=copy.deepcopy(gene_dict[gene])
		gene_list.sort(key=sort_by_genome_position)
		gene_dict[gene]={}
		for line in gene_list:
			strand=line[7]
			if strand not in gene_dict[gene]:
				gene_dict[gene][strand]=[]
			gene_dict[gene][strand].append(line)
	for gene in gene_dict:
		for strand in gene_dict[gene]:
			gene_list=copy.deepcopy(gene_dict[gene][strand])
			gene_dict[gene][strand]=[]
			old_start=99999999999999999999
			old_chrom='chrnever_heard_of_it'
			for line in gene_list:
				start, chrom=int(line[4]), line[6]
				if start<old_start or chrom!=old_chrom:
					gene_dict[gene][strand].append([])
				gene_dict[gene][strand][-1].append(line)
				old_start, old_chrom=start, chrom
	return gene_dict

def utr_starts(bed_file_list, refseq_file_dict):
	utr_dict={}
	for bed_entry in bed_file_list:
		gene_name=bed_entry[3]
		if bed_entry[5]=='+':
			utr_length=int(bed_entry[2])-int(bed_entry[7])
		if bed_entry[5]=='-':
			utr_length=int(bed_entry[6])-int(bed_entry[1])
		utr_start=len(refseq_file_dict[gene_name])-utr_length
		utr_dict[gene_name]=utr_start
	return utr_dict

def get_overlap_coverage(gene_dict, utr_dict):
	bad_utrs=set([])
	for gene in gene_dict:
		transcript_list=[]
		for strand in gene_dict[gene]:
			for transcript_number, transcript in enumerate(gene_dict[gene][strand]):
				coverage=set([])
				old_end, overlap=0,0
				gene_length=int(transcript[0][3])
				for line in transcript:
					start, end=int(line[4]), int(line[5])
					coverage=coverage|set(range(start, end))
					current_overlap=old_end-start
					utr_start=utr_dict[gene]
					if current_overlap>0:
						overlap=overlap+current_overlap
						if start>utr_start or old_end>utr_start:
							bad_utrs.add(gene)
					old_end=end
				gene_dict[gene][strand][transcript_number].extend([gene_length, len(coverage), overlap])
				transcript_list.append(gene_dict[gene][strand][transcript_number])
		transcript_list.sort(key=sort_by_coverage)
		gene_dict[gene]=transcript_list
	#print gene_dict['NM_001918']
	#print len(gene_dict['NM_001918'])
	return gene_dict, bad_utrs

def threshold_test(thresholds, gene_dict, bad_genes):
	best_coverage_threshold, second_best_ratio, overlap_threshold=thresholds
	for gene in gene_dict:
		gene_length, best_coverage, best_overlap=gene_dict[gene][-1][-3:]
		if len(gene_dict[gene])>1:
			second_best_coverage=gene_dict[gene][-2][-2]
		else:
			second_best_coverage=0
		if float(best_coverage)/gene_length>best_coverage_threshold and float(second_best_coverage)/best_coverage<second_best_ratio:
			if float(best_overlap)/best_coverage<overlap_threshold:
				pass
			else:
				bad_genes.add(gene)
		else:
			bad_genes.add(gene)
	total_genes, total_bad=len(gene_dict), len(bad_genes)
	print total_genes, "total genes"
	print total_bad, "total bad genes"
	for bad_gene in bad_genes:
		gene_dict.pop(bad_gene)
	return gene_dict

genome_folder=sys.argv[1]
print '\n\nthe current genome folder is', genome_folder
refseq_file_dict=dict(custom.read_fasta(sys.argv[2]))
bed_file_list=[line.strip().split('\t') for line in open(sys.argv[3])]

'''
The following variables define the thresholds of the program:
'identity' only keeps transcripts with more than this percent identity to the query gene
'best_converage_threshold' removes genes with no transcript covering greater than this fraction of the query gene
'second best ratio' removes genes where the second best transcript coverage covers more than this fraction of the best transcript
'overlap_threshold' removes genes where self-overlap of the hits making up a transcript is greater than this fraction of the total length of the query gene covered
'''
identity, best_coverage_threshold, second_best_ratio, overlap_threshold=95, 0.8, 0.2, 0.2
thresholds=[best_coverage_threshold, second_best_ratio, overlap_threshold]
pickled_file=open(genome_folder+'pickled_good_gene_dict', 'w')

gene_dict=make_transcripts(genome_folder+'all_results', identity)
print 'there are', len(gene_dict.keys()), 'total genes with highly identical hits'
utr_dict=utr_starts(bed_file_list, refseq_file_dict)
gene_dict, bad_utrs=get_overlap_coverage(gene_dict, utr_dict)
gene_dict=threshold_test(thresholds, gene_dict, bad_utrs)
print 'there are', len(gene_dict.keys()), 'genes with a single high confidence transcript hit after filtering'
cPickle.dump(gene_dict, pickled_file)

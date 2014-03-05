#remove identities below 95%
#make dict sorted by gene
#sort by strand
#group by increasing positions
#sum coverage by group
#sum self-overlap by group
#remove genes with no group having >20% coverage
#remove genes with multiple groups having >20% coverage
#remove genes where other group coverage is >20% of best group
#remove genes where self-overlap is >20% of coverage amount.


import copy
import custom
import cPickle

'''
pickled_file=open('pickled_good_gene_dict', 'w')

def sort_by_genome_position(gene_line):
	return [gene_line[6], int(gene_line[9])]
def sort_by_coverage(group):
	return group[-2]

working_list, gene_dict=[], {}
for line in open('all_results'):
	line=line.split()
	if float(line[12][:-1])>=95:
		working_list.append(line)
for line in working_list:
	if line[1] not in gene_dict:
		gene_dict[line[1]]=[]
	gene_dict[line[1]].append(line)
working_list=[]
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
'''
bad_utrs=set([])
utr_dict={}

for fasta_gene in custom.read_fasta('human_refseq_utr_lowercase'):
	exon_start, utr_start=0,0
	for letter_number, letter in enumerate(fasta_gene[1]):
		if letter.isupper() and not exon_start:
			exon_start=letter_number
		if letter.islower() and exon_start and not utr_start:
			utr_start=letter_number
	print fasta_gene[0].split()[0], utr_start
	utr_dict[fasta_gene[0].split()[0]]=utr_start

'''
for gene in gene_dict:
	group_list=[]
	for strand in gene_dict[gene]:
		for group_number, group in enumerate(gene_dict[gene][strand]):
			coverage=set([])
			old_end, overlap=0,0
			gene_length=int(group[0][3])
			for line in group:
				start, end=int(line[4]), int(line[5])
				coverage=coverage|set(range(start, end))
				current_overlap=old_end-start
				utr_start=utr_dict[gene]
				if current_overlap>0:
					overlap=overlap+current_overlap
					if start>utr_start or old_end>utr_start:
						bad_utrs.add(gene)
				old_end=end
			gene_dict[gene][strand][group_number].extend([gene_length, len(coverage), overlap])
			group_list.append(gene_dict[gene][strand][group_number])
	group_list.sort(key=sort_by_coverage)
	gene_dict[gene]=group_list
#print gene_dict['NM_001918']
#print len(gene_dict['NM_001918'])
high_self, poor_coverage, too_many_high=0,0,0
best_coverage_threshold, second_best_ratio, overlap_threshold=0.8, 0.2, 0.2
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
			high_self+=1
			bad_utrs.add(gene)
	else:
		bad_utrs.add(gene)
	if float(best_coverage)/gene_length<=best_coverage_threshold:
		poor_coverage+=1
	if float(best_coverage)/gene_length>best_coverage_threshold and float(second_best_coverage)/best_coverage>=second_best_ratio:
		too_many_high+=1
total_bad_utrs=len(bad_utrs)-(poor_coverage+too_many_high+high_self)
total_genes, total_bad=len(gene_dict), len(bad_utrs)
print total_genes, "total genes"
print total_bad, "total bad genes"
for bad_gene in bad_utrs:
	gene_dict.pop(bad_gene)
total_good=len(gene_dict)
print "{0} good_genes, {1} poor coverage genes, {2} multiple good hit genes, {3} high self overlap genes, {4} bad_UTR_genes".format(total_good, poor_coverage, too_many_high, high_self, total_bad_utrs)
print '\t'.join([str(value) for value in [total_genes, total_bad, total_good, poor_coverage, too_many_high, high_self, total_bad_utrs]])
cPickle.dump(gene_dict, pickled_file)
'''

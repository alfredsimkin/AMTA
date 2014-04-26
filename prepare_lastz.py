'''
This program acts on a MAF formatted list of species, a BED formatted
list of transcripts, a fasta formatted list of the same transcripts,
and a series of fasta formatted genomes. The program filters and
sorts BED and MAF files, and prepares a list of LASTZ commands (used
in later steps to pull syntenic transcripts from other genomes.)
'''

import subprocess
import os

#make sure all data (MAF files, BED files, fasta files, etc.
#is stored in this folder
data_folder='../data_folder/'

#name of refseq genes BED file (in data_folder).
refseq_input_bed='human_refseq_bed'

'''
do not use fasta files precomputed by UCSC for 'refseq_input_fasta'. 
Instead, upload your BED file to UCSC as a custom track and download
the resulting coordinates from 'table browser' as a fasta file with
one fasta entry per gene, and including 5' UTR, cDNA, and 3' UTR
exons but no introns
'''
#name of fasta file with genes corresponding to BED file 
#(in data_folder)
refseq_input_fasta='test_fasta'


#location of maf_file (in data_folder)
maf_input='multiz11way.maf'

'''
species of interest. Names need to be identical to those in your maf
file, and first species in the list needs to be your reference
(same species as used in your BED file for genes)
'''
species_list="['hg19', 'gorGor3', 'panTro3', 'nomLeu1']"
#species_list="['hg19', 'gorGor3', 'ponAbe2', 'panTro3', 'nomLeu1']"

'''
This is the most involved prep step. In order to call transcripts
from other genomes, you will need to download each genome into a
folder within 'data_folder', and add the names of these genomes to
'genome_species' with the reference genome (the one with the BED 
file) listed first. Large genomes should be separated into at least
20 separate approximately equal sized fasta files (which can each
have individual chromosomes or multiple chromosomes/contigs per
file). I've written a script called 'get_the_fasta_things.py' to help
with this. You will need to cull any extraneous chromosomes/contigs
manually (such as extra haplotypes that tend to make sequences look
duplicated). You will also need to create a text file with a list of
the names of these >=20 fasta files (one fasta file per line) called
chromosome_list and stored in the genome's folder.
'''
genome_species="['human', 'gorilla', 'chimp', 'gibbon']"
genome_paths=[data_folder+genome+'/' for genome in eval(genome_species)]

os.chdir('script_folder')

'''
coordinate_converter.py operates on the BED formatted file from UCSC to get 
rid of extra potentially problematic genes (such as noncoding genes like 
tRNAs, genes without 3' UTRs, genes with multiple 3' UTR exons, genes which 
are annotated with the same name in multiple places in the genome, and, in
the case of the human genome, 'hap' chromosomes which are alternate haplotypes. 
3' UTR coordinates are extracted for genes that pass the filters.
'''
subprocess.call(['python', 'coordinate_converter.py', data_folder, refseq_input_bed, refseq_input_fasta])

'''
filter_for_all_species.py operates on the trimmed maf files, removing maf 
entries that have missing species from the species in species_list.
'''
print "filtering out maf entries that don't have all species present"
subprocess.call(['python', 'filter_for_all_species.py', data_folder, maf_input, species_list])

'''
index_all_chunks.py uses the maf file generated with 
extract_only_all_species.py. The output is a list of MAF entries, their byte 
counts, and their coordinates (relative to the positive strand as BED does 
rather than the current strand as MAF does) in each species.
'''
print "indexing the chunks and sorting by human coordinates"
subprocess.call(['python', 'index_all_chunks2.py', data_folder, species_list])

'''
make_first_lastz_scripts.py operates on the genomes that make up your
maf file. This program creates a set of lastz commands for each
genome, which can be run in parallel or serially.
'''
subprocess.call(['rm', data_folder+'lastz_commands'])
for genome_folder in genome_paths:
	subprocess.call(['python', 'make_first_lastz_scripts.py', data_folder, genome_folder, refseq_input_fasta+'_filtered'])

print 'you will now need to run all of the lastz commands from the "lastz_commands" script',
print 'within your data folder. You may want to parallelize these commands as lastz commands',
print 'on large or repetitive genomes can take a day or more to run. If a job is not finishing',
print 'try splitting the genome into smaller files. When all jobs finish, continue on to main_script2.py'
#exit()

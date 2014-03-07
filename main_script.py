import subprocess
import os
#location of refseq genes bed file.
refseq_input_bed='human_refseq_bed'
#location of refseq genes fasta file
refseq_input_fasta='test_fasta'
#location of maf_file
data_folder='../test_data_folder/'
maf_input='multiz11way.maf'
#species of interest (needs to have names identical to those used in your maf file
#species_list="['hg19', 'gorGor3', 'ponAbe2', 'panTro3', 'nomLeu1']"
species_list="['hg19', 'gorGor3', 'panTro3', 'nomLeu1']"
#ftp locations of the genomes corresponding to your species of interest
#(should be a single gzipped fasta file per genome, with same genome 
#versions as the versions used by your maf file, soft masked or unmasked)

os.chdir('script_folder')
'''
coordinate_converter.py operates on the BED formatted file from UCSC to get 
rid of extra potentially problematic genes (such as noncoding genes like 
tRNAs, genes without 3' UTRs, genes with multiple 3' UTR exons, genes which 
are annotated with the same name in multiple places in the genome, and, in
the case of the human genome, 'hap' chromosomes which are alternate haplotypes. 
3' UTR coordinates are extracted for genes that pass the filters.
'''
subprocess.call(['python', 'coordinate_converter2.py', data_folder, refseq_input_bed, refseq_input_fasta])

'''
********************
At this point, a list of fasta_formatted human refseq genes which passed the 
filters of coordinate_converter.py is downloaded twice from UCSC, once with 
all exons (both protein coding and UTR) in uppercase, and once with proein 
coding exons in uppercase and UTR exons in lowercase. lastz is run to 
compare the file with all exons in uppercase to the fasta files making up 
each primate genome.
*********************
'''


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

exit()

import subprocess
import os
data_folder='../data_folder/'
input_sequence_dict='ancestor_dictionary_nogaps'
ancestor_dict="{'human':'2', 'chimp':'2', 'gorilla':'1', '2':'1', 'gibbon':'1'}"
descendant_dict="{'1':['gibbon', 'gorilla', '2'], '2':['human', 'chimp']}"

os.chdir('script_folder')
'''
count_gains_losses.py uses a dictionary of genes, each of which contains
species, each of which contains sequence to count how many times every 8mer
within every species is present, gained, and lost within every gene. The
output dictionary is populated by genes, which are each a dictionary of
species, which are each a dictionary of eightmers, each of which is a 3 number
summary list: number of times the eightmer is present in that species in that
gene, number of times the eightmer is gained in that species in that gene
relative to the ancestor, and number of times the eightmer is lost in that
species in that gene. Because such a dictionary would be much larger than the
available memory when calculated across the entire list of protein coding genes,
multiple dictionaries of 100 genes each are created. This format is cumbersome but
fully adaptable to gene-specific motif turnover research questions.
'''
subprocess.call(['mkdir', data_folder+'ind_turnover_counts'])
subprocess.call(['python', 'count_gains_losses.py', data_folder, input_sequence_dict, ancestor_dict, descendant_dict])

'''
distributions_by_eightmer.py counts the total number of times every eightmer
had a given 3 number summary (present, gained, lost) across genes for a given
species. All outputs of count_gain_losses.py can be stored in a single file.
The output is a dictionary of eightmers, each of which has a dictionary of 
species, each of which has a dictionary of all 3 number summaries associated
with that species for that eightmer. Each of these dictionaries terminates in
a count of how many genes had that 3 number summary in that species for that
eightmer.
Ex: example_dict['AAAAAAAA']['human'][1,0,0] might return '2' meaning two genes
had a pattern of one 'AAAAAAAA' in human that was neither gained nor lost
relative to its ancestor.
'''
print 'creating distributions by eightmer, this may take a while'
subprocess.call(['python', 'distributions_by_eightmer.py', data_folder])

'''
distribution_sums.py has two outputs. The first is a sum of total sites, 
gains, and losses within each species for each eightmer. The second is a 
sum of total sites, gains and losses summed across species for each 
eightmer.
'''
print 'summing the distributions now'
subprocess.call(['python', 'distribution_sums.py', data_folder])

'''
nearest_neighbor_values.py takes the second output of distribution_sums.py 
and uses it to rank each eightmer's gain and loss rates relative to those 
of all eightmers one mutational step away.
'''
print 'ranking eightmer turnover rates relative to similar eightmers'
subprocess.call(['python', 'nearest_neighbor_values.py', data_folder])

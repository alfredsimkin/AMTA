import sys
import custom
import cPickle
import subprocess
#data_folder='../test_data_folder/'
#species_list=eval("['human', 'gorilla', 'chimp', 'gibbon']")
data_folder=sys.argv[1]
species_list=eval(sys.argv[2])
total_species=len(species_list)
utr_dict=cPickle.load(open(data_folder+'final_utr_dictionary_nogaps'))
dnaml_output=open('dnaml_input', 'w')
dummy_outfile=open('outfile', 'w')
dummy_outtree=open('outtree', 'w')
dummy_infile=open('infile', 'w')
dummy_outfile.close()
dummy_outtree.close()
dummy_infile.close()


phylip_species_list=[]
for species_number, species in enumerate(species_list):
	phylip_species_list.append(species+' '*(10-len(species)))

dnaml_output.write('r\nu\n5\no\n'+str(total_species)+'\ny\nr')
dnaml_output.close()

ancestor_dict={}
fasta_list=[]
for gene in utr_dict:
	alignment_list=[]
	for species in species_list:
		alignment_list.append(utr_dict[gene][species])
		fasta_list.append([gene+'_'+species, utr_dict[gene][species]])
	custom.print_phylip(phylip_species_list, [gene, alignment_list], 'infile')
	subprocess.call(['sh', 'dnaml_script.sh'])
	first_line='big'
	for line_number, line in enumerate(open('outfile')):
		if line.startswith('Probable'):
			first_line=line_number+4
		if line_number>=first_line:
			line=line.split()
			if len(line)>1:
				species, sequence=line[0], ''.join(line[1:])
				if gene not in ancestor_dict:
					ancestor_dict[gene]={}
				if species not in ancestor_dict[gene]:
					ancestor_dict[gene][species]=''
				ancestor_dict[gene][species]+=sequence
custom.print_fasta(fasta_list, data_folder+'fasta_formatted_utrs', 'w')
cPickle.dump(ancestor_dict, open(data_folder+'ancestor_dictionary', 'w'))

first_output=open('eightmer_sums_by_species', 'w')
first_output.write('eightmer\tspecies\ttotal_sites\tgains\tlosses\tgains_by_total\tlosses_by_total\n')
second_output=open('eightmer_sums_across_species', 'w')
second_output.write('eightmer\ttotal_sites\tgains\tlosses\tgains_by_total\tlosses_by_total\n')
import cPickle
eightmer_dict=cPickle.load(open('vert_distributions_by_eightmer'))
summed_eightmer_dict, first_list={}, []
for eightmer in eightmer_dict:
	for species in eightmer_dict[eightmer]:
		total_sum, gain_sum, loss_sum=0,0,0
		for dist in eightmer_dict[eightmer][species]:
			count=eightmer_dict[eightmer][species][dist]
			values=eval(dist)
			values=map(int, values)
			total_sites, total_gains, total_losses=values[0]*count, values[1]*count, values[2]*count
			total_sum+=total_sites
			gain_sum+=total_gains
			loss_sum+=total_losses
		if total_sum!=0:
			gain_by_total=float(gain_sum)/total_sum
			loss_by_total=float(loss_sum)/total_sum
		else:
			gain_by_total, loss_by_total=0,0
		first_list.append(map(str, [eightmer, species, total_sum, gain_sum, loss_sum, gain_by_total, loss_by_total]))
		if eightmer not in summed_eightmer_dict:
			summed_eightmer_dict[eightmer]=[0,0,0]
		for value_number, value in enumerate([total_sum, gain_sum, loss_sum]):
			summed_eightmer_dict[eightmer][value_number]+=value
first_output.write('\n'.join(['\t'.join(line) for line in first_list]))
for eightmer in summed_eightmer_dict:
	string_form=map(str, summed_eightmer_dict[eightmer])
	if summed_eightmer_dict[eightmer][0]!=0:
		gains_by_total=str(float(summed_eightmer_dict[eightmer][1])/summed_eightmer_dict[eightmer][0])
		losses_by_total=str(float(summed_eightmer_dict[eightmer][2])/summed_eightmer_dict[eightmer][0])
		string_form.extend([gains_by_total, losses_by_total])
		second_output.write(eightmer+'\t'+'\t'.join(string_form)+'\n')
	else:
		second_output.write(eightmer+'\t'+'\t'.join(string_form)+'\t0\t0\n')

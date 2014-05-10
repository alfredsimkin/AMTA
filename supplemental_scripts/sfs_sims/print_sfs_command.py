total_time, sequence_length=200, 30000
sfs_table=[line.strip().split() for line in open('sfs_input_table')]
print 'sfs_code', len(sfs_table), '1 -L 1', sequence_length, 
for table_entry in sfs_table:
	species, split, descendants=table_entry
	if descendants!='none':
		descendants=descendants.split('&')
		print '-TS', split, species, str(int(species)+1), '-TE', split, species, '-TS', split, ' '.join(descendants),
print '-TE', total_time

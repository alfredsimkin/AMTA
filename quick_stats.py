mer_list=['sevenmer', 'eightmer', 'ninemer']
for mer_number, mer in enumerate(range(7,10)):
	folder_name='full_'+str(mer)+'mer_counts/'
	real_counts=[line.strip().split('\t')[6:9] for line in open(folder_name+'real_'+mer_list[mer_number]+'_ranked_results')]
	full_counts=[line.strip().split('\t')[6:9] for line in open(folder_name+mer_list[mer_number]+'_nearest_neighbor_values')]
	one_one_real, one_one_full=0,0
	glm_llm_real, glm_llm_full=0,0
	ggm_llm_real, ggm_llm_full=0,0
	glm_lgm_real, glm_lgm_full=0,0
	ggm_lgm_real, ggm_lgm_full=0,0
	big_big_full, big_big_real=0,0
	median=(mer*3+2)/2.0
	big=mer*3+1
	for real in real_counts:
		real=map(int, real)
		if real[1]==1 and real[2]==1:
			one_one_real+=1
		if real[1]<median and real[2]<median:
			glm_llm_real+=1
		if real[1]<median and real[2]>median:
			glm_lgm_real+=1
		if real[1]>median and real[2]<median:
			ggm_llm_real+=1
		if real[1]>median and real[2]>median:
			ggm_lgm_real+=1
		if real[1]==big and real[2]==big:
			big_big_real+=1
	for full in full_counts:
		full=map(int, full)
		if full[1]==1 and full[2]==1:
			one_one_full+=1
		if full[1]<median and full[2]<median:
			glm_llm_full+=1
		if full[1]<median and full[2]>median:
			glm_lgm_full+=1
		if full[1]>median and full[2]<median:
			ggm_llm_full+=1
		if full[1]>median and full[2]>median:
			ggm_lgm_full+=1
		if full[1]==big and full[2]==big:
			big_big_full+=1
	print mer
	print 'one_one_real, one_one_full, glm_llm_real, glm_llm_full, ggm_llm_real, ggm_llm_full, glm_lgm_real, glm_lgm_full, ggm_lgm_real, ggm_lgm_full, big_big_full, big_big_real'
	print one_one_real, one_one_full, glm_llm_real, glm_llm_full, ggm_llm_real, ggm_llm_full, glm_lgm_real, glm_lgm_full, ggm_lgm_real, ggm_lgm_full, big_big_full, big_big_real


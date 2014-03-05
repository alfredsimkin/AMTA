from decimal import Decimal
output_file=open('out', 'w')
prob_list=['1.0', '0.1056', '0.6304', '0.1056', '0.0336', '0.088', '0.4048', '0.6304', '0.2736', '0.4048', '0.1248', '0.088', '0.0448', '0.4048', '0.1456', '0.192', '0.168', '0.664', '0.928', '0.304', '0.192', '0.0576', '0.1248', '0.5952', '0.5584', '0.0448', '0.5584', '0.304', '0.1456', '0.5584', '0.304', '0.016', '0.1056']
items=len(prob_list)
full_grid=[]
observed_successes=21

def grid_into_value(x, y, items):
	return y*items+x
for value in range(len(prob_list)**2):
	x=value%items
	y=value/items
	if x>0:
		previous_x_prob=full_grid[value-1]
	else:
		previous_x_prob=0
	if y>0:
		previous_y_prob=full_grid[grid_into_value(x, y-1, items)]
	else:
		previous_y_prob=0	
	if (x>0 or y>0) and (x+y)<len(prob_list):
		full_grid.append(previous_x_prob*Decimal(prob_list[x+y])+previous_y_prob*(1-Decimal(prob_list[x+y])))
	elif x==0 and y==0:
		full_grid.append(Decimal('1.0'))
	else:
		full_grid.append(Decimal('0.0'))
for final_prob_number, final_prob in enumerate(full_grid):
	final_prob=str(final_prob)
	if final_prob_number%items==items-1:
		output_file.write(final_prob+'\n')
	else:
		output_file.write(final_prob+'\t')
equal_or_better=0
for not_improved in range(items-observed_successes):
	y=not_improved
	x=items-1-y
	equal_or_better=equal_or_better+full_grid[grid_into_value(x,y,items)]
print 'the cumulative probability of', observed_successes, 'or more successes in', items-1, 'trials with your probabilities is', equal_or_better

def sort_by_thing(list1):
	sorting_thing=list1[1][1]
	return sorting_thing
list2=[['A',['g',3]],['B',['c',2]],['C',['b', 4]]]
list2.sort(key=sort_by_thing)
print list2

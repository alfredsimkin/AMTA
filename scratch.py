import cPickle
full_dictionary=cPickle.load(open('final_utr_dictionary'))
print full_dictionary['NM_001080825']
small_dictionary={}
small_dictionary['NM_001080825']=full_dictionary['NM_001080825']
cPickle.dump(small_dictionary, open('NM_001080825', 'w'))

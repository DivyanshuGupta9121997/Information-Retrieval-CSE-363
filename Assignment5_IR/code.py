
def read_bin_file(filename):
	token_list=[]
	with open(filename,'rb') as inp:
		for line in inp:
			token_list.append(line.strip().split())

	return token_list

qrel= read_bin_file('qrels.test')
results = read_bin_file('results.test')

query_ids=list(set([token[0] for token in qrel]))

def get_rel_for_every_doc():
	doc_info={}
	for token in qrel:
		if token[2] in doc_info:
			doc_info[token[2]][token[0]] = token[3]
		else:
			doc_info[token[2]]=dict()
			doc_info[token[2]][token[0]] = token[3]

	for key in doc_info.keys():
		for q_id in query_ids:
			if not q_id in doc_info[key].keys():
				doc_info[key][q_id]='0'
	return doc_info

def get_output_for_every_query():
	query_output={}
	for token in results:
		if token[0] in query_output:
			query_output[token[0]].append([token[2],token[3],token[4],token[5]])
		else:
			query_output[token[0]]=list()
			query_output[token[0]].append([token[2],token[3],token[4],token[5]])

	return query_output

rel_docs = get_rel_for_every_doc()
query_info = get_output_for_every_query()


def sort_query_info():
	sorted_query_info={}
	for key in query_info.keys():
		sorted_query_info[key] = sorted(query_info[key],key=lambda x:int(x[1]) )
	return sorted_query_info

sorted_info = sort_query_info()

def avg_precision_for_query(q_id):
	num_rel=len([doc_id for doc_id in rel_docs.keys() if rel_docs[doc_id][q_id]=='1'])
	#print("Number of relevant docs")
	#print(num_rel)
	cur_num_of_rev =0
	sum_prec =0
	info = sorted_info[q_id]
	for row in info:
		if not row[0] in rel_docs.keys():
			continue
		else:
			if rel_docs[row[0]][q_id] =='1':
				cur_num_of_rev =cur_num_of_rev+1
				sum_prec=sum_prec+(cur_num_of_rev*1.0/float(row[1]))
	
	return sum_prec*1.0/num_rel


def calculate_map():
	sum_avg_prec = 0
	for q_id in query_ids:
		ap=avg_precision_for_query(q_id)
		print("AVERAGE PRECISION FOR " + str(q_id) + " is :-" )
		print(ap)
		sum_avg_prec += ap
	return sum_avg_prec*1.0/len(query_ids)

MAP = calculate_map()
print("\n\nMean Average Precision (MAP) is :- ")
print(MAP)




import os,sys
import math
import functools
import pickle,re,string
from collections import defaultdict
from nltk import clean_html
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
#20news_18828

def store_paths():
	d={}
	i=0
	for root,dirs,files in os.walk('/home/dg/Downloads/Assignment2/20news_18828'):
		if not dirs:
			for f in files:
				d[i]=os.path.join(root,f)
				i=i+1
	return d

path_dict=store_paths()      	 #stores all the file paths
N=len(path_dict)		 #Total number of documents
dictionary=set()	   	 #stores all the term present in vocubalary
postingdict = defaultdict(dict)	 #stores document frequency of each term in the vocubalary
doc_freq=defaultdict(int)
length_doc=defaultdict(float)

characters = " .,!#$%^&*\()/;:\n\t\\\"?!{}[]<>+-='_"
translate_table = dict((ord(char), None) for char in string.punctuation)

def create_posting():
	global dictionary,postingdict
	with open("postingdict2.pkl","rb") as f:
		postingdict=pickle.load(f)
	with open("dictionary2.pkl","rb") as f:
		dictionary=pickle.load(f)

def create_doc_freq():
	global doc_freq
	for term in dictionary:
		doc_freq[term]=len(postingdict[term])
def stemming(doc):
	doclist=doc.split()
	stemmer=PorterStemmer()

	content=""

	for word in doclist:
		word=word.strip(characters)
		elem=stemmer.stem(word.lower())
		content=content + elem + " "
	
	return content

def calc_IDF(term):
	ans=0.0
	if(term in dictionary):
		ans=math.log(N/doc_freq[term],10)
	return(ans)
	
def calc_termWeight(term,docid):
	ans=0.0
	if(docid in postingdict[term]):
		idf=calc_IDF(term)
		tf1=1+math.log(postingdict[term][docid])
		tf2=postingdict[term][docid]
		ans=tf1*idf
	return(ans)


def create_length_doc():
	global length_doc
	for docid in path_dict:
		l=0
		for term in dictionary:
			termWt=calc_termWeight(term,docid)
			l=l+(termWt**2)
		length_doc[docid]=math.sqrt(l)

def create_lengthDoc():
	global length_doc
	with open("length_doc.pkl","rb") as f:
		length_doc=pickle.load(f)
	
		
def cos_similarity(query,docid):
	ans=0
	for term in query:
		if term in dictionary:
			tw=calc_termWeight(term,docid)
			ans=ans + (tw)
	ans=ans/(length_doc[docid])
	return(ans)

def remove_stopwords(doc):
	file1=open('/home/dg/Downloads/Assignment2/english','r')
	l_stopwords = file1.read().split()
	
	content=""
	doclist=doc.split()
	for w in doclist:
		if w.lower() not in l_stopwords:
			content=content + w + " "

	return content

def isStopword(s):
	file1=open('/home/dg/Downloads/Assignment2/english','r')
	l_stopwords = file1.read().split()
	
	if(s.lower() in l_stopwords):
		return True
	else:
		return False


def process_query(s):
	query=s.split()
	docset_of_terms=[]
	
	for term in query:
		docset_of_terms.append( set(postingdict[term].keys()) )
	relevant_docs = functools.reduce(set.intersection,[l for l in docset_of_terms])
	print(relevant_docs)
	
	if not relevant_docs:
		print("Error : No relevant documents found for the query\n")
		return
	else:
		score=sorted([(id,cos_similarity(query,id)) for id in relevant_docs])
		score=sorted(score,key=lambda x:x[1],reverse=True)
		print("All the relevant documents with their Doc-id(s) + ((Cosine Similarity Score)) are as follows-\n\n")
		for (id,sco) in score:
			print(str(id) + " -> " + str(sco) + " : " + path_dict[id])
		print("\n\n")
	
	

create_posting()   	#creating a posting list which is a dict of dict { <term> : {doc_id,doc_freq},{},{},{},......}
create_doc_freq()       #creating a dictionary of Document Frequency  {<term> : int}	
create_lengthDoc()
while(True):
	s=input("\n\nInput query :- ")
	if(s=="___"):
		break	
	s = re.sub(r"\d+", "", s)
	s = s.translate(translate_table)
	s=stemming(s)
	print(s)
	flag=0
	for elem in s.split():
		if isStopword(elem):
			flag=1
			break	
	
	if( len(s.split()) <1 ):
		print("The retrieval system has to query atleast 3 words. \nPlease again enter the query. ")
		continue
	if(flag==1):
		print("Not a Strong Query, try to use query without Stopwords \nPlease again enter the query. ")
		continue
	process_query(s)
	#print("\n--------\nThe final document id(s) satisfying the above query are : \n\n\n",ans)






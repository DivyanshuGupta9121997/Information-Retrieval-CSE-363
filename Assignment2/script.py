import os
import pickle
from collections import defaultdict
from nltk import clean_html
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer

def store_paths():
	d={}
	i=0
	for root,dirs,files in os.walk('/home/dg/Desktop/Assignment2/dataset'):
		if not dirs:
			for f in files:
				d[i]=os.path.join(root,f)
				i=i+1
	return d

path_dict=store_paths()
#print(path_dict)
dictionary=set()
postingdict = defaultdict(dict)
doc_freq=defaultdict(int)
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>+-_"

def create_posting_list():
	global dictionary,postingdict
	
	for i in path_dict:
		print(path_dict[i])
		try:
			f=open(path_dict[i],'r',encoding="utf-8")
			orig_doc=f.read()
			f.close()
		except:
			continue
		doc=remove_stopwords(orig_doc)		
		doc=stemming(doc)		
		#doc=lemmatise(doc)
		t=tokenise(doc)
		
		uniq_terms=set(t)			   #local set of tokens
		dictionary=dictionary.union(uniq_terms)    #global set of tokens

		for elem in uniq_terms:
			postingdict[elem][i]=t.count(elem)
	
#mergethispls
def create_doc_freq():
	global doc_freq
	for term in dictionary:
		doc_freq[term]=len(postingdict[term])

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

def stemming(doc):
	doclist=doc.split()
	stemmer=PorterStemmer()

	content=""

	for word in doclist:
		word=word.strip(characters)
		elem=stemmer.stem(word.lower())
		content=content + elem + " "
	
	return content

def lemmatise(doc):
	doclist=doc.split()
	wnl = WordNetLemmatizer()

	content=""

	for word in doclist:
		word=word.strip(characters)
		elem=wnl.lemmatize(word.lower())
		content=content + elem + " "
	#print(content)
	
	return content			

def tokenise(document):
	terms = document.lower().split()
	return [term.strip(characters) for term in terms]
  



create_posting_list()   #creating a posting list which is a dict of dict { <term> : {doc_id,doc_freq},{},{},{},......}
create_doc_freq()       #creating a dictionary of Document Frequency  {<term> : int}


print("The Posting List of the given dataset is :- \n\n")
print(postingdict)





#input a query
while True:
	s=input("Input a query word :- ")
	elem=""

	if(isStopword(s)):
		print("Given word is a Stopword")
	else:
		stemmer=PorterStemmer()
		elem=stemmer.stem(s.lower())

	#Result
	if(elem!=""):
		print("The posting list of Query word is : ")
		print(postingdict[elem])
		sum_=0
		for v in postingdict[elem].values():
			sum_=sum_+int(v)
		print("The term frequency of the query word is :\n")
		print(sum_)
		print("The document frequency of the query word is :\n")
		print(doc_freq[elem])
	else:
		print("Query Word Not found")
	if(s=="___"):
		break







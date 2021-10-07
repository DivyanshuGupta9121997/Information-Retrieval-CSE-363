import os
from collections import defaultdict
import math
import sys
import re
from nltk import clean_html
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

def store_paths():
	d={}
	i=0
	for root,dirs,files in os.walk('/home/dg/Desktop/Assignment_2_IR/dataset'):
		if not dirs:
			for f in files:
				d[i]=os.path.join(root,f)
				i=i+1
	return d

path_dict=store_paths()
n=len(path_dict)
dictionary=set()
postingdict = defaultdict(dict)
doc_freq=defaultdict(int)
length=defaultdict(float)
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

def create_posting_list():
	global dictionary,postingdict
	
	for i in path_dict:
		#print(path_dict[i])
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
		
		uniq_terms=set(t)
		dictionary=dictionary.union(uniq_terms)

		for elem in uniq_terms:
			postingdict[elem][i]=t.count(elem)
		if(i==3):
			break

def create_doc_freq():
	global doc_freq
	for term in dictionary:
		doc_freq[term]=len(postingdict[term])

def remove_stopwords(doc):
	file1=open('/home/dg/Desktop/Assignment_2_IR/english','r')
	l_stopwords = file1.read().split()
	
	content=""
	doclist=doc.split()
	for w in doclist:
		if w.lower() not in l_stopwords:
			content=content + w + " "

	return content

def isStopword(s):
	file1=open('/home/dg/Desktop/Assignment_2_IR/english','r')
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
create_doc_freq()       #creating a dictionary of Document Frequency


print("The Posting List of the given dataset is :- \n\n")
print(postingdict)

#input a query
s=input("Input a query word :- ")
elem=""

if(isStopword(s)):
	print("Given word is a Stopword")
	sys.exit()
else:
	stemmer=PorterStemmer()
	elem=stemmer.stem(s.lower())

#Result
if(elem!=""):
	print("The posting list of Query word is : ")
	print(postingdict[elem])
	print(doc_freq[elem])
else:
	print("Query Not found")







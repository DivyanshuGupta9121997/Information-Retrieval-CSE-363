import pickle,sys
from nltk import PorterStemmer
from math import sqrt as sqrt
from collections import defaultdict

postingdict = defaultdict(dict)

with open("postingdict.pkl","rb") as f:
	postingdict=pickle.load(f)


total=18828

def postfix(query):
	preced=dict()
	preced['NOT']=3
	preced['AND']=2
	preced['OR']=1
	preced['(']=0
	preced[')']=0

	ans=[]
	
	stack=[]

	for elem in query:
		if(elem == '('):
			stack.append(elem)
			#print(stack)
		elif(elem == ')'):
			op=stack.pop()
			
			while(op!='('):
				ans.append(op)
				op=stack.pop()
		elif( elem in preced ):
			if(len(stack)!=0):
				curr_op=stack[-1]
				
				while(len(stack)!=0 and preced[curr_op]>preced[elem]):
					ans.append(stack.pop())
					if(len(stack)!=0):
						curr_op=stack[-1]
			stack.append(elem)
		else:
			ans.append(elem)
			#print(stack,ans)

	while(len(stack)!=0):
		ans.append(stack.pop())

	return ans

			
def booleanAND(l,r):
	#perform merge

	res=[]
	i=0
	j=0
	

	while( i<len(l) and j<len(r) ):
		lval = l[i]
		rval = r[j]
		
		if(lval == rval):
			res.append(lval)
			i=i+1
			j=j+1
		elif(lval > rval):
			j=j+1
		else:
			i=i+1
	return(res)
				
def booleanOR(l,r):
	res=[]
	i=0
	j=0
	
	while(i<len(l) and j<len(r)):
		lval=l[i]
		rval=r[j]
		
		if(lval==rval):
			res.append(lval)
			i=i+1
			j=j+1
		elif(lval < rval):
			res.append(lval)
			i=i+1
		else:
			res.append(rval)
			j=j+1
		
	while(i<len(l)):
		res.append(l[i])
		i=i+1
	while(j<len(r)):
		res.append(r[j])
		j=j+1
	
	return res
			
def booleanNOT(r):
	global total
	l=[]
	for i in range(total):
		l.append(i)
		
	res=set(l)-set(r)
	res=list(res)
	res=sorted(res)
	return res

def isStopword(s):
	file1=open('/home/dg/Videos/Assignment3_IR/english','r')
	l_stopwords = file1.read().split()
	
	if(s.lower() in l_stopwords):
		return True
	else:
		return False

def process_query(query):
	stemmer=PorterStemmer()
	
	q=query.replace('(',' ( ')
	q=q.replace(')',' ) ')
	
	q=q.split()	
	
	l=postfix(q)	
	print("The postfix form is :\n",l)
	
	finalstack=[]	
	
	for token in l:
		res=[]
		
		if(token!="AND" and token!="OR" and token!="NOT"):
			token=stemmer.stem(token.lower())

			if(token in postingdict):
				res=sorted(postingdict[token])
		elif(token == "AND"):
			r=finalstack.pop()
			l=finalstack.pop()
			res= booleanAND(l,r)

		elif(token == "OR"):
			r=finalstack.pop()
			l=finalstack.pop()
			res=booleanOR(l,r)
		
		elif(token == "NOT"):
			r=finalstack.pop()
			res=booleanNOT(r)	
		
		finalstack.append(res)
				

	return(finalstack.pop())	

while(True):
	s=input("\n\nInput query :- ")
	if(s=="___"):
		break
	t=s
	t=t.replace('(',' ')
	t=t.replace(')',' ')
	t=t.replace("AND",' ')
	t=t.replace("OR",' ')
	t=t.replace("NOT",' ')	
	
	flag=0
	for elem in t.split():
		if isStopword(elem):
			flag=1
			break
		
	
	if( len(t.split()) <3 ):
		print("The retrieval system has to query atleast 3 words. \nPlease again enter the query. ")
		continue
	if(flag==1):
		print("Not a Strong Query, try to use query without Stopwords \nPlease again enter the query. ")
		continue
	ans=process_query(s)
	print("\n--------\nThe final document id(s) satisfying the above query are : \n\n\n",ans)
	


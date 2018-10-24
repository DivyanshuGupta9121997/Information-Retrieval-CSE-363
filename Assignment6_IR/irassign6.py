
# coding: utf-8
# life

# In[13]:


import os


# In[12]:


from sklearn.feature_extraction.text import TfidfVectorizer
sklearn_tfidf = TfidfVectorizer()


# In[95]:


import string
import re


# In[121]:


tran_tab=dict((ord(char), ' ') for char in string.punctuation)


# In[122]:


def remove_stopwords(doc):
    doc=re.sub(r"\d+"," ",doc)
    doc=doc.translate(tran_tab)
    file1=open('english','r')
    l_stopwords = file1.read().split()

    content=[]
    doclist=nltk.word_tokenize(doc)
    for w in doclist:
        if w.lower() not in l_stopwords:
            content.append(w)

    return content


# In[79]:


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
 
def remove_stop(example_sent):
 
    stemmer = PorterStemmer()
    word_tokens = remove_stopwords(example_sent)
    singles = [stemmer.stem(plural) for plural in word_tokens]
    return singles


# In[123]:


import codecs
all_docs = []
doc_ids = []
for root, dirs, files in os.walk("20_newsgroups/comp.graphics"):
    for name in files:
        try:
            all_docs.append(' '.join(remove_stop(codecs.open(os.path.join(root, name), 'r', encoding='utf-8').read())))
            doc_ids.append(name)
        except:
            continue


# In[143]:


sklearn_representation = sklearn_tfidf.fit_transform(all_docs).toarray()


# In[202]:


all_docs[0]


# In[199]:


def get_vectors(list_sen):
    return sklearn_tfidf.fit_transform(list_sen).toarray()


# In[210]:


def get_vector_for(doc_id, dataset):
    return dataset[doc_id]


# In[150]:


import numpy as np


# In[318]:


def find_min_ind(point, kmeans):
    min_ind = 0
    min_dist = np.linalg.norm(point - kmeans[0])
    for i in range(1, len(kmeans)):
        dist = np.linalg.norm(point - kmeans[i])
        if dist < min_dist:
            min_dist = dist
            min_ind = i
#         print(dist, "TRIVEDI")
    return min_ind


# In[319]:


def find_centroid(vector):
    sum = 0
    sum += np.sum(vector, axis = 0)
    sum /= len(vector)
    return sum


# In[328]:


def single_loop(dataset, kmeans):
    bin = [[] for i in range(len(kmeans))]
    for j,point in enumerate(dataset):
        min_ind = find_min_ind(point, kmeans)
        bin[min_ind].append(j)
#         print(min_ind, " RAg")
    kmeans_new = []
    for i in bin:
        new_vector = []
        for j in i:
            new_vector.append(get_vector_for(j, dataset))
        kmeans_new.append(find_centroid(new_vector))
#         print(find_centroid(new_vector))
    print(np.sum(np.sum(np.array(kmeans_new) - np.array(kmeans), axis = 1)))
#     kmeans_new = [[find_centroid(get_vector_for(i, dataset))] for i in bin]
    return kmeans_new, bin


# In[330]:


def asli_kmeans(k, dataset):
    kmeans = dataset[:k]
#     kmeans = random.sample(list(dataset), k)
    print(kmeans)
    for i in range(100):
        kmeans, bin = single_loop(dataset, kmeans)
    print(kmeans)
    return kmeans, bin


# In[280]:


dataset = get_vectors(["cricket bat", "cricket ram","football",  "ronaldo football"])
kmeans = dataset[:2]


# In[291]:


find_min_ind(dataset[2], kmeans)


# In[308]:


find_centroid([dataset[0], dataset[2], dataset[3]]) - dataset[0]


# In[333]:


k = int(input())
kmeans, bin = asli_kmeans(k, sklearn_representation)


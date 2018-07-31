# -*- coding: utf-8 -*-
import codecs
import re
import sys
class Tokenizer():

	def __init__(self,text=None):
		if text is  not None:
			self.text=text.decode('utf-8')
			self.clean_text()
		else:
			self.text=None
		self.sentences=[]
		self.tokens=[]
		self.stemmed_word=[]
		self.final_list=[]
		self.final_tokens=[]
	
	def generate_sentences(self):
		text=self.text
		self.sentences=text.split(u"।")

	def print_sentences(self,sentences=None):
		if sentences:
			for i in sentences:
				sys.stdout.write( i.encode('utf-8') + " ")
		else:
			for i in self.sentences:
				sys.stdout.write( i.encode('utf-8') + " ")


	def clean_text(self):
		text=self.text
		text=re.sub(r'(\d+)',r'',text)
		text=text.replace(u',','')
		text=text.replace(u'"','')
		text=text.replace(u'(','')
		text=text.replace(u')','')
		text=text.replace(u'"','')
		text=text.replace(u':','')
		text=text.replace(u"'",'')
		text=text.replace(u"‘‘",'')
		text=text.replace(u"’’",'')
		text=text.replace(u"''",'')
		text=text.replace(u".",'')
		self.text=text

	def remove_only_space_words(self):
		tokens=filter(lambda tok: tok.strip(),self.tokens)
		self.tokens=tokens
		
	def hyphenated_tokens(self):

		for each in self.tokens:
			if '-' in each:
				tok=each.split('-')
				self.tokens.remove(each)
				self.tokens.append(tok[0])
				self.tokens.append(tok[1])



	def tokenize(self):
		if not self.sentences:
			self.generate_sentences()

		sentences_list=self.sentences
		tokens=[]
		for each in sentences_list:
			word_list=each.split(' ')
			tokens=tokens+word_list
		self.tokens=tokens
		#remove words containing spaces
		self.remove_only_space_words()
		#remove hyphenated words
		self.hyphenated_tokens()

	def print_tokens(self,print_list=None):
		if print_list is None:
			for i in self.tokens:
				sys.stdout.write( i.encode('utf-8') + " ")
		else:
			for i in print_list:
				sys.stdout.write( i.encode('utf-8') + " ")






	def generate_stem_words(self,word):
		suffixes = {
    1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
    2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],
    3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
    4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
    5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"],
}
		for L in 5, 4, 3, 2, 1:
			if len(word) > L + 1:
				for suf in suffixes[L]:
					#print type(suf),type(word),word,suf
					if word.endswith(suf):
						#print 'h'
						return word[:-L]
		return word

	def generate_stem_dict(self):


		stem_word={}
		if not self.tokens:
			self.tokenize()
		for each_token in self.tokens:
			#print type(each_token)
			temp=self.generate_stem_words(each_token)
			#print temp
			stem_word[each_token]=temp
			self.stemmed_word.append(temp)
			
		return stem_word

	def stem_words(self):

		tokens=[i for i in self.stemmed_word if unicode(i)]
		self.final_tokens=tokens
		return tokens


if __name__=="__main__":
	t=Tokenizer(open("input.txt","r").read())
	
	t.generate_sentences()
	t.tokenize()
	#f=t.generate_freq_dict()
	#s=t.concordance('बातों')
	f=t.generate_stem_dict()

	z=t.stem_words()
	t.print_tokens(t.final_tokens)


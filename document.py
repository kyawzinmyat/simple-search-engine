import json
import re
import string



class Document:
	def __init__(self):
		self.combined_data_doc = self.prepare()
		self.inverted_index={}
	
	
	
	def prepare(self):
		with open("original_doc.json","r") as file:
				self.original_doc= json.load(file)
		return self.original_doc.copy()
	

	
	def tokenize(self):
		stop_words=["the","a","an","and","of","not","is","are","were","was","but","etc","hence","those","these","there","very","in","it's","am","are","among","on","from","in","at","others","other","it","s","because","to","its","how","if","you","i"]## nltk 
		for title,doc in self.combined_data_doc.items():
			doc=doc.lower()
			doc = re.sub("[%s]"%re.escape(string.punctuation)," ",doc)
			doc = doc.split(" ")
			doc = [char for char in doc if char not in stop_words]
			self.combined_data_doc[title]=doc
			
	def n_gram(self,tokens,min=1):
		terms={}
		for pos,token in enumerate(tokens):
			for size in range(min,len(token)+1):
				terms.setdefault(token[:size],set(()))
				terms[token[:size]].add(pos)
		return terms
	
	def stem(self):
		self.tokenize()
		for title,data in self.combined_data_doc.items():
			for term in self.n_gram(data):
				self.inverted_index.setdefault(term,[])
				self.inverted_index[term].append(title)
		self.load_inverted_index()
		
	def load_inverted_index(self,name="inverted_index2"):
			with open(f"{name}.json","w+") as file:
				json.dump(self.inverted_index,file,indent=4)
			
doc = Document()
#doc.combine_data()
doc.stem()			
#	
		
		
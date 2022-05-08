import re
import string
import json

class Search:
	def __init__(self):
		self.set_inverted_index()
	
	def set_inverted_index(self):
		with open("inverted_index2.json","r") as file:
			self.inverted_index = json.load(file)
		
			


class Query:
	def __init__(self,query):
			self.query=query
			self.tokens=""
			self.inverted_index=Search().inverted_index
	
	def tokenize(self):
		stop_words=["the","a","an","and","of","not","is","are","were","was","but","etc","hence","those","these","there","very","in","it's","am","are","among","on","from","in","at","others","other","it","s","because","to","its","how","if","you","i"]## nltk 
		self.tokens=self.query.lower()
		self.tokens = re.sub("[%s]"%re.escape(string.punctuation)," ",self.tokens)
		self.tokens = self.tokens.split(" ")
		self.tokens = [char for char in self.tokens if char not in stop_words]
	
	def find_doc_in_original_docs(self,docs_lists):
		result=[]
		links=[]
		with open("original_doc.json","r") as file:
			data = json.load(file)
		for doc in docs_lists:
			if data[doc] not in links:
				result.append(data[doc])
				links.append(doc)
		return result
	
	def find_smallest(self,doc_lists):
		try:
			return min(doc_lists,key=len)
		except:
			return []
		
		
				
				
	def intersected_match(self,doc_lists):
		result=set()
		small_list = self.find_smallest(doc_lists)
		for doc in small_list:
			for docs in doc_lists:
				if doc in docs:
					result.add(doc)
		return self.find_doc_in_original_docs(result)
			
		
	def search(self):
		self.tokenize()
		doc_lists=[]
		for term in self.tokens:
			try:
				doc_lists.append(self.inverted_index[term])
			except:
				pass
		
		return self.intersected_match(doc_lists)

	

			
			
query=Query("Olivia Rodrigo")
for link in query.search():
			print(link[:80])
			print()
			
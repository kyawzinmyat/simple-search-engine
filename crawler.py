import bs4
import requests
import lxml
import re
import json
from collections import deque

class Crawler:
	def __init__(self,term=""):
		self.term=term
		self.urls =[]
		self.docs={}
		self.crawled_link=[]
		self.links=deque()
		self.base_url="https://en.m.wikipedia.org/wiki/Olivia_Rodrigo"
		
	def crawl(self):
		response =  requests.get(self.base_url+self.term)
		if response:
			soup = bs4.BeautifulSoup(response.text,"lxml")
			self.load_doc(self.base_url+self.term,soup.findAll("p"))
			links = soup.findAll("a",href=re.compile("^/wiki/"))
			for link in links:
				if link.attrs["href"]:
					if link.attrs["href"] not in self.links and link.attrs["href"] not in self.crawled_link:
						self.links.append(link.attrs["href"])
						self.crawled_link.append(self.term)
			self.load_doc_json()
	
	def load_doc(self,key,value):
		self.docs[key]="".join(i.text for i in value)
		
	def load_doc_json(self):
		with open("original_doc.json","w+") as doc:
			json.dump(self.docs,doc)
		
	def _crawl(self):
		while self.links:
			term = self.links.popleft()
			response = requests.get(self.base_url+term)
			if response:
				soup = bs4.BeautifulSoup(response.text,"lxml")
				links = soup.findAll("a",href=re.compile("^/wiki/"))
				for link in links:
					if link.attrs["href"]:
						if link.attrs["href"] not in self.links and link.attrs["href"] not in self.crawled_link and "olivia" in link.attrs["href"]:
							self.links.append(link.attrs["href"])
							self.crawled_link.append(term)
	
							
				
			
		#print(response)


c = Crawler()
c.crawl()
#print(c.links)

#print(len(c.crawled_link))
#print(c.docs)
#print(c.links[0])
#response = requests.get(c.links[8])
#print(response)



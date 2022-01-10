import discord
from discord.ext import commands
from dotenv import load_dotenv
import csv
import requests
from bs4 import BeautifulSoup

headers = {"user-agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36;", "from": "Throwaway69420Email@protonmail.com"}

def SetProduct(url, member):
	
	'''
	if not checkRedundancies(url):
		return "redundant"
	'''

	try:
		#page = the url request
		page = requests.get(url, headers = headers)
		pageContent = page.content
		soup = BeautifulSoup(pageContent, "html.parser")
		
		nameContent = soup.find("div", class_="title-brand")
		name = nameContent.find_next("h1").get_text()
	
		if name == None:
			name = "No Name"
			
		priceContent = soup.find("span", class_="price price--withoutTax").get_text()
		price = priceContent[1:]
		if price == None:
			price = "No Price"

		price = float(price)
		print(name, price)
		MTGProduct = Product(name, price, url, member)
		writeToCSV(MTGProduct)
		return MTGProduct

	except:
		return None

	#loop through somehow

def writeToCSV(product):
	with open("MTGPrices.csv", mode="a+", newline="") as MTGFile:
		writer = csv.writer(MTGFile)
		writer.writerow([product.name, product.price, product.url, product.requestor])

def checkRedundancies(url):
	with open("MTGPrices.csv", mode="r", newline="") as MTGFile:
		reader = csv.reader(MTGFile)
		for Product in reader:
			if Product[2] == url:
				return False

	return True

def checkPrices():

	outputText = ""

	names = []
	prices = []
	urls = []
	users = []

	"""
	NOTES
	lines = list()
	with open('mycsv.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    for row in reader:
        lines.append(row)
        for field in row:
            if field == members:
                lines.remove(row)
	with open('mycsv.csv', 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(lines)
	"""

	with open("MTGPrices.csv", mode="r", newline="") as MTGFile:
		reader = csv.reader(MTGFile)
	
		for Product in reader:

			try:
				#page = the url request
				page = requests.get(Product[2], headers = headers)
				pageContent = page.content
				soup = BeautifulSoup(pageContent, "html.parser")
		
				priceContent = soup.find("span", class_="price price--withoutTax").get_text()
				price = priceContent[1:]
				if price != Product[1]:
					outputText += Product[0] + " WAS $" +  Product[1] + " NOW " + str(price)
					
				price = float(price)

				names.append(Product[0])
				prices.append(price)
				urls.append(Product[2])
				users.append(Product[3])

			except:
				return "ERROR"
				
	with open("MTGPrices.csv", mode="w", newline="") as MTGFile:
		writer = csv.writer(MTGFile)
		
		for x in range(len(names)):
			writer.writerow([names[x], prices[x], urls[x], users[x]])

	return outputText

class Product:
	"""description of class"""

	requestor = None
	url = ""
	name = "Null"
	price = -1

	def __init__(self, name, price, url, requestor):
		self.name = name
		self.price = price
		self.url = url
		self.requestor = requestor

if __name__ == "__main__":
	print("This is not the correct file to run")
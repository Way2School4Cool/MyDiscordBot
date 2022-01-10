from mtgsdk import *

from bs4 import BeautifulSoup
import requests

headers = {"user-agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36;", "from": "Throwaway69420Email@protonmail.com"}
urlStart = "https://www.mtggoldfish.com/price/"


def scrape(set, card):

	#break card into individual letters
	card = list(card)

	for x in range(0, len(card)):
		if card[x] == "'" or card[x] == ",":
			del card[x]
			break
		if card[x] == "/":
			card = card[:x-1]
			break

	card = "".join(card)

	fullURL = urlStart + set + "/" + card

	#page = the url request
	page = requests.get(fullURL, headers= headers)
	pageContent = page.content
	soup = BeautifulSoup(pageContent, "html.parser")

	#find the wrapper for the content you are looking for
	try:
		content = soup.find("div", class_="price-box-price").get_text()
	except:
		content = "$ 0.00"

	return content

def generateBooster(set):
	try:

		#generate cards from a set
		cards = Set.generate_booster(set)
		setName = Set.find(set).name
		totalPrice = 0.00
		totalText = ""


		for card in cards:
			totalText += card.name + ": "

			price = scrape(setName, card.name)
			totalText += price + "\n"
			totalPrice += (float) (price[1:])

		totalText += ("Total Value: $" + str(round(totalPrice, 2)))

		return totalText

	except:
		return "Set not found (note: this api is weird about packs)"



if __name__ == "__main__":
	cards = Set.generate_booster("CMR")
	setName = Set.find("CMR").name
	totalPrice = 0.00


	for card in cards:
		
		print(card.name, end = ": ")

		price = scrape(setName, card.name)
		print(price)
		totalPrice += (float) (price[1:])

	print("Total Value: $" + str(round(totalPrice, 2)))
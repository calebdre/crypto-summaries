import requests
import re
from pyquery import PyQuery as pq
import json
import os
from fetch_coin_data import get_market_cap_data, get_crypto_compare_coin_list

def get_description(url):
	page = requests.get(url).text
	page = [line for line in page.split("\n") if 'pageInfo.setCoinPageInfo({"Res' in line][0]
	page = page[page.find('{"Response'):]
	page = page.replace('\\"',"")
	page = page.replace(" ", " ")
	page = page[0:page.find(',"Subs":')]
	page += "}}"
	j = json.loads(page)
	try:
		descriptionHtml = j["Data"]["General"]["Description"]
		if not descriptionHtml:
			descriptionHtml = j["Data"]["ICO"]["Description"]	
	except:
		descriptionHtml = j["Data"]["ICO"]["Description"]
	
	if not descriptionHtml:
		return ""

	text = pq(descriptionHtml).text()
	return ".".join(text.split(".")[0:4])

def init():
	print("Fetching coinmarketcap")
	market_cap = get_market_cap_data()
	print("Fetching crypto compare")
	crypto_compare_coins = get_crypto_compare_coin_list()
	print("transforming market cap data")
	market_cap = [c["symbol"] for c in market_cap]
	print("transforming crypto compare data")
	crypto_compare_coin_names = [coin for coin in crypto_compare_coins["Data"]]

	all_collected_files = os.listdir("./reference")
	collected_files = []
	for f in all_collected_files:
		if len(f.split("-")) == 1 or f.split("-")[0] in collected_files:
			continue
		collected_files.append(f.split("-")[0])

	market_cap_crypto_compare_shared = list(set(crypto_compare_coin_names) & set(market_cap))
	missing_from_shared = list(set(market_cap_crypto_compare_shared) - set(collected_files))

	print("\n\n" + str(len(missing_from_shared)) + " coins are missing from shared.")
	print("fetching them now.\n\n")
	no_descriptions = []
	missing_coins = [crypto_compare_coins["Data"][coin] for coin in missing_from_shared]
	for i, coin in enumerate(missing_coins):
		symbol = coin["Symbol"]
		name = coin["CoinName"]
		url = "https://www.cryptocompare.com" + coin["Url"]

		print("Getting page for " + name + " (" + str(i) + "/" + str(len(missing_coins)) + ")")
		description =  get_description(url)
		if not description:
			print("no description for " + name)
			no_descriptions.append(name)
			continue
		splitted = description.split(".")
		splitted = [item + "." for item in splitted]

		for i in range(1, len(splitted)):
			sentences = ". ".join(splitted[0:i])
			filename = 'reference/' + symbol + '-' + str(i) + '.txt'
			with open(filename, 'w') as the_file:
				print("Writing " + str(i) + " lines to " + filename)
				the_file.write(sentences)

	print("\n\nThere are not descriptions for these coins: " + ",".join(no_descriptions))

if __name__ == "__main__":
	init()
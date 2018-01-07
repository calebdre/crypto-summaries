import requests
import shutil
from pyquery import PyQuery as pq
import os
import json
from fetch_coin_data import get_market_cap_data

reference_dir = "./reference"
json_dir = "./json"
reference_files = os.listdir(reference_dir)
reference_file_ext = ".txt"

def get_file(filename, predicate=None):
	partial = reference_dir + "/" + filename
	if predicate != None:
		partial += predicate()
	
	return partial

print("formatting coin data")
market_cap_data_mapped_by_symbol = {}
market_cap_data = get_market_cap_data()
for coin in market_cap_data:
	market_cap_data_mapped_by_symbol[coin["symbol"]] = coin

if os.path.exists(json_dir):
	coins_already_mapped_to_json = [c[:-5] for c in os.listdir(json_dir)]
else:
	coins_already_mapped_to_json = []

# for each reference coin, get the corrosponding marketcap data
coin_infos = []
for reference_file in reference_files:
	if len(reference_file.split("-")) > 1:
		continue
	
	coin = reference_file[:-len(reference_file_ext)]
	if coin not in market_cap_data_mapped_by_symbol.keys() or market_cap_data_mapped_by_symbol[coin]["symbol"] in coins_already_mapped_to_json:
		continue
	
	coin_item = market_cap_data_mapped_by_symbol[coin]
	with open(get_file(reference_file), "r") as f:
		descriptions = {}
		for line in f.readlines():
			sentences = len(line.split("."))
			line = line.replace("\n", "")
			descriptions[sentences] = line
		
		coin_item["descriptions"] = descriptions
	
	coin_infos.append(coin_item)

print("getting more data for each coin")
# filter data by requirements

if not os.path.exists(json_dir):
	os.makedirs(json_dir)

transformed_coin_info = []
for coin_info in coin_infos:
	print("getting data for " + coin_info["id"])
	page = requests.get("https://coinmarketcap.com/currencies/" + coin_info["id"]).text
	html = pq(page)
	website = html("span[title='Website']:first + a").attr("href")
	image = "https://files.coinmarketcap.com/static/img/coins/64x64/" + coin_info["id"] + ".png"
	explorer = html("span[title='Explorer']:first + a").attr("href") 

	mapped_coin_info = {
		"coin": coin_info["name"],
		"symbol": coin_info["symbol"],
		"website": website,
		"image": image,
		"explorer": explorer,
		"descriptions":  coin_info["descriptions"]
	}

	json_string = json.dumps(mapped_coin_info)
	with open(json_dir + "/" + mapped_coin_info["symbol"] + ".json", "w+") as f:
		f.write(json_string)
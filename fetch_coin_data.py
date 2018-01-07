import requests
import json
import os

cache_dir = "./cache/" 
market_cap_file_name = "coin_market_cap.json"
crypto_compare_file_name = "crypto_compare.json"

def get_market_cap_data():
	data = fetch_from_cache(market_cap_file_name)
	if data is not None:
		print("fetched cached marketcap data")
		return data

	pages = 6
	num_of_coins = 1385
	coins_per_page = num_of_coins / pages
	data = []
	url = "https://api.coinmarketcap.com/v1/ticker/?start=0&limit=1385"
	print("fetching marketcap data")
	data = requests.get(url).json()
	cache(data, market_cap_file_name)
	return data

def get_crypto_compare_coin_list():
	data = fetch_from_cache(crypto_compare_file_name)
	if data is not None:
		print("fetched cached cryptocompare data")
		return data
	
	print("fetching cryptocompare data")
	crypto_compare_coins = requests.get("https://min-api.cryptocompare.com/data/all/coinlist").json()
	cache(crypto_compare_coins, crypto_compare_file_name)
	return crypto_compare_coins

def cache(data, name):
	if not os.path.exists(cache_dir):
		os.makedirs(cache_dir)
		
	with open(cache_dir + name, "w+") as f:
		f.write(json.dumps(data))

def fetch_from_cache(name):
	if os.path.exists(cache_dir + name):
		with open(cache_dir + name, "r") as f:
			json_data = f.readline()
			if json_data:
				return json.loads(json_data)
	return None

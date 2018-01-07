import os 

reference_folder = "./reference"
output_file_path = "./index.html"
reference_files = os.listdir(reference_folder)
reference_file_ext = ".txt"

if os.path.exists(output_file_path): os.remove(output_file_path)

def get_file(filename, predicate=None):
	partial = reference_folder + "/" + filename
	if predicate != None:
		partial += predicate()
	
	return partial + reference_file_ext

def generate_all_summaries_file(coin, lines):
	all_summaries = []
	for line in lines:
		with open(get_file(coin, lambda: "-" + line), "r") as f:
			all_summaries.append(f.read())
	
	f = get_file(coin)
	if os.path.exists(f): os.remove(f)
	with open(f, "w+") as f:
		f.write("\n".join(all_summaries))

output_file_content = ["<h1>An API for short summaries of key features of all crypto currencies</h1>"]
output_file_content.append("<ul>")
output_file_content.append("<li><a target='_blank' href='https://s3.amazonaws.com/crypto-summaries/all_coins'>All coins (json)</a></li>")

reference_file_map = {}

for f in reference_files:
	splitted = f.split("-")
	if len(splitted) == 1:
		continue
	coin = splitted[0]
	line = splitted[1][0]
	if coin not in reference_file_map.keys():
		reference_file_map[coin] = [line]
	else:
		reference_file_map[coin].append(line)


for key in sorted(reference_file_map.keys()):
	links = ["<a target='_blank' href='" + get_file(key, lambda: "-" + line) + "'>" + line + "</a>" for line in reference_file_map[key]]
	
	if len(reference_file_map[key]) > 1:
		generate_all_summaries_file(key, reference_file_map[key])
		links.append("<a target='_blank' href='" + get_file(key) + "'>all</a>")
	links.append("<a href='https://s3.amazonaws.com/crypto-summaries/" + key + ".json'>json</a>")
	links_stirng = "&nbsp;".join(links)
	output_file_content.append("<li>" + key + " (" + links_stirng + ")</li>")

output_file_content.append("</ul>")
output_file_content.append("<h3><a href='https://github.com/calebdre/crypto-summaries/'>Pull Requests welcome</a><h3>")
output_file_content.append("<h5>Webdesign and development by <a href='https://caleblewis.me'>Caleb Lewis</a><h5>")

with open(output_file_path, "w") as output_file:
    output_file.write("\n".join(output_file_content))

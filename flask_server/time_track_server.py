from flask import Flask, jsonify,request
import time, tldextract, json, requests

app = Flask(__name__)


file = open('data.json', 'r')
website_dict = json.load(file)
url_timestamp = {}
prev_url = ""


def url_domain(url):
	url_list = tldextract.extract(url)
	domain_name = url_list.domain + '.' + url_list.suffix

	if(domain_name == '.'):
		return "EMPTY_DOMAIN_NAME"
	else:
		return domain_name

dont_track = ["EMPTY_DOMAIN_NAME", "newtab."]


@app.route('/send_url', methods=['POST'])
def send_url():
	resp_json = request.get_data()
	params = resp_json.decode()
	url = params.replace("url_for_time=", "")
	print("Open website: " + url_domain(url))
	parent_url = url_domain(url)

	global url_timestamp
	global website_dict
	global prev_url

	if(parent_url not in website_dict.keys()) and (parent_url not in dont_track):
		website_dict[parent_url] = {'time_spent' : 0, 'score' : 0, 'topic' : ""}

	if(prev_url != '') and (prev_url not in dont_track):
		time_spent = int(time.time() - url_timestamp[prev_url])
		website_dict[prev_url]['time_spent'] += time_spent

	x = int(time.time())
	url_timestamp[parent_url] = x
	prev_url = parent_url
	#print("Total viewtimes: ", website_dict)

	with open('data.json', 'w') as file:
		json.dump(website_dict, file, indent=4)

	return jsonify({'message': parent_url + 'time logged'}), 200


@app.route('/scroll_update', methods=['POST'])
def scroll_update():
	resp_json = request.get_json()

	parent_url = url_domain(resp_json['url'])
	scroll_dist = resp_json['scroll_dist']

	print("Scroll recorded on: " + url_domain(parent_url) + ", dist = " + str(scroll_dist))

	return jsonify({'message': parent_url + 'scroll logged'}), 200


app.run(host='0.0.0.0', port=5000)
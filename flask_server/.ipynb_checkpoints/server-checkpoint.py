from flask import Flask, jsonify,request
import time, tldextract, json, requests
import pickle
import pprint
from IPy import IP
from collections import defaultdict
import itertools  #used to slice a dictionary

app = Flask(__name__)

path_history = './../data/history.data'

try:
	with open(path_history, 'rb') as f:
		website_dict = pickle.load(f)
except:
	website_dict = {}

url_timestamp = {}
prev_url = ""

skip_domains = [
    'www.mail.google.com',
    'www.mail.yahoo.com',
    'www.account.google.com',
    'www.facebook.com',  
    'www.docs.google.com'
]

def isIP(str):
    try:
        IP(str)
    except ValueError:
        return False
    return True


def clean_url(url):
	url_list = tldextract.extract(url)
	domain_name = url_list.domain + '.' + url_list.suffix

	if(domain_name == '.'):
		return "EMPTY_DOMAIN_NAME"
	
	spltAr = url.split("://");
	protocol = spltAr[0]
	if protocol not in ['http', 'https']:
		return "DO_NOT_TRACK"
	i = (0,1)[len(spltAr)>1];
	dm = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower();
	if dm[0:4] != 'www.':
		# check if domain is ip address
		if isIP(dm):
			return "DO_NOT_TRACK"
		dm = 'www.' + dm
	# domain checks
	if dm in skip_domains:
		return "DO_NOT_TRACK"
	return url
	

dont_track = ["EMPTY_DOMAIN_NAME", "newtab.", "DO_NOT_TRACK"]


@app.route('/send_url', methods=['POST'])
def send_url():
	resp_json = request.get_data()
	params = resp_json.decode()
	url = params.replace("url_for_time=", "")
	print("Open website: " + clean_url(url))
	parent_url = clean_url(url)

	global url_timestamp
	global website_dict
	global prev_url

	if(parent_url not in website_dict.keys()) and (parent_url not in dont_track):
		website_dict[parent_url] = {'time_spent' : 0,
									   'scroll_dist' : 0}

	if(prev_url != '') and (prev_url not in dont_track):
		time_spent = int(time.time() - url_timestamp[prev_url])
		website_dict[prev_url]['time_spent'] += time_spent

	#print('Time on ' + prev_url + ' : ' + str(website_dict[prev_url]['time_spent']))

	x = int(time.time())
	url_timestamp[parent_url] = x
	prev_url = parent_url



	with open(path_history, 'wb') as f:
		 pickle.dump(website_dict, f)
			
	pprint.pprint(website_dict)

	return jsonify({'message': parent_url + 'time logged'}), 200


@app.route('/scroll_update', methods=['POST'])
def scroll_update():
	resp_json = request.get_json()

	parent_url = clean_url(resp_json['url'])
	scroll_dist = resp_json['scroll_dist']

	if(parent_url not in website_dict.keys()) and (parent_url not in dont_track):
		website_dict[parent_url] = {'time_spent' : 0,
									   'scroll_dist' : scroll_dist}
	else:
		website_dict[parent_url]['scroll_dist'] += scroll_dist

	print("Scroll on: " + clean_url(parent_url) + " : " + str(scroll_dist))

	return jsonify({'message': parent_url + 'scroll logged'}), 200


app.run(host='0.0.0.0', port=5000)
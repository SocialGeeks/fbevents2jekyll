#!/usr/bin/env python2

import json
import urllib
from datetime import datetime

def getFile(name):
	f = open(name, "r")
	file = f.read()
	f.close()
	return file 

def retrievePicture(source, destination):
	if source is not None:	
		urllib.urlretrieve(source, destination)

json_file = "sg_events.json"
events = json.loads(getFile(json_file))

template_file = "template.md"
template_original = getFile(template_file)

for event in events["data"]:
# name, description, start_time, end_time, location, host, venue, pic, pic_big, pic_cover, pic_small

	print("[+] Processing event '" + event["name"] + "'")

	template = template_original	
	start_date = event["start_time"][:10]

	file_name = start_date + "-" + event["name"].replace(" ", "-").replace("/", "").replace('"', "").replace("'", "")
	pic_base = "output/public/images/thumbnails/"
	pic = pic_base + file_name + ".jpg"
	pic_big = pic_base + file_name + "_big.jpg"
	pic_cover = pic_base + file_name + "_cover.jpg"
	pic_small = pic_base + file_name + "_small.jpg"
	post = "output/_posts/" + file_name + ".md"

	template = template.replace("[TITLE]", event["name"].replace("'", "").replace('"', ""))
	template = template.replace("[DESCRIPTION]", event["location"] + " " + event["description"][:20] + "...")	
	template = template.replace("[TAGLINE]", start_date)
	template = template.replace("[THUMBNAIL]", file_name + ".jpg")
	template = template.replace("[BODY]", "Start time: " + event["start_time"] + "  \n" + event["description"])
	# One of the posts has **** before and after text which messes up the template engine
	template = template.replace("****", "###")
	# One of the posts has some unicode that wasn't saving correctly
	template = template.encode("ascii", "ignore")

	file = open(post, "w")
	file.write(template)
	file.close()

	retrievePicture(event["pic"], pic)
	retrievePicture(event["pic_big"], pic_big)
	if event["pic_cover"] is not None:
		retrievePicture(event["pic_cover"]["source"], pic_cover)
	retrievePicture(event["pic_small"], pic_small)

 
#"name": "Network Sys Tech Student CCNA study group", 
#      "description": "Canyon room 123", 
#      "start_time": "2013-05-29T18:00:00-0600", 
#      "end_time": "2013-05-29T21:00:00-0600", 
#      "location": "College of Southern Idaho", 
#      "host": "SocialGeeks", 
#      "venue": {
#        "latitude": 42.580160676872, 
#        "longitude": -114.47447860752, 
#        "city": "Twin Falls", 
#        "state": "ID", 
#        "country": "United States", 
#        "id": 161280523619, 
#        "street": "315 Falls Avenue", 
#        "zip": "83303"
#      }, 
#      "pic": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-ash4/c225.0.264.264/s296x100/295369_10151592138587432_1816131650_n.jpg", 
#      "pic_big": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-ash4/c225.0.264.264/s552x414/295369_10151592138587432_1816131650_n.jpg", 
#      "pic_cover": {
#        "cover_id": "10151592138587432", 
#        "source": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-ash4/295369_10151592138587432_1816131650_n.jpg", 
#        "offset_y": 0, 
#        "offset_x": 0
#      }, 
#      "pic_small": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-ash4/c225.0.264.264/s160


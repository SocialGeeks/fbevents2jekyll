#!/usr/bin/env python

import json
import urllib
from datetime import datetime

def getFbEventsJson(file):
	f = open("sg_events.json", "r")
	file = f.read()
	events = json.loads(file)
	f.close()
	return events

def getJekyllTemplate(file):
	f = open("template.md", "r")
	template = f.read()
	f.close()
	return template

def saveThumbnail(name, file):
	f = open(name, "rw")
	f.write(file)
	
json_file = "sg_events.json"
events = getFbEventsJson(json_file)

template_file = "template.md"
template_original = getJekyllTemplate(template_file)

for event in events["data"]:
# name, description, start_time, end_time, location, host, venue, pic, pic_big, pic_cover, pic_small

	print("[+] Processing event '" + event["name"] + "'")

	template = template_original	
	start_date = str(datetime.strptime(event["start_time"][:10], "%Y-%m-%d"))[:10]

	file_name = start_date + "-" + event["name"].replace(" ", "-").replace("/", "").replace('"', "").replace("'", "")
	thumbnail = "output/public/images/thumbnails/" + file_name + ".jpg"
	post = "output/_posts/" + file_name + ".md"

	template = template.replace("[TITLE]", event["name"].replace("'", "").replace('"', ""))
	template = template.replace("[DESCRIPTION]", event["location"] + " " + event["description"][:20] + "...")	
	template = template.replace("[TAGLINE]", event["start_time"])
	template = template.replace("[THUMBNAIL]", file_name + ".jpg")
	template = template.replace("[BODY]", "Start time: " + event["start_time"] + "  \n" + event["description"])
	template = template.replace("****", "##")
	template = template.encode('ascii', 'ignore')

	file = open(post, "w")
	file.write(template)
	file.close()

	urllib.urlretrieve(event["pic"], thumbnail)

 
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


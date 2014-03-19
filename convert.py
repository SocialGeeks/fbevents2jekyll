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
# name, description, start_time, end_time, location, host, venue, picture

    print("[+] Processing event " + event["start_time"] + " - '" + event["name"] + "'")

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

    try:
        template = template.replace("[DESCRIPTION]", event["location"] + " " + event["description"][:20] + "...")   
    except KeyError:
        pass
    template = template.replace("[TAGLINE]", start_date)
    template = template.replace("[THUMBNAIL]", file_name + ".jpg")
    try:
        template = template.replace("[BODY]", "Start time: " + event["start_time"] + "  \n" + event["description"])
    except KeyError:
        template = template.replace("[BODY]", "Start time: " + event["start_time"] + "  ")
    # One of the posts has **** before and after text which messes up the template engine
    template = template.replace("****", "###")
    # One of the posts has some unicode that wasn't saving correctly
    template = template.encode("ascii", "ignore")

    file = open(post, "w")
    file.write(template)
    file.close()

    retrievePicture(event["picture"]["data"]["url"], pic)
    retrievePicture(event["picture"]["data"]["url"], pic_big)
    retrievePicture(event["picture"]["data"]["url"], pic_cover)
    retrievePicture(event["picture"]["data"]["url"], pic_small)

#    {
#      "name": "Turkey Lan planning night",
#      "description": "We will be planning and ironing out all the details for the turkey lan.  If you plan on coming to the LAN, pl
#an on coming to help get the stuff ready!",
#      "start_time": "2011-11-02T19:00:00",
#      "end_time": "2011-11-02T21:00:00",
#      "location": "CSI Sub",
#      "venue": {
#        "street": "",
#        "city": "",
#        "state": "",
#        "country": ""
#      },
#      "id": "248187198566972",
#      "picture": {
#        "data": {
#          "is_silhouette": true,
#          "url": "https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yE/r/tKlGLd_GmXe.png"
#        }
#      }
#    },


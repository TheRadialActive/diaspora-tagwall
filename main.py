#!/usr/bin/python

import json
import requests
import socket
import sys, os
from datetime import datetime
import CommonMark
import re
import scss

# install
# pip install requests
# use
# python commenting_user.py | sort -u

# Usage:
# run the script and define the post link 

if len(sys.argv) == 2:
    tag = sys.argv[1]
else:
    sys.exit("ERROR: Please enter a valid diaspora* tag in quotation marks.")

try:
    print("Get posts of tag " + tag)
    url_tags = "https://pod.geraspora.de/tags/" + tag + ".json"
    tag_request = requests.get(url_tags, verify=True)

    execution_date = datetime.now().strftime('%d.%m.%Y %H:%M')

    posts = ""
    for post in tag_request.json():
        section_start = '<section data-markdown><script type="text/template">'
        post_author = "[![](" + post['author']['avatar']['small'] + ")"  + post['author']['name'] + " (" + post['author']['diaspora_id'] + ")](/people/" + post['author']['guid'] + ")"
        post_text = re.compile('\#(\w)').sub(r'\\#\1', post['text'])
        post_date = post['created_at']
        post_pics = ""
        for photo in post['photos']:
            post_pics = post_pics + "![](" + photo['sizes']['large'] + ")"
        section_end = '</script></section>'
        
        posts = posts + section_start + post_author + "\n\n" + post_text + "\n\n **Posted at: " + post_date + "** \n\n\n *Last Update of tag lists at " + execution_date + "* \n" + post_pics + " " + section_end
    
    slide_file = open("slides.md", "w")
    slide_file.write(posts)
    slide_file.close()

    
except requests.exceptions.Timeout:

    print("Time out ")

except socket.timeout:

    print("socket Time out ")

except socket.error:

    print("socket error ")

except requests.exceptions.ConnectionError:

    print("Connection Error ")

except requests.exceptions.HTTPError:

    print ("HTTP Error ")

except requests.exceptions.RequestException:

    print("requests.exceptions.RequestException ")


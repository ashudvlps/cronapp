#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os, sys
import re
import MySQLdb
import webapp2
import datetime
import logging

rootdir = os.path.dirname(os.path.abspath(__file__))
lib = os.path.join(rootdir, 'lib')
sys.path.append(lib)

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch

INSTANCE_NAME = 'perm-status:us-west1:youtube'
DATABASE = 'youtube'
DB_USER = 'youtube_users'
DB_PASSWORD = 'ashvan'

time = str(datetime.datetime.now())
channels = ['channel/UChWtJey46brNr7qHQpN6KLQ','channel/UC9CYT9gSNLevX5ey2_6CK0Q','user/ndtv','channel/UCx8Z14PpntdaxCt2hakbQLQ','user/aajtaktv','user/abpnewstv','channel/UC7IdArS3MibBKFsqckq8GhQ']

db = MySQLdb.connect(unix_socket='/cloudsql/' + INSTANCE_NAME, db = DATABASE, user = DB_USER, passwd = DB_PASSWORD)
cursor = db.cursor()

for i in channels:
    req = urlfetch.fetch('https://www.youtube.com/'+i+'/about')
    soup = BeautifulSoup(req.content, "html.parser")
    s = soup.find_all('span', {'class': 'about-stat'})
    t = soup.find_all('span', {'class': 'qualified-channel-title-text'})
    subs = s[0].findChildren()[0].get_text().replace(',', '')
    views = s[1].findChildren()[0].get_text().replace(',', '')
    title = t[0].findChildren()[0].get_text().replace(',', '')
    logging.info(
        'INSERT INTO News_Channels(subs, views, ChannelName, timestamp) VALUES("' + subs + '", "' + views + '","' + title + '","' + time + '")')

    cursor.execute(
        'INSERT INTO News_Channels(subs, views, ChannelName, timestamp) VALUES("' + subs + '", "' + views + '","' + title + '","' + time + '")')

db.commit()
db.close()

logging.info('time and again:'+time)
class YoutubeHandler(webapp2.RequestHandler):
    def get(self):
        pass

app = webapp2.WSGIApplication([
    ('/', YoutubeHandler)
], debug=True)

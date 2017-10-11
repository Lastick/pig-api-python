#!/usr/bin/python
# -*- coding: UTF-8 -*-


# Copyright (c) 2017 The Karbowanec developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from urlparse import urlparse
import urllib
import httplib
import json

class PIGapi:

  api_url = ""
  api_status = False
  api_res = False
  api_url_default = 'http://stats.karbovanets.org/services/PIG/'
  user_agent = "PIGbot/1.0"

  def __init__(self, url):
    if (url != ""):
      self.api_url = url
    else:
      self.api_url = self.api_url_default

  def client(self, get_add):
    buff = ''
    self.api_status = False
    try:
      o = urlparse(self.api_url)
      conn = httplib.HTTPConnection(o.hostname, 80, timeout=10);
      headers = {"User-Agent": self.user_agent}
      conn.request("GET", o.path + 'api.php?' + get_add, '', headers)
      res = conn.getresponse()
      if (res.status == 200):
        buff = res.read()
        self.api_status = True
        conn.close()
    except:
      self.api_status = False
    return buff;

  def encode(self, mess):
    payment_id = ''
    self.api_res = False
    if (len(mess) <= 29):
      res = self.client(urllib.urlencode({'action': 'encode', 'mess': mess}))
      if (self.api_status):
        try:
          json_obj = json.loads(res)
          if (json_obj['status']):
            payment_id = json_obj['payment_id']
            self.api_res = True
        except:
          self.api_res = False
    return payment_id

  def decode(self, payment_id):
    mess = ''
    self.api_res = False
    if (len(payment_id) == 64):
      res = self.client(urllib.urlencode({'action': 'decode', 'payment_id': payment_id}))
      if (self.api_status):
        try:
          json_obj = json.loads(res)
          if (json_obj['status']):
            mess = json_obj['mess']
            self.api_res = True
        except:
          self.api_res = False
    return mess

  def getStatus(self):
    return self.api_res
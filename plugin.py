# -*- coding: utf-8 -*-
import sys
import re   
import xbmc
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from bs4 import BeautifulSoup
import requests


addon_id = 'plugin.video.videobronx'
addon = Addon(addon_id, sys.argv)
net = Net()

#find the mode
mode = addon.queries['mode']
#find the URL to resolve if a video has been clicked
url = addon.queries.get('url','')

def main():
	xbmc.executebuiltin("Container.SetViewMode(500)")
	categories()

def links(url):
	xbmc.executebuiltin("Container.SetViewMode(500)")
	#Grab the playlist file
	data = requests.get(url)
	html = BeautifulSoup(data.content, 'html5lib')
	post = html.find('div',{'class': 'post-body entry-content'})
	links = post.find_all('a')
	addon.log(links[2].get('href'),level=1)
	resolve(links[2].get('href'))

def categories():
	url = 'http://videobronxxx.blogspot.co.uk/'
	data = requests.get(url)
	html = BeautifulSoup(data.content, 'html5lib')
	links = html.find_all('div',{'class' : 'post hentry'})
	for link in links:
		name = link.h3.a.text
		thumb = link.img.get('src')
		url = link.h3.a.get('href')
		addon.add_item({'mode':2,'url':url}, {'title': name}, img=thumb, fanart='', resolved=False, total_items=0, item_type='video', is_folder=False)

def resolve(url):
	import commonresolvers
	stream_url = commonresolvers.get(url)
	if stream_url:
		addon.resolve_url(stream_url)
		addon.log('Resolved URL',level=1)

if mode=='main':
	main()		
elif mode =='2':
	links(url)
elif mode =='3':
	resolve(url)

addon.end_of_directory()
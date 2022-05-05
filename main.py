import os
import time
import praw
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from RedDownloader import RedDownloader

def remove_special_symbols(a):
	a = a.replace('.', '')
	a = a.replace('?', '')
	a = a.replace('"', '')
	a = a.replace('|', '')
	a = a.replace('/', '')
	a = a.replace('\\', '')
	a = a.replace('.', '')
	a = a.replace('>', '')
	a = a.replace('<', '')
	a = a.replace('*', '')
	return a

def download_gfycat(post):
	page = urlopen(post.url)
	html_text = page.read()
	soup = BeautifulSoup(html_text, 'lxml')
	actual_link = (soup.find(type='video/mp4'))['src']
	print(actual_link)
	download_image(actual_link, post.title)

def download_image(url, title):
	r = requests.get(url)
	file_format = url[url.rfind('.'):]   #this gives us the extension by searching the dot backwards
	filename = remove_special_symbols(title) + file_format
	with open(subreddit_name+'\\' + filename, 'wb') as f:
		f.write(r.content)

def download_gifv(post):
	if '.gif' not in post.preview['images'][0]['variants']:
		return 
	else:
		url = post.preview['images'][0]['variants']['gif']['source']['url']
	r = requests.get(url)
	file_format = post.url[post.url.rfind('.'):]   #this gives us the extension by searching the dot backwards
	filename = remove_special_symbols(post.title) + file_format
	with open(subreddit_name+'\\' + filename, 'wb') as f:
		f.write(r.content)

reading_instance = praw.Reddit(client_id='XnUXSC6Ctdf_sRY9Hs3FnA', client_secret='At5aTj9W3Wj9h3TwDA-jUH_d-CNuvQ', user_agent='scraper', ratelimit_seconds=300)
subreddit = reading_instance.subreddit("dogelore")
subreddit_name = subreddit.display_name
def download_subreddit(subreddit_name):
	count = 0
	
	try:
		os.mkdir(subreddit_name)
	except FileExistsError:
		pass

	for post in subreddit.top("all", limit = 7000):
		#print('\033[0;37;40m')
		try:
			
			count+=1	

			#error https://www.reddit.com/gallery/qjsi1r	
			#https://i.redd.it/r37yy3j5kkm81.jpg
			#https://v.redd.it/7p1juyn60vj61

			if 'tenor' in post.url:
				print('\033[1;31;47m', count, 'Tenor alarm aaa')
				#print('\033[0;37;40m') 
				continue  #I will do this later
			if post.is_self:
				if post.selftext == '[ Removed by reddit in response to a copyright notice. ]':
					continue  #Removed post

			if '.gifv' in post.url:
				download_gifv(post)
				print('\033[0;32;40m', 'Downloaded gifv number %d:'%count , post.title, post.url)
			elif '.jpg' in post.url or '.gif' in post.url or '.png' in post.url:
				download_image(post.url, post.title)
				print('\033[0;32;40m', 'Downloaded picture number %d:'%count, post.title, post.url)
			elif 'gfycat.com' in post.url:
				download_gfycat(post)
				print('\033[0;32;40m', 'Downloaded gfycat gif number %d:'%count, post.title, post.url)
			else:
				#print(post.preview)
				RedDownloader.Download(post.url)#, output=remove_special_symbols(post.title))
				print(count, post.url)
		except:
			print('\033[2;31;43m', count, post.title , post.url)
			#print('\033[0;37;40m')
download_subreddit(subreddit_name)

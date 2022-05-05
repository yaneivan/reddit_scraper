import os
import time
from termcolor import colored
try:
	import praw
	import requests
	import pandas as pd
	from bs4 import BeautifulSoup
	from urllib.request import urlopen
	from RedDownloader import RedDownloader
except:
	print('Missing some libraries, trying to install them')
	os.system('pip install --upgrade requests pandas beautifulsoup4 urllib3 lxml neo4j praw RedDownloader')
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
	download_image(actual_link, post.title, post.subreddit.display_name)

def v_reddit(link, post):
	r = requests.get(link, allow_redirects= True)
	new_link = r.url 
	print(colored((new_link, post.title, post.subreddit.display_name), 'red'))
	RedDownloader.Download(new_link, output= post.title, destination = post.subreddit.display_name+'/')
	#download_image(new_link, post.title, post.subreddit.display_name)

def download_image(url, title, subreddit_name):
	r = requests.get(url, allow_redirects = True)
	file_format = url[url.rfind('.'):]   #this gives us the file format by searching the dot backwards
	filename = remove_special_symbols(title) + file_format
	with open(subreddit_name+'/' + filename, 'wb') as f:
		f.write(r.content)

def download_gifv(post):
	if '.gif' not in post.preview['images'][0]['variants']:
		return 
	else:
		url = post.preview['images'][0]['variants']['gif']['source']['url']
	r = requests.get(url)
	file_format = post.url[post.url.rfind('.'):]   #this gives us the extension by searching the dot backwards
	filename = remove_special_symbols(post.title) + file_format
	with open(subreddit_name+'/' + filename, 'wb') as f:
		f.write(r.content)

#don't forget to delete your api key before uploading to github
reading_instance = praw.Reddit(client_id='XnUXSC6Ctdf_sRY9Hs3FnA', client_secret='At5aTj9W3Wj9h3TwDA-jUH_d-CNuvQ', user_agent='scraper', ratelimit_seconds=300)

def download_subreddit(subreddit_name):
	subreddit = reading_instance.subreddit(subreddit_name)
	subreddit_name = subreddit.display_name
	count = 0
	
	try:
		os.mkdir(subreddit_name)
	except FileExistsError:
		pass

	
	#maybe we can search by some popular words in the sub
	posts = list(subreddit.top('all', limit=None))
	
	posts+= list(subreddit.top('year', limit = None))
	posts+= list(subreddit.top('month', limit = None))
	posts+= list(subreddit.top('week', limit = None))
	posts+= list(subreddit.top('day', limit = None))
	posts+= list(subreddit.top('hour', limit = None))
	posts+= list(subreddit.hot(limit = None))
	posts+= list(subreddit.new(limit = None))
	

	print('Found %d posts, starting to download'%len(posts))
	time.sleep(3)
	
	for post in posts:#subreddit.top('all', limit = 4):
		#try:
		if True:	
			count+=1	

			#error https://www.reddit.com/gallery/qjsi1r	

			if post.is_self:
				if post.selftext == '[ Removed by reddit in response to a copyright notice. ]':
					#print('Removed post')
					print(colored('Removed post', 'red'))
					continue  #Removed post
			if 'tenor' in post.url:
				#print(count, 'Tenor alarm aaa')
				print(colored('Tenor alarm', 'red'))
				continue  #I will do this later
			
			#apparently RedDownloader could download pictures,
			#so a lot of theese functions are useless
			elif 'v.redd.it' in post.url:
				v_reddit(post.url, post)
				print(colored('Downloaded v.redd.it post number {}: {}, {}'.format(count, post.title, post.url)))
			elif '.gifv' in post.url:
				download_gifv(post)
				#print('Downloaded gifv number %d:'%count , post.title, post.url)
				print(colored('Downloaded gifv number {}: {}, {}'.format(count, post.title, post.url), 'green'))
			elif '.jpg' in post.url or '.gif' in post.url or '.png' in post.url:
				download_image(post.url, post.title, post.subreddit.display_name)
				#print('Downloaded picture number %d:'%count, post.title, post.url)
				print(colored(('Downloaded picture number {}: {}, {}'.format(count, post.title, post.url)), 'green'))
			elif 'gfycat.com' in post.url:
				download_gfycat(post)
				#print('Downloaded gfycat gif number %d:'%count, post.title, post.url)
				print(colored('Downloaded gfycat fig number {}: '.format(count, post.title, post.url), 'green'))
			elif 'gallery' in post.url:
				RedDownloader.Download(post.url, output = post.title, destination = post.subreddit.display_name)
			else:
				#print(post.preview)
				#RedDownloader.Download(post.url)#, output=remove_special_symbols(post.title))
				#print("I couldn't recognise any known types of posts", count, post.url)
				print(colored("I couldn't recognise any known types of posts {}".format(post.url), 'red'))
		#except:
		#	print(count, post.title , post.url)

download_subreddit('bigfloppa')

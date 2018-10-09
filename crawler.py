#/usr/bin/python
import requests
from bs4 import BeautifulSoup
import sys
import re
import argparse 
import signal
from selenium import webdriver

def link_extractor(content, start_url):
	soup = BeautifulSoup(content, 'lxml')
	links = soup.find_all('a')
	extracted_links = []
	for tag in links:
		link = tag.get('href', None)
		if link is not None:
			if link.startswith('/') or link.startswith(start_url):			
				extracted_links.append(link)
	return extracted_links


def send_new_request(url, method='GET', data=None):
	client = webdriver.PhantomJS()
	if method == 'GET':
		client.get(url)
		return client.page_source

def sigint_handler(signum, frame):
	print '\n\n\nWhere Are You Going?!'
	sys.exit()


def show_progress(now, end):
	pass
	

def main():
	signal.signal(signal.SIGINT, sigint_handler)
	url_regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})'

	parser = argparse.ArgumentParser(description='The Best Crawler ')
	parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s version 1.0')
	parser.add_argument('-u', dest='start_url', action='store',
                    default=False,
                    help='find devices in a particular city')
	parser.add_argument('-d', dest='detailed', action='store',
						default=False, 
						help='Generate Detailed Report Including Request and Response')
	parser.add_argument('-p', dest='path', action='store',
						default=False, 
						help='path to store report')
	
	args = parser.parse_args()
	if len(sys.argv) == 1: 
	    parser.print_help()
	    exit()
	if not re.search(url_regex, args.start_url, re.I):
		print 'Invalid Url :-) Try Again!'
		sys.exit()

	start_response = send_new_request(args.start_url)
	extracted_links = link_extractor(start_response, args.start_url)

	for i, link in enumerate(extracted_links):
		if not link.startswith('http://') and not link.startswith('https://'):
			link = args.start_url + link
		sys.stdout.write('\r' + 'Current Link ' + link + ' Remaning page to crawl----> ' + str(len(extracted_links) - i))
		sys.stdout.flush()
		link_response = send_new_request(link)
		new_links = link_extractor(link_response, args.start_url)
		extracted_links.extend(new_links)

main()

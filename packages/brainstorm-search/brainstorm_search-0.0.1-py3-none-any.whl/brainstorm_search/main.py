from bs4 import BeautifulSoup
from collections import OrderedDict, Counter
from duckduckgo_search import ddg
from .helper import *
from math import inf
from pathlib import Path
import argparse
import concurrent.futures 
import os
import pickle
import re
import requests

def main():

	# Create the parser and add arguments
	parser = argparse.ArgumentParser(description="Summarize lists of ideas provided by Duckduckgo")
	parser.add_argument(dest='keywords', help="brainstorm topic you are searching for, example: \"best icecream flavors\"")
	parser.add_argument('-v', '--verbose', action="store_true", help="show details of what the script is doing")
	parser.add_argument('-cc', '--clear-cache', action="store_true", help="clear the cache before script runs")
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-l', '--list', action="store_true", help="output as list")
	group.add_argument('-s', '--set', action="store_true", help="output as set")
	group.add_argument('-d', '--dict', action="store_true", help="output as dict")

	# Parse and print the results
	args = parser.parse_args()

	# keywords = "best programming languages"
	# keywords = "best icecream flavors"
	# keywords = "best side gig ideas"
	keywords = args.keywords
	verbose = args.verbose
	clear_cache = args.clear_cache

	set_up_cache_folders()

	if clear_cache:
		clear_all_cache()
		if verbose:
			print('cache cleared')


	if verbose: print(f'Checking if "{keywords}" exists in cache')
	if exists_in_search_cache(keywords):
		if verbose:
			print(f'Yes it exists')
			print(f'Searching cache for "{keywords}"')
		search_result = result_of_search_cache(keywords)
		
	else:
		if verbose:
			print(f'No it does not exist')
			print(f'Searching Duckduckgo for "{keywords}"')
		search_result = result_of_ddg_search(keywords)
		
		if verbose:
			print(f'Adding "{keywords}" search to cache')
		add_to_search_cache(keywords, search_result)
		

	urls = [webpage['href'] for webpage in search_result]

	if verbose:
		print('Search results:')
		print(*urls, sep="\n")
		print('Retrieving webpages concurrently')

	with concurrent.futures.ThreadPoolExecutor() as exector: 
	   exector.map(download_url, urls)


	# search_result = search_result[17:18]  # for testing purposes

	idea_set = Counter()

	for website in search_result:
		title = website['title']
		url = website['href']

		if not exists_in_page_cache(url):
			continue

		num_ideas_in_title = get_num_ideas(title)

		if num_ideas_in_title == None:
			if verbose:
				print('Ignoring website', url, 'which has no number in its title')

			continue

		if verbose:
			print('Looking at', url, 'and hope to find', num_ideas_in_title, 'ideas')

		text = read_page_cache(url)
		soup = BeautifulSoup(text, features='lxml')

		for number in range(2, 7):
			tag_name = 'h'+str(number)
			tags = soup.find_all(tag_name)

			if tags == None:
				continue

			if len(tags) < num_ideas_in_title:
				continue

			category = OrderedDict()

			for tag in tags:
				nest = str(tag).replace('\n', '')
				nest = re.sub(r'>.*?<', '><', nest)
				nest = re.sub(r'".*?"', '""', nest)

				tag_text = tag.text.replace('\n', '')
				# remove everything after n-dash or m-dash
				tag_text = re.sub(r'[–—].*', '', tag_text)
				tag_text = re.sub(r'.*:', '', tag_text)
				tag_text = remove_non_ascii(tag_text)
				tag_text = tag_text.strip()

				if nest in category:
					category[nest].append(tag_text)
				else:
					category[nest] = [tag_text]


			nest_rank = []

			for uniq_nest, tag_texts in category.items():
				if len(tag_texts) < num_ideas_in_title:
					continue
				nest_rank.append((len(tag_texts), uniq_nest))

			if not nest_rank: continue

			nest_rank.sort()
			key_nest = nest_rank[0][1]


			idea_candidates = category[key_nest][:num_ideas_in_title]

			if majority_start_with_number(idea_candidates):
				idea_candidates = keep_only_start_with_number(idea_candidates)

			idea_candidates = remove_leading_numbers(idea_candidates)

			if verbose:
				print(f'Found {len(idea_candidates)} idea candidates:', idea_candidates)

			idea_set.update(idea_candidates)

			break

		else:
			if verbose:
				print('Found no ideas here')


	if verbose:
		print(f'Here is the summary of brainstorm ideas for "{keywords}"')

	if args.list:
		print(list(idea_set.keys()))
	elif args.set:
		print(set(idea_set.keys()))
	elif args.dict:
		print(dict(idea_set))
	else:
		print(*list(idea_set.keys()), sep="\n")


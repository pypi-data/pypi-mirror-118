from duckduckgo_search import ddg
from math import inf
from pathlib import Path
from unidecode import unidecode
import glob
import os
import pickle
import re
import requests


def alphanum(x):
	return ''.join(ch for ch in x if ch.isalnum())

def add_to_search_cache(keywords, search_results):
	new_cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/search/' + alphanum(keywords)
	with open(new_cache_path, 'wb') as new_file:
		pickle.dump(search_results, new_file)
	new_file.close()
	

def exists_in_search_cache(keywords):
	expected_cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/search/' + alphanum(keywords)
	path_is_file = Path(expected_cache_path).is_file()
	return path_is_file

def result_of_search_cache(keywords):
	keyword_cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/search/' + alphanum(keywords)
	with open(keyword_cache_path, 'rb') as keyword_cache_file:
		return pickle.load(keyword_cache_file)
	return {}

def result_of_ddg_search(keywords):
	return ddg(keywords)


def get_num_ideas(title):
	numbers = re.findall(r'\d+', title)
	for number in numbers:
		number = int(number)
		if not 2019 < number < 2099:
			return number
	return

def exists_in_page_cache(url):
	expected_cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/page/' + alphanum(url)
	return Path(expected_cache_path).is_file()

def add_to_page_cache(url, page_results):
	new_cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/page/' + alphanum(url)
	with open(new_cache_path, 'wb') as new_file:
		pickle.dump(page_results, new_file)
	new_file.close()

def download_url(url):
	if exists_in_page_cache(url):
		return

	try:
		request = requests.get(url, timeout=5)
		if request.status_code != 200:
			return
		add_to_page_cache(url, request.text)
	except:
		return

def read_page_cache(url):
	cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/page/' + alphanum(url)
	with open(cache_path, 'rb') as cache_file:
		return pickle.load(cache_file)
	return {}


def majority_start_with_number(idea_candidates):
	num_total = len(idea_candidates)
	num_start_with_number = 0

	for idea in idea_candidates:
		num_seen = False
		letter_seen = False

		for ch in idea:
			if ch.isdigit():
				num_seen = True
			elif ch.isalpha():
				letter_seen = True

			if num_seen and not letter_seen:
				num_start_with_number += 1
				break

	return num_start_with_number / num_total > 0.5


def keep_only_start_with_number(idea_candidates):
	result = []
	for idea in idea_candidates:
		num_seen = False
		letter_seen = False

		for ch in idea:
			if ch.isdigit():
				num_seen = True
			elif ch.isalpha():
				letter_seen = True

			if num_seen and not letter_seen:
				result.append(idea)
				break

	return result

def remove_leading_numbers(idea_candidates):
	result = []
	for idea in idea_candidates:
		num_seen = False
		letter_seen = False

		for idx, ch in enumerate(idea):
			if ch.isdigit():
				num_seen = True
			elif ch.isalpha():
				letter_seen = True
			else:
				continue

			if num_seen and not letter_seen:
				continue
			else:
				result.append(idea[idx:])
				break

	return result


def remove_non_ascii(text):
	# return unidecode(unicode(text, encoding = "utf-8"))
	return unidecode(text)

def clear_all_cache():
	search_files = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/cache/search/*')
	for f in search_files:
		os.remove(f)

	page_files = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/cache/page/*')
	for f in page_files:
		os.remove(f)

def set_up_cache_folders():
	cache_path = os.path.dirname(os.path.abspath(__file__)) + '/cache'
	search_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/search'
	page_path = os.path.dirname(os.path.abspath(__file__)) + '/cache/page'


	if not os.path.exists(cache_path):
		os.mkdir(cache_path)

	if not os.path.exists(search_path):
		os.mkdir(search_path)

	if not os.path.exists(page_path):
		os.mkdir(page_path)




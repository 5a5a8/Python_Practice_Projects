import requests
import sys
from bs4 import BeautifulSoup


def get_urls_words(urls: list, depth: int = 0) -> list:
	"""Visits a web page, returns a list of any URLs on that webpage.
	If depth = 0, it only does that web page.
	If depth = 1, it visits the URLs on each of those pages too.
	And so on."""


	url_list = []
	for url in urls:
		try:
			response = requests.get(url)
		except:
			print('[ERROR]: Could not open: ' + url)
			continue
		html = response.text
		soup = BeautifulSoup(html, 'lxml')
		anchor_links = soup.find_all('a')

		#we may as well get the words on the page while we're here
		words = soup.get_text()
		wordlist = words.split(' ')
		with open('words.txt', 'a') as wordsfile:
			for i in range(0, len(wordlist)):
				wordlist[i] = wordlist[i].strip('\n\t ')
				wordsfile.write(wordlist[i] + '\n')
			wordsfile.close()

		for link in anchor_links:
			captured_url = link.get('href')
			if captured_url and captured_url.startswith('http'): 
				url_list.append(captured_url)

	unique_urls = list(set(url_list))
	if depth == 0:
		return unique_urls
	else:
		return list(set(unique_urls + get_urls_words(unique_urls, depth-1)))


def tidy_wordlist(filename: str = 'words.txt') -> None:
	"""Tidies our wordlist by removing duplicates and blank lines"""

	with open(filename, 'r') as f:
		words = f.readlines()
		f.close()
	
	#remove duplicates and blank lines
	words = list(set(words))
	if '\n' in words: words.remove('\n')

	with open(filename, 'w') as f:
		for word in words:
			f.write(word.strip('\t '))
		f.close()

	return
	
def expand_wordlist(words_file: str = 'words.txt') -> None:
	"""Expands the wordlist with masks.
	For example we could change 'Cats' to 'c4t$'.
	This function leaves a lot to be desired, use a proper tool
	if you're serious about this."""
	
	with open(words_file, 'r') as f:
		words = f.readlines()
		f.close()
	
	find_chars = 'aeilos'
	repl_chars = '431105'
	find_chars2 = 'AEILOS'
	repl_chars2 = '@3110$'

	with open(words_file, 'a') as f:
		for word in words:
			trans = word.maketrans(find_chars, repl_chars)
			new_word = word.translate(trans)
			f.write(new_word)

			trans2 = word.maketrans(find_chars2, repl_chars2)
			new_word2 = word.translate(trans2)
			f.write(new_word2)
		f.close()
	
	return

	
def main():
	for i in range(len(sys.argv)):
		if sys.argv[i] == '--url':
			url = sys.argv[i + 1]
		elif sys.argv[i] == '--depth':
			depth = int(sys.argv[i + 1])
		elif sys.argv[i] == '--expand':
			expand = True

	print('Working... Depending on the depth, this can take a while.')
	get_urls_words([url], depth)
	tidy_wordlist()
	if expand:
		expand_wordlist()
		tidy_wordlist()

if __name__ == '__main__':
	main()

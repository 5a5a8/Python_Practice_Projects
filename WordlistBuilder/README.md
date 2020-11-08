# WordlistBuilder
Scrape a webpage for words to use in a wordlist.

Why? A site about dogs is more likely to have e.g. a password or admin URL about dogs.

Run it with `python wordlist.py --url https://example.com --depth 0 --expand`

Where the URL is the site to scrape, and the depth is how far to follow links.
A depth of 0 takes only words from the specified page.
A depth of 1 follows the URLs on that page, and takes words from them too...
And so on.

If the --expand option is set, the wordlist will be expanded using common character replacements.
For example 's' will be replaced by '$'.
So the word 'dogs' might become 'd0g$'.

Written 2020-Nov-08, and inspired by another piece of software which I forget the name of.

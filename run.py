import os

if __name__ == "__main__":
	folder_path = os.path.abspath("./")
	command = ('scrapy runspider mtg_crawler.py -O %s/cards.json --set="ROBOTSTXT_OBEY=True"' % (folder_path))
	os.system(command)

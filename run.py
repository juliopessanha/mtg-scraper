import os

if __name__ == "__main__":
	folder_path = os.path.abspath("./")
	command = ('(cd ./mtg_scraper && exec scrapy crawl mtg_crawler -O %s/cards.json)' % (folder_path))
	os.system(command)

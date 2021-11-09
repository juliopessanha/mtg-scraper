import os

if __name__ == "__main__":
	folder_path = os.path.abspath("./")
	command = ('(cd ./mtg_scrapper && exec scrapy crawl mtg_crawler -O %s/cards2.json)' % (folder_path))
	os.system(command)

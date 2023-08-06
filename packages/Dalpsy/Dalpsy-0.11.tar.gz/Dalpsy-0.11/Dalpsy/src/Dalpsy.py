import requests
from bs4 import BeautifulSoup
from helpers.format import format
from helpers.check_if_exists import check_if_exists

class Manga:
	'''
	Manga class.
	'''
	def __init__(self):
		self.base_manga_url = "https://www.anime-planet.com/manga/"
		self.base_manga_reviews = "https://www.anime-planet.com/manga/{}/reviews"

	def get_manga_reviews(self, manga: str) -> list:
		'''
		Get the reviews of a manga.
		'''
		manga = format(manga)
		r = requests.get(self.base_manga_reviews.format(manga))
		soup = BeautifulSoup(r.content, "html5lib")
		reviews = soup.find_all("div", {"class":"pure-1 userContent readMore"})
		review_list = []

		for x in reviews:
			review_list.append(x)

		reviews = []

		for x in review_list:
			string = ""
			while True:
				try:
					x = x.find("p")
					x = x.getText()
					string += f"{x}\n"
				except:
					break		

			reviews.append(string)

		return reviews


	def get_manga_info(self, manga: str) -> dict:
		'''
		Get information on a manga.
		'''
		manga = format(manga)
		r = requests.get(self.base_manga_url + f"{manga}")
		soup = BeautifulSoup(r.content, "html5lib")

		if check_if_exists(manga):
			dict = {}
			dict["title"] = soup.find("meta", property="og:title")["content"]
			dict["description"] = soup.find("meta", property="og:description")["content"]
			dict["url"] = soup.find("meta", property="og:url")["content"]
			dict["type"] = soup.find("meta", property="og:type")["content"]
			dict["author"] = soup.find("meta", property="book:author")["content"]
			dict["author"] = dict["author"].replace("https://www.anime-planet.com/people/","")
			dict["cover"] = soup.find("meta", property="og:image")["content"]
			dict["reviews"] = self.get_manga_reviews(manga)
			return dict
		else:
			return "We could not find that."

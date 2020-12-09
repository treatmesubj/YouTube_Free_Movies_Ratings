import json
import requests
import operator
from bs4 import BeautifulSoup
import re

"""
HTTP fetches records of YouTube's available free movies, then fetches and sorts the RottenTomatoes ratings for those movies
"""


def get_YT_storefront_dictionary(url):

	"""
	HTTP fetches YouTube Movies Storefront ytInitialData JavaScript object from a script in the pre-rendered HTML
	"""

	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	pattern = re.compile(r"ytInitialData\s=\s({.*});")
	script_elem = soup.find("script", text=pattern)
	jaysean = pattern.search(script_elem.string).group(1)
	sanjay = json.loads(jaysean)

	return sanjay


if __name__ == "__main__":

	home_sanjay = get_YT_storefront_dictionary("https://www.youtube.com/feed/storefront")

	for guy in home_sanjay['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']:
		try:
			if "Free" in guy['itemSectionRenderer']['contents'][0]['shelfRenderer']['title']['runs'][0]['text']:
				free_movies_url_ext = guy['itemSectionRenderer']['contents'][0]['shelfRenderer']['endpoint']['commandMetadata']['webCommandMetadata']['url']
				break
		except KeyError:
			pass

	free_sanjay = get_YT_storefront_dictionary(f"https://www.youtube.com{free_movies_url_ext}")

	movies_data = free_sanjay['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['gridRenderer']['items']

	movies = [movie['gridMovieRenderer']['title']['runs'][0]['text'] for movie in movies_data]

	movie_ratings = tuple()

	for movie in movies:
		response = requests.get(f"https://www.rottentomatoes.com/search?search={movie}")
		soup = BeautifulSoup(response.text, 'html.parser')
		sanjay = json.loads(soup.select_one("script#movies-json").string)
		if sanjay['count'] > 0:
			movie_rating = ((movie, int(sanjay['items'][0]['tomatometerScore'].get('score') or 0), int(sanjay['items'][0]['audienceScore'].get('score') or 0)),)
			movie_ratings += movie_rating
			
			print(f"{movie_rating[0][0][:25], movie_rating[0][1], movie_rating[0][2]}".ljust(50, '#'), len(movie_ratings), end="\r")

	movie_ratings = sorted(movie_ratings, key=lambda x: 0 if not x[1] else x[1], reverse=True)
	print('#'*50)
	for movie in movie_ratings:
		print(movie)
	
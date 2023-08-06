import requests
from bs4 import BeautifulSoup
import difflib
import argparse
from rich.console import Console
import json
import os

def animeid(psearch):
	response = []
	page = requests.get(f"https://myanimelist.net/info.php?search={psearch}&go=relationids&divname=relationGen1")

	soup = BeautifulSoup(page.content, "html.parser")
	try:
		for i in soup.find("table", {"border":"0", "cellpadding":"3", "cellspacing":"0", "width":"100%"}).findAll("tr"):
			if i.find("td", attrs={"class": ["td1", "td2"]}) is None:
				pass
			else:
				response.append((i.find("a").get_text(), i.find("td", attrs={"align":"left"}).get_text(), difflib.SequenceMatcher(None, psearch, i.find("td", attrs={"align":"left"}).get_text()).ratio()*100))
	except AttributeError:
		print("Error : 404 Not Found")
		quit()

	sim = 0
	for resp in response:
		if resp[2] > sim:
			sim = resp[2]
		else:
			pass

	for resp in response:
		if resp[2] == sim:
			return resp

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--search", metavar="name", help="retrieves all the information about specific anime", required=True, nargs='+')
	args = parser.parse_args()

	animeidx = animeid("+".join(args.search))
	display(animeidx)

##############################################################################################
	
def display(animeidx):
	os.system("cls")
	console = Console()
	reqjikan = requests.get(f"https://api.jikan.moe/v3/anime/{animeidx[0]}")
	rjson = json.loads(reqjikan.text)
	print()
	console.print(f"[royal_blue1]{rjson['title']}[/royal_blue1] [cyan][{rjson['title_english']}][/cyan]", justify="center")
	print()
	console.print(f"   Score [MAL] : [magenta]{rjson['score']}[/magenta]", )
	console.print(f"   Rank [MAL] : [magenta]#{rjson['rank']}[/magenta]",)
	console.print(f"   Popularity [MAL] : [magenta]#{rjson['popularity']}[/magenta]",)
	console.print(f"   Members [MAL] : [magenta]{rjson['members']}[/magenta]",)
	console.print(f"   Favourites [MAL] : [magenta]{rjson['favorites']}[/magenta]",)
	print()
	console.print(f"   Type : [red]{rjson['type']}[/red]",)
	console.print(f"   Source : [red]{rjson['source']}[/red]",)
	console.print(f"   Episodes : [red]{rjson['episodes']}[/red]",)
	console.print(f"   Rating : [red]{rjson['rating']}[/red]",)
	console.print(f"   Duration : [red]{rjson['duration']}[/red]",)
	console.print(f"   Aired : [red]{rjson['aired']['string']}[/red]",)
	console.print(f"   Status : [red]{rjson['status']}[/red]",)
	print()
	console.print(f"   Synopsis", style="blue")
	print()
	console.print(f"   {rjson['synopsis'].strip('[Written by MAL Rewrite]')}", justify="center")









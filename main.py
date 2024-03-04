import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS

note_url = "https://pl.wikipedia.org/wiki/J%C4%99zyk_programowania"
ranking_url = "https://www.tiobe.com/tiobe-index/"
img_url = "https://www.tiobe.com"

ddgs = DDGS()

if not os.path.exists("images"):
    os.mkdir("images")

if not os.path.exists("sites"):
    os.mkdir("sites")


def write_search(file, query, count):
    file.write(f"### Wyniki wyszukiwania: \"{query}\" \n\n")
    results = [r for r in ddgs.text(query, max_results=count)]
    for r in results:
        site.write(f"#### [{r['title']}]({r['href']}) \n\n {r['body']}\n\n\n\n\n")


# główna
response = requests.get(note_url)
note = BeautifulSoup(response.text, "html.parser")
note = note.find("p")
note = note.text.replace("[1]", "")
with open("index.md", "w") as f:
    f.write(f"# Języki Programowania \n\n{note} \n Źródło: [Wikipedia]({note_url})\n\n \n\n")
    f.write(f"### [Top 20 języków programowania](top20.md)")

# lista
response = requests.get(ranking_url)
top20 = BeautifulSoup(response.text, 'html.parser')
top20 = top20.find("table", {"class": "table-top20"})
top20 = top20.find_all("tr")
with open('top20.md', 'w') as f:
    f.write(f"# Top 20 języków programowania: \n\n")
    for row in top20:
        cells = row.find_all("td")
        if len(cells) <= 5:
            continue

        # zbieranie danych z tabeli
        rank = cells[0].text.strip()
        language = cells[4].text.strip()
        language_name = language.split("/")[-1].replace(" ", "_")
        rating = cells[5].text.strip()
        image = img_url + cells[3].find("img")["src"]

        # zapisywanie obrazka
        with open(os.path.join("images", language_name + ".png"), "wb") as img:
            img.write(requests.get(image).content)

        # element listy
        f.write(f"### {rank}. {language} \n\n ![{language} image]({image}) \n\nOcena: {rating}\n\n")
        subsite = os.path.join("sites", language_name + ".md")
        f.write(f" [Więcej informacji]({subsite})\n\n---\n\n")

        # tworzenie podstrony
        with open(subsite, "w") as site:
            site.write(f"# {language} ![{language} image]({image})\n\n")
            write_search(site, language + " język programowania", 5)
            site.write(f"\n\n---\n\n")
            write_search(site, language + " kurs programowania", 3)
            site.write(f"\n\n---\n\n [Powrót do listy](../top20.md)")

    f.write(f"\n\n---\n\n [Powrót do strony głównej](index.md)")

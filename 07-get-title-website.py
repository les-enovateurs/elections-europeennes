import requests
from bs4 import BeautifulSoup
import json

# Lecture du fichier JSON depuis un fichier
with open('./data/refacto/programme-website-stats-falc.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

titles = []

# Parcourir chaque entrée dans les données
for entry in data['data']:
    if len(entry['website_url']) > 0:
        try:
            response = requests.get(entry['website_url'][0], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title found"

            print(f"- [{title}]({entry['website_url'][0]})")
            titles.append({'url': entry['website_url'][0], 'title': title})
        except requests.RequestException as e:
            titles.append({'url': entry['website_url'][0], 'title': f"Error: {str(e)}"})

for entry in titles:
    print(f"- ({entry['title']})[{entry['url']}]")
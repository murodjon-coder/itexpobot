import requests
from bs4 import BeautifulSoup
import json

def scrape_itpark_events():
    url = "https://itpark.uz/uz/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    forumlar = []
    cards = soup.find_all("div", class_="news-item")

    for card in cards[:5]:  # faqat 5 ta yangilik
        sarlavha = card.find("h3").get_text(strip=True)
        sana = card.find("div", class_="news-date").get_text(strip=True)
        forumlar.append({"sana": sana, "nomi": sarlavha})

    with open("forumlar.json", "w", encoding="utf-8") as f:
        json.dump(forumlar, f, ensure_ascii=False, indent=4)

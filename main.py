import requests
import feedparser
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        return feed.entries
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_movie_name(title):
    return title.split(" (")[0].strip()

def extract_magnets_from_description(description_html):
    soup = BeautifulSoup(description_html, "html.parser")
    links = soup.find_all('a', href=True)
    magnets = [link['href'] for link in links if link['href'].startswith("magnet:")]
    return magnets

def main():
    print("─" * 80)
    print("                         🎬 TamilMV CLI Scraper via RSS                          ")
    print("─" * 80)

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    movie_titles = [extract_movie_name(entry.title) for entry in entries]

    for idx, title in enumerate(movie_titles, 1):
        print(f"[{idx}] {title}")
    
    try:
        choice = int(input("\n[?] Choose a movie/show to view magnet links: "))
        if not (1 <= choice <= len(entries)):
            raise ValueError("Out of range.")
    except ValueError as ve:
        print(f"❌ Invalid input: {ve}")
        return

    selected_entry = entries[choice - 1]
    magnets = extract_magnets_from_description(selected_entry.description)

    if magnets:
        print("\n📡 Magnet Links Found:")
        for m in magnets:
            print(f"• {m}")
    else:
        print("❌ No magnet links found in the description.")

if __name__ == "__main__":
    main()

import requests
import feedparser
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.content).entries
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_magnets(description_html):
    soup = BeautifulSoup(description_html, "lxml")
    links = soup.find_all("a", href=True)
    magnets = [(link.text.strip(), link["href"]) for link in links if link["href"].startswith("magnet:?")]
    return magnets

def main():
    print("─" * 80)
    print("                         🎬 TamilMV CLI Scraper via RSS                          ")
    print("─" * 80)

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    for idx, entry in enumerate(entries):
        print(f"[{idx + 1}] {entry.title} | {entry.link}")

    try:
        choice = int(input("\n[?] Choose a movie/show to list magnet links: ")) - 1
        if not (0 <= choice < len(entries)):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    selected = entries[choice]
    magnets = extract_magnets(selected.description)

    if not magnets:
        print("❌ No magnet links found in the description.")
        return

    print(f"\n🔗 Available Magnet Links for: {selected.title}\n")
    for i, (title, _) in enumerate(magnets):
        print(f"[{i + 1}] {title}")

    try:
        link_choice = int(input("\n[?] Choose a magnet link to view: ")) - 1
        if not (0 <= link_choice < len(magnets)):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    print(f"\n🔗 Magnet Link:\n{magnets[link_choice][1]}\n")

if __name__ == "__main__":
    main()

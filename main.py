import cloudscraper
import feedparser
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.content).entries
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_magnets(description_html):
    soup = BeautifulSoup(description_html, "lxml")
    links = soup.find_all("a", href=True)
    magnets = []
    for link in links:
        href = link["href"]
        if href.startswith("magnet:?"):
            title = link.text.strip()
            quality_match = re.search(r"(2160p|1080p|720p|480p|x264|x265|HEVC|AVC|DD[\+\d\.]*|AAC[\d\.]*|HQ|LQ|ESub)", title, re.IGNORECASE)
            quality = quality_match.group(0).upper() if quality_match else "UNKNOWN"
            magnets.append((quality, href))
    return magnets

def main():
    print("─" * 80)
    print("                         🎬 TamilMV CLI Scraper via RSS                          ")
    print("─" * 80)

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    for idx, entry in enumerate(entries, start=1):
        print(f"[{idx}] {entry.title.split(' (')[0].strip()}")

    try:
        choice = int(input("\n[?] Choose a movie/show to list magnet links: ")) - 1
        if choice < 0 or choice >= len(entries):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    selected = entries[choice]
    print(f"\n📌 Fetching magnets for: {selected.title}\n")
    magnets = extract_magnets(selected.description)

    if not magnets:
        print("❌ No magnet links found.")
        return

    for i, (quality, _) in enumerate(magnets, start=1):
        print(f"[{i}] {quality}")

    try:
        m_choice = int(input("\n[?] Choose a magnet link to view: ")) - 1
        if m_choice < 0 or m_choice >= len(magnets):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    print(f"\n🔗 Magnet Link:\n{magnets[m_choice][1]}\n")

if __name__ == "__main__":
    main()

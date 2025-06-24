import cloudscraper
import feedparser
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get(url, timeout=15)
        r.raise_for_status()
        feed = feedparser.parse(r.content)
        return feed.entries
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_magnets(description_html):
    soup = BeautifulSoup(description_html, "lxml")
    anchors = soup.find_all("a", href=True)
    magnets = []
    for a in anchors:
        href = a["href"]
        if href.startswith("magnet:?"):
            title = a.text.strip()
            # Extract quality from title
            quality = "UNKNOWN"
            match = re.search(r"(2160p|1080p|720p|480p|x264|x265|HEVC|AVC|DD\+?[0-9\.]*|AAC[0-9\.]*|ESub)",
                              title, re.IGNORECASE)
            if match:
                quality = match.group(1).upper()
            magnets.append((quality, href))
    return magnets

def main():
    print("─" * 80)
    print(" 🎬 TamilMV CLI Scraper via RSS ".center(80, "─"))
    print("─" * 80)

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    for i, e in enumerate(entries, 1):
        name = e.title.split(" (")[0].strip()
        print(f"[{i}] {name}")

    try:
        idx = int(input("\n[?] Choose a movie/show to list magnet links: ")) - 1
        if idx < 0 or idx >= len(entries):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    entry = entries[idx]
    print(f"\n📌 Fetching magnets for: {entry.title}\n")
    magnets = extract_magnets(entry.description)

    if not magnets:
        print("❌ No magnet links found.")
        return

    for j, (quality, _) in enumerate(magnets, 1):
        print(f"[{j}] {quality}")

    try:
        m_idx = int(input("\n[?] Choose a magnet link to view: ")) - 1
        if m_idx < 0 or m_idx >= len(magnets):
            raise IndexError
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    print(f"\n🔗 Magnet Link:\n{magnets[m_idx][1]}")

if __name__ == "__main__":
    main()

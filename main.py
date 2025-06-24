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
    magnets = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("magnet:?"):
            continue

        # Get nearby context
        quality_context = ""

        # Try previous sibling text
        if a.previous_sibling and isinstance(a.previous_sibling, str):
            quality_context += a.previous_sibling.strip()

        # Try parent text
        if a.parent and a.parent.text:
            quality_context += " " + a.parent.get_text(strip=True)

        # Try next sibling
        if a.next_sibling and isinstance(a.next_sibling, str):
            quality_context += " " + a.next_sibling.strip()

        # Search for common quality keywords
        match = re.search(
            r"(2160p|1080p|720p|480p|x264|x265|HEVC|AVC|DD\+?[0-9\.]*|AAC[0-9\.]*|ESub)",
            quality_context,
            re.IGNORECASE,
        )
        quality = match.group(1).upper() if match else "UNKNOWN"

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

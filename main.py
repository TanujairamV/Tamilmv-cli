import cloudscraper
import feedparser
from bs4 import BeautifulSoup
import re
import subprocess
import os

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def clear_terminal():
    os.system("clear" if os.name == "posix" else "cls")

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

def fetch_post_description(post_url):
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get(post_url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        desc = soup.find("div", class_="ipsType_richText")
        return desc.get_text(separator=" ", strip=True) if desc else ""
    except Exception as e:
        print(f"❌ Failed to fetch post page: {e}")
        return ""

def extract_magnet_links(description):
    magnets = re.findall(r'(magnet:\?xt=urn:btih:[^\s\"\'<>]+)', description)
    labeled = []
    for magnet in magnets:
        match = re.search(r'(\d{3,4}p|x264|x265|HEVC)', magnet, re.IGNORECASE)
        label = match.group(1).upper() if match else "UNKNOWN"
        labeled.append((label, magnet))
    return labeled

def main():
    clear_terminal()
    print("─" * 80)
    print(" " * 25 + "🎬 TamilMV CLI Scraper via RSS")
    print("─" * 80)

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    for i, e in enumerate(entries, 1):
        print(f"[{i}] {e.title.split(' (')[0].strip()}")

    choice = input("\n[?] Choose movie to fetch magnets: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(entries)):
        print("❌ Invalid selection.")
        return

    e = entries[int(choice) - 1]
    print(f"\n📌 Fetching magnets from post: {e.title}")
    desc = fetch_post_description(e.link)
    magnets = extract_magnet_links(desc)

    if not magnets:
        print("❌ No magnet links found.")
        return

    print("\n🎞️ Available Streams:")
    for j, (label, _) in enumerate(magnets, 1):
        print(f"[{j}] {label}")

    sel = input("\n[?] Choose a stream to play (or press Enter cancel): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(magnets)):
        print("❌ Cancelled.")
        return

    magnet = magnets[int(sel) - 1][1]
    print(f"\n🚀 Streaming via mpv:\n{magnet}\n")

    try:
        subprocess.run(["mpv", magnet])
    except FileNotFoundError:
        print("❌ mpv not found. Install it with: sudo pacman -S mpv")

if __name__ == "__main__":
    main()

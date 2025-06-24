import requests
from bs4 import BeautifulSoup
import feedparser
import re
from urllib.parse import urlparse, parse_qs, unquote
import pyperclip

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return feedparser.parse(response.content).entries
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_magnet_links(post_url):
    try:
        response = requests.get(post_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        description_div = soup.find("div", class_="ipsType_richText")
        if not description_div:
            return []

        # Search for all magnet links
        magnets = re.findall(r'magnet:\?xt=urn:btih:[a-zA-Z0-9&%=.?_\-:/]+', description_div.decode())
        return list(set(magnets))  # Remove duplicates
    except Exception as e:
        print(f"❌ Failed to fetch post content: {e}")
        return []

def extract_display_name(magnet_link):
    try:
        parsed = urlparse(magnet_link)
        params = parse_qs(parsed.query)
        return unquote(params.get("dn", ["Unknown Title"])[0])
    except Exception:
        return "Unknown Title"

def main():
    print("────────────────────────────────────────────────────────────────────────────────")
    print("                         🎬 TamilMV CLI Scraper via RSS                          ")
    print("────────────────────────────────────────────────────────────────────────────────")

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    print("\n🎞️ Available Movies:")
    for i, entry in enumerate(entries, start=1):
        print(f"[{i}] {entry.title.split('(')[0].strip()}")

    try:
        choice = int(input("\n[?] Choose a movie/show to view magnet links: "))
        if not (1 <= choice <= len(entries)):
            raise ValueError
    except ValueError:
        print("❌ Invalid selection.")
        return

    selected_entry = entries[choice - 1]
    magnets = extract_magnet_links(selected_entry.link)

    if not magnets:
        print("❌ No magnet links found.")
        return

    print("\n🔗 Magnet Titles:")
    titles = [extract_display_name(link) for link in magnets]
    for idx, title in enumerate(titles, 1):
        print(f"[{idx}] {title}")

    try:
        m_choice = int(input("\n[?] Choose a magnet link to copy: "))
        if 1 <= m_choice <= len(magnets):
            selected_magnet = magnets[m_choice - 1]
            pyperclip.copy(selected_magnet)
            print(f"\n✅ Magnet copied to clipboard:\n{selected_magnet}")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a valid number.")

if __name__ == "__main__":
    main()

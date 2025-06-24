import feedparser
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def clear_terminal():
    os.system("clear" if os.name == "posix" else "cls")

def fetch_rss_entries(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "xml")
        return soup.find_all("item")
    except Exception as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

def extract_title(entry):
    return entry.title.text.strip()

def extract_link(entry):
    return entry.link.text.strip()

def extract_description(entry):
    desc = entry.description.text.strip()
    return re.sub(r'<[^>]+>', '', desc)  # Strip HTML

def extract_magnet_links(description):
    magnet_pattern = re.compile(r'(magnet:\?xt=urn:btih:[^\s<"]+)')
    magnets = magnet_pattern.findall(description)

    labeled = []
    for magnet in magnets:
        quality_match = re.search(r'(\d{3,4}p)', magnet)
        label = quality_match.group(1) if quality_match else "UNKNOWN"
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

    titles = [extract_title(entry) for entry in entries]
    links = [extract_link(entry) for entry in entries]

    for i, title in enumerate(titles, 1):
        print(f"[{i}] {title} | {links[i-1]}")

    choice = input("\n[?] Choose a movie/show to stream: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(entries)):
        print("❌ Invalid choice.")
        return

    index = int(choice) - 1
    chosen_entry = entries[index]
    description = extract_description(chosen_entry)
    magnet_links = extract_magnet_links(description)

    if not magnet_links:
        print("❌ No magnet links found.")
        return

    print("\n🎞️ Available Streams:\n")
    for i, (quality, _) in enumerate(magnet_links, 1):
        print(f"[{i}] {quality}")

    stream_choice = input("\n[?] Choose a stream to play (or press Enter to cancel): ").strip()
    if not stream_choice.isdigit() or not (1 <= int(stream_choice) <= len(magnet_links)):
        print("❌ Cancelled.")
        return

    selected_link = magnet_links[int(stream_choice) - 1][1]
    print(f"\n🚀 Launching stream with mpv: {selected_link}\n")
    
    try:
        subprocess.run(["mpv", selected_link])
    except FileNotFoundError:
        print("❌ mpv is not installed or not found in PATH.")
        print("👉 Install with: sudo pacman -S mpv")

if __name__ == "__main__":
    main()

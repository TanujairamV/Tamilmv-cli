import requests
from bs4 import BeautifulSoup

def banner():
    print("─" * 80)
    print("🎬 TamilMV CLI Scraper via RSS".center(80))
    print("─" * 80)

def fetch_rss_entries(rss_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("item")

def search_entries(entries, query):
    query_lower = query.lower()
    return [entry for entry in entries if query_lower in entry.title.text.lower()]

def display_results(results):
    if not results:
        print("❌ No matching results found.")
        return

    print(f"✅ Found {len(results)} matching result(s):\n")
    for i, item in enumerate(results[:10], start=1):
        title = item.title.text.strip()
        link = item.link.text.strip()
        print(f"{i}. {title}\n   🔗 {link}\n")

def main():
    RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"
    banner()
    entries = fetch_rss_entries(RSS_URL)

    if not entries:
        print("❌ No entries found.")
        return

    query = input("🔍 Enter movie/show name: ").strip()
    if not query:
        print("❌ Empty input. Aborting.")
        return

    results = search_entries(entries, query)
    display_results(results)

if __name__ == "__main__":
    main()

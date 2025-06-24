# cli.py
from tamilmv import TamilmvParser

def main():
    print("🎬 TamilMV CLI Scraper")
    query = input("Enter the movie/show name: ").strip()
    parser = TamilmvParser(query)
    results = parser.get_search_results()

    if not results:
        print("❌ No results found.")
        return

    print("\nAvailable Results:\n")
    for idx, res in enumerate(results):
        print(f"[{idx + 1}] {res['title']}")

    try:
        choice = int(input("\nSelect one by number: ")) - 1
        if choice < 0 or choice >= len(results):
            raise ValueError()
    except ValueError:
        print("❌ Invalid choice.")
        return

    print(f"\nFetching torrents for: {results[choice]['title']}\n")
    torrents = parser.get_torrents_from_listing(results[choice]['link'])

    if not torrents:
        print("❌ No torrents found.")
    else:
        for i, t in enumerate(torrents):
            print(f"[{i + 1}] {t['name']}")
            print(f"     🔗 {t['link']}")

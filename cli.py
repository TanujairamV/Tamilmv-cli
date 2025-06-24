# cli.py
from tamilmv_browser import TamilMVBrowserScraper

def main():
    print("🎬 TamilMV CLI Scraper (Selenium Edition)")
    query = input("Enter the movie/show name: ").strip()
    scraper = TamilMVBrowserScraper(query)

    try:
        results = scraper.search()
        if not results:
            print("❌ No results found.")
            return

        print("\nAvailable Results:\n")
        for i, result in enumerate(results):
            print(f"[{i+1}] {result['title']}")

        try:
            choice = int(input("\nSelect one by number: ")) - 1
            if choice < 0 or choice >= len(results):
                raise ValueError()
        except ValueError:
            print("❌ Invalid selection.")
            return

        torrents = scraper.get_torrents(results[choice]["link"])
        if not torrents:
            print("❌ No torrents found.")
        else:
            print("\n🎞️ Torrents Found:\n")
            for i, t in enumerate(torrents):
                print(f"[{i+1}] {t['name']}")
                print(f"     🔗 {t['link']}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()

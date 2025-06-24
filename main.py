import requests
from bs4 import BeautifulSoup
import inquirer
import webbrowser
import os

RSS_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"

def fetch_rss_entries(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch RSS feed: {e}")
        return []

    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("item")

def display_menu(entries):
    choices = []
    for entry in entries:
        title = entry.title.text.strip()
        link = entry.link.text.strip()
        choices.append(f"{title} | {link}")
    return choices

def main():
    os.system("clear" if os.name == "posix" else "cls")
    print("────────────────────────────────────────────────────────────────────────────────")
    print("                         🎬 TamilMV CLI Scraper via RSS                          ")
    print("────────────────────────────────────────────────────────────────────────────────")

    entries = fetch_rss_entries(RSS_URL)
    if not entries:
        print("❌ No entries found.")
        return

    choices = display_menu(entries)
    questions = [
        inquirer.List(
            "selected",
            message="Choose a movie/show to open",
            choices=choices,
            carousel=True
        )
    ]
    answer = inquirer.prompt(questions)
    if answer:
        selected_entry = answer["selected"]
        selected_link = selected_entry.split("|")[-1].strip()
        print(f"🌐 Opening: {selected_link}")
        webbrowser.open(selected_link)

if __name__ == "__main__":
    main()

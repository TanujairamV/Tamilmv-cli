import feedparser
import webbrowser
from rich import print
from rich.prompt import Prompt
from rich.console import Console

RSS_FEED_URL = "https://www.1tamilmv.pet/index.php?/forums/forum/11-web-hd-itunes-hd-bluray.xml"
console = Console()

def fetch_rss_entries():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

def search_entries(entries, query):
    query_lower = query.lower()
    return [entry for entry in entries if query_lower in entry.title.lower()]

def display_entries(entries):
    for idx, entry in enumerate(entries, start=1):
        print(f"[cyan]{idx}. {entry.title}[/cyan]")
    print()

def get_user_choice(max_choice):
    while True:
        try:
            choice = int(Prompt.ask("🎯 Enter the number to open link (0 to exit)"))
            if 0 <= choice <= max_choice:
                return choice
        except ValueError:
            continue

def open_selected_link(link):
    print(f"[green]🚀 Opening: {link}")
    webbrowser.open(link)

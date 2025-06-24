from tamilmv.core import (
    fetch_rss_entries,
    search_entries,
    display_entries,
    get_user_choice,
    open_selected_link
)
from rich.console import Console
from rich.prompt import Prompt

def main():
    console = Console()
    console.rule("[bold green]🎬 TamilMV CLI Scraper via RSS")

    entries = fetch_rss_entries()
    if not entries:
        console.print("[red]❌ No entries found.")
        return

    query = Prompt.ask("🔍 Enter the movie/show name")
    matched = search_entries(entries, query)

    if not matched:
        console.print(f"[red]❌ No results for '{query}'")
        return

    display_entries(matched)
    choice = get_user_choice(len(matched))

    if choice == 0:
        return

    selected = matched[choice - 1]
    open_selected_link(selected.link)

if __name__ == "__main__":
    main()

# tamilmv.py
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class TamilmvParser:
    def __init__(self, user_query: str):
        self.user_query = user_query.strip()
        self.user_query_words = self.user_query.split()
        self.domain = "https://www.1tamilmv.one"
        self.endpoint = "index.php?/search/&q="

    def _process_listing(self, result):
        text = result.text.strip()
        if any(word.lower() in text.lower() for word in self.user_query_words):
            link = result.find('a', href=True)
            if link:
                return {
                    'title': text,
                    'link': self.domain + link['href']
                }

    def _fetch_torrent_links(self, url):
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            torrents = []
            for tag in soup.find_all('a', class_='ipsAttachLink', href=True):
                if ".srt" not in tag.text.lower():
                    torrents.append({
                        'name': tag.text.strip(),
                        'link': tag['href']
                    })
            return torrents
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
            return []

    def get_search_results(self):
        try:
            resp = requests.get(f'{self.domain}/{self.endpoint}{self.user_query}', timeout=10)
            if resp.status_code != 200:
                return []
            soup = BeautifulSoup(resp.content, 'html.parser')
            listings = soup.find_all("div", class_="ipsType_break ipsContained")
            results = list(filter(None, [self._process_listing(r) for r in listings]))
            return results
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []

    def get_torrents_from_listing(self, listing_url):
        return self._fetch_torrent_links(listing_url)

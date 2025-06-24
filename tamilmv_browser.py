# tamilmv_browser.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class TamilMVBrowserScraper:
    def __init__(self, query):
        self.query = query.strip()
        self.domain = "https://www.1tamilmv.pet"
        self.search_url = (
            f"{self.domain}/index.php?/search/&q={self.query}&search_and_or=and&search_in=titles&sortby=relevancy"
        )
        self._init_browser()

    def _init_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--lang=en-US")
        self.driver = webdriver.Chrome(options=chrome_options)

    def search(self):
        print(f"[DEBUG] Searching: {self.search_url}")
        self.driver.get(self.search_url)
        time.sleep(5)  # Wait for JS and Cloudflare
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listings = soup.find_all("div", class_="ipsType_break ipsContained")
        print(f"[DEBUG] Found {len(listings)} search results.")
        results = []
        for result in listings:
            link_tag = result.find("a", href=True)
            if link_tag:
                title = link_tag.text.strip()
                url = self.domain + link_tag["href"]
                results.append({"title": title, "link": url})
        return results

    def get_torrents(self, url):
        print(f"[DEBUG] Fetching torrents from: {url}")
        self.driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        torrents = []
        for tag in soup.find_all("a", class_="ipsAttachLink", href=True):
            if ".srt" not in tag.text.lower():
                torrents.append({
                    "name": tag.text.strip(),
                    "link": tag["href"]
                })
        return torrents

    def close(self):
        self.driver.quit()

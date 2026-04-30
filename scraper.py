from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

async def scrape_url(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle")
        html_content = await page.content()

        await browser.close()

        soup = BeautifulSoup(html_content, "html.parser")

        for element in soup(["script", "style"]):
            element.decompose()

        clean_text = soup.get_text(separator=" ", strip=True)

        return clean_text

async def crawl_website(base_url: str, max_pages: int = 5):
    visited_urls = set()
    urls_to_visit = [base_url]
    extracted_text = []

    base_domain = urlparse(base_url).netloc

    async with async_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = await browser.new_page()

        while urls_to_visit and len(visited_urls) < max_pages:
            current_url = urls_to_visit.pop(0)

            if current_url in visited_urls:
                continue

            print(f"Crawling:  {current_url}..")
            visited_urls.add(current_url)

            pass

        

if __name__ == "__main__":
    print("This file contains a function to scrape a website.")
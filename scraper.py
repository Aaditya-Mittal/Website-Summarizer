from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

async def scrape_url(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle")
        html_content = await page.content()

        await browser.close()

        soup = BeautifulSoup(html_content, "html.parser")

        for element in soup(["script", "style"]):
            element.decompose()

        clean_text = soup.get_text(separator=" ", strip=True)

        return clean_text

async def crawl_website(base_url: str, max_pages: int = 5, scroll: bool = False):
    visited_urls = set()
    urls_to_visit = [base_url]
    extracted_text = []

    base_domain = urlparse(base_url).netloc

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.new_page()

        while urls_to_visit and len(visited_urls) < max_pages:
            current_url = urls_to_visit.pop(0)

            if current_url in visited_urls:
                continue

            print(f"Crawling:  {current_url}..")
            visited_urls.add(current_url)

            try:
                await page.goto(current_url, wait_until="networkidle", timeout=15000)

                if scroll:
                    for _ in range(3):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(1000)
                    
                html_content = await page.content()
            
            except Exception as e:
                print(f"Skipping {current_url} due to error: {e}")
                continue
            
            soup = BeautifulSoup(html_content, "html.parser")

            if len(visited_urls) < max_pages:
                for link in soup.find_all("a", href=True):
                    full_url = urljoin(base_url, link["href"])
                    
                    if urlparse(full_url).netloc == base_domain and full_url not in visited_urls:
                        if full_url not in urls_to_visit:
                            urls_to_visit.append(full_url)

            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()
            
            clean_text = soup.get_text(separator=" ", strip=True)

            extracted_text.append(f"\n--- Data from {current_url} ---\n{clean_text}")

        await browser.close()

        return "\n".join(extracted_text)



        

if __name__ == "__main__":
    print("This file contains a function to scrape a website.")
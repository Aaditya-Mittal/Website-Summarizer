from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    print("This file contains a function to scrape a website.")
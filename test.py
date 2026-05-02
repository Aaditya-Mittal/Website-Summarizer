import asyncio
from scraper import crawl_website
from agent import summarize_text

async def main():
    content = await crawl_website("https://portfolio-aaditya-mittal.vercel.app/")
    result = await summarize_text(content)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
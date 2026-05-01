import asyncio
from scraper import crawl_website

async def main():
    content = await crawl_website("https://portfolio-aaditya-mittal.vercel.app/")
    print(content)

if __name__ == "__main__":
    asyncio.run(main())
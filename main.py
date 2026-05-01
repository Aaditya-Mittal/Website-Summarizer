from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import crawl_website
from agent import summarize_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods =["*"],
    allow_headers = ["*"]
)

class URLRequest(BaseModel):
    url : str
    scroll: bool = False

@app.post("/summarize")
async def summarize_endpoint(request: URLRequest):
    print(f"Received request for URL: {request.url}")

    crawled_text = await crawl_website(request.url, max_pages = 5, scroll=request.scroll)

    summary = await summarize_text(crawled_text)

    return {
        "url": request.url,
        "summary": summary
    }
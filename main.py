from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_url
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

@app.post("/summarize")
async def summarize_endpoint(request: URLRequest):
    print(f"Received request for URL: {request.url}")

    scraped_text = await scrape_url(request.url)

    summary = await summarize_text(scraped_text)

    return {
        "url": request.url,
        "summary": summary
    }
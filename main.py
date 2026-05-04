import sys
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from scraper import crawl_website
from agent import summarize_text_stream

# Force Windows to use the correct async event loop for Playwright
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class URLRequest(BaseModel):
    url : str
    scroll: bool = False

@app.post("/summarize")
async def summarize_endpoint(request: URLRequest):
    print(f"Received request for URL: {request.url}")

    crawled_text = await crawl_website(request.url, max_pages = 5, scroll=request.scroll)

    async def stream_generator():
        async for chunk in summarize_text_stream(crawled_text):
            yield chunk

    return StreamingResponse(stream_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
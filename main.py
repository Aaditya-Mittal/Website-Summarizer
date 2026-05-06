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
    allow_origins = ["*"], # Allows any Vercel URL to connect
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class URLRequest(BaseModel):
    url : str
    scroll: bool = False
    max_pages: int = 5  # 1 to 20, controlled by frontend

@app.get("/")
async def health_check():
    """Health check endpoint for cron jobs and uptime monitors."""
    return {"status": "ok", "message": "AI Website Summarizer API is running."}

@app.post("/summarize")
async def summarize_endpoint(request: URLRequest):
    print(f"Received request for URL: {request.url}")

    # Clamp max_pages to 1-20 range for safety
    pages = max(1, min(20, request.max_pages))
    # Scale timeout: ~5 seconds per page, minimum 30s
    crawl_timeout = max(30, pages * 5)

    try:
        crawled_text = await asyncio.wait_for(
            crawl_website(request.url, max_pages=pages, scroll=request.scroll),
            timeout=crawl_timeout
        )
    except asyncio.TimeoutError:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=504,
            content={"detail": "Crawling timed out. The website took too long to respond."}
        )
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error while crawling: {str(e)}"}
        )

    async def stream_generator():
        try:
            async for chunk in summarize_text_stream(crawled_text):
                yield chunk
        except Exception as e:
            print(f"Streaming error: {e}")
            yield f"\n\n[Error: The AI response was interrupted. Please try again.]"

    return StreamingResponse(stream_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
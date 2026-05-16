import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import urllib.parse
import os

app = FastAPI(title="TikTok No Watermark Downloader")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class DownloadRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/fetch")
async def fetch_tiktok_info(request: DownloadRequest):
    tiktok_url = request.url.strip()
    if not tiktok_url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    api_url = f"https://www.tikwm.com/api/?url={urllib.parse.quote(tiktok_url)}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            data = response.json()
            
            if data.get("code") != 0:
                return JSONResponse(status_code=400, content={"error": data.get("msg", "Failed to fetch video info")})
            
            video_data = data.get("data", {})
            return {
                "success": True,
                "id": video_data.get("id"),
                "title": video_data.get("title"),
                "cover": video_data.get("cover"),
                "no_wm_url": video_data.get("play"),
                "music_url": video_data.get("music"),
                "author": video_data.get("author", {}).get("nickname", "TikTok User"),
                "origin_url": tiktok_url
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feed")
async def get_tiktok_feed(region: str = "TR"):
    # TikWM Feed API
    feed_url = f"https://www.tikwm.com/api/feed/list?region={region}&count=10"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(feed_url)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download")
async def download_video(url: str, filename: str = "tiktok_video.mp4"):
    async def stream_video():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return StreamingResponse(stream_video(), media_type="video/mp4", headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

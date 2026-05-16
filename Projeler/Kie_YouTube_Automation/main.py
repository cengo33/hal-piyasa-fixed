import os
import logging
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv

from core.kie_client import KieClient
from core.youtube_publisher import YouTubePublisher

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

def run_daily_automation():
    logging.info("Starting Daily Video Production & YouTube Upload...")
    
    try:
        # 1. Initialize Clients
        kie = KieClient()
        youtube = YouTubePublisher(
            credentials_path="credentials.json", 
            token_path="token.json"
        )

        # 2. Generate Video Prompt
        # Burada her gün farklı bir içerik üretmek için LLM kullanılabilir veya bir liste üzerinden gidilebilir.
        # Şimdilik örnek bir prompt kullanıyoruz.
        today_str = datetime.now().strftime("%Y-%m-%d")
        prompt = f"A cinematic drone shot of a futuristic city with neon lights and flying cars, high quality, 4k, futuristic atmosphere, sunset lighting"
        video_title = f"Futuristic City Vision - {today_str}"
        video_desc = f"AI generated vision of a futuristic city. Created on {today_str} using Kie AI automation. #AI #Futuristic #City #Cinematic"

        # 3. Create Kie AI Task
        logging.info(f"Creating Kie AI task with prompt: {prompt}")
        task_id = kie.create_video_task(prompt)
        logging.info(f"Task created. Task ID: {task_id}")

        # 4. Wait for Video
        video_url = kie.poll_status(task_id)
        logging.info(f"Video produced! URL: {video_url}")

        # 5. Download Video
        temp_path = f"temp/video_{today_str}.mp4"
        kie.download_video(video_url, temp_path)
        logging.info(f"Video downloaded to {temp_path}")

        # 6. Upload to YouTube
        youtube.upload_video(
            file_path=temp_path,
            title=video_title,
            description=video_desc
        )
        
        logging.info("==========================================")
        logging.info("Daily Automation Completed Successfully!")
        logging.info("==========================================")

    except Exception as e:
        logging.error(f"Automation Failed: {e}", exc_info=True)

if __name__ == "__main__":
    # Hemen bir kere çalıştır (test için)
    # run_daily_automation()

    # Her gün saat 10:00'da çalışacak şekilde ayarla
    schedule.every().day.at("10:00").do(run_daily_automation)

    logging.info("Automation scheduler started. Waiting for 10:00 AM every day...")
    while True:
        schedule.run_pending()
        time.sleep(60)

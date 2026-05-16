import logging
import os
from core.youtube_publisher import YouTubePublisher

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_upload():
    logging.info("Testing YouTube OAuth2 & Upload...")
    
    try:
        publisher = YouTubePublisher(
            credentials_path="credentials.json",
            token_path="token.json"
        )
        
        # Test Upload (as Private so it doesn't bother subscribers)
        video_path = "temp/dummy_test.mp4"
        if not os.path.exists(video_path):
            logging.error(f"Test video not found at {video_path}")
            return
            
        logging.info("Starting test upload (Private mode)...")
        video_id = publisher.upload_video(
            file_path=video_path,
            title="Antigravity Test Upload",
            description="Testing automated upload pipeline.",
            privacy_status="private"
        )
        
        print(f"\n✅ YOUTUBE TEST BAŞARILI!")
        print(f"Video ID: {video_id}")
        print(f"URL: https://www.youtube.com/watch?v={video_id}")

    except Exception as e:
        logging.error(f"YouTube Test Failed: {e}")

if __name__ == "__main__":
    test_upload()

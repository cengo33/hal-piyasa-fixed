import os
import logging
from dotenv import load_dotenv
from core.kie_client import KieClient

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def test_kie():
    logging.info("Testing Kie AI Video Generation...")
    
    try:
        kie = KieClient()
        
        # Test Prompt
        prompt = "A high-tech laboratory with glowing blue interfaces and robots working, cinematic, 4k, futuristic"
        logging.info(f"Creating task with prompt: {prompt}")
        
        task_id = kie.create_video_task(prompt)
        logging.info(f"Task ID: {task_id}")
        
        logging.info("Waiting for video to be produced (this may take 2-5 minutes)...")
        video_url = kie.poll_status(task_id, interval=15)
        logging.info(f"Success! Video URL: {video_url}")
        
        # Download
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        temp_path = "temp/test_video.mp4"
        kie.download_video(video_url, temp_path)
        logging.info(f"Video downloaded to {temp_path}")
        
        print(f"\n✅ TEST BAŞARILI!")
        print(f"Video URL: {video_url}")
        print(f"Lokal Dosya: {os.path.abspath(temp_path)}")

    except Exception as e:
        logging.error(f"Test Failed: {e}")

if __name__ == "__main__":
    test_kie()

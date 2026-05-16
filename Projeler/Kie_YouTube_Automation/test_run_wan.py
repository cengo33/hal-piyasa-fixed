import os
import logging
from dotenv import load_dotenv
from core.kie_client import KieClient

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def test_kie():
    logging.info("Testing Kie AI Video Generation (using Wan 2.6 - cheaper model)...")
    
    try:
        kie = KieClient()
        
        # Test Prompt
        prompt = "A high-tech laboratory with glowing blue interfaces and robots working, cinematic, 4k, futuristic"
        logging.info(f"Creating task with prompt: {prompt}")
        
        # We'll call the low level task creation to use wan-2.6
        url = f"https://api.kie.ai/api/v1/jobs/createTask"
        payload = {
            "model": "wan-2.6",
            "input": {
                "prompt": prompt,
                "resolution": "1080p",
                "aspect_ratio": "16:9",
                "duration": 5
            }
        }
        
        import requests
        response = requests.post(url, headers=kie.headers, json=payload)
        data = response.json()
        
        if data.get("code") != 200:
            raise Exception(f"Kie AI Task Creation Failed: {data.get('msg')}")
            
        task_id = data["data"]["taskId"]
        logging.info(f"Task ID: {task_id}")
        
        logging.info("Waiting for video to be produced...")
        video_url = kie.poll_status(task_id, interval=15)
        logging.info(f"Success! Video URL: {video_url}")
        
        # Download
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        temp_path = "temp/test_video_wan.mp4"
        kie.download_video(video_url, temp_path)
        logging.info(f"Video downloaded to {temp_path}")
        
        print(f"\n✅ TEST BAŞARILI!")
        print(f"Video URL: {video_url}")

    except Exception as e:
        logging.error(f"Test Failed: {e}")

if __name__ == "__main__":
    test_kie()

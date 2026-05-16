import os
import logging
import requests
import json
import time
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def test_image():
    logging.info("Testing Kie AI Image Generation (Nano Banana 2)...")
    
    api_key = os.getenv("KIE_AI_API_KEY")
    base_url = "https://api.kie.ai/api/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 1. Create Task
        prompt = "A majestic eagle flying over snow-capped mountains, cinematic lighting, 4k, hyper-realistic"
        logging.info(f"Creating image task with prompt: {prompt}")
        
        url = f"{base_url}/jobs/createTask"
        payload = {
            "model": "nano-banana-2",
            "input": {
                "prompt": prompt,
                "aspect_ratio": "16:9"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if data.get("code") != 200:
            raise Exception(f"Kie AI Task Creation Failed: {data.get('msg')}")
            
        task_id = data["data"]["taskId"]
        logging.info(f"Task ID: {task_id}")
        
        # 2. Poll Status
        logging.info("Waiting for image to be produced (usually ~30-60 seconds)...")
        image_url = None
        
        for _ in range(20):
            status_url = f"{base_url}/jobs/recordInfo?taskId={task_id}"
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()
            
            state = status_data.get("data", {}).get("state")
            if state == "success":
                result_json = json.loads(status_data["data"].get("resultJson"))
                image_url = result_json.get("resultUrls")[0]
                break
            elif state in ["failed", "fail"]:
                raise Exception(f"Task failed: {status_data['data'].get('failMsg')}")
            
            time.sleep(10)
            
        if not image_url:
            raise Exception("Timeout waiting for image.")
            
        logging.info(f"Success! Image URL: {image_url}")
        
        # 3. Download
        if not os.path.exists("temp"):
            os.makedirs("temp")
            
        temp_path = "temp/test_image.jpg"
        img_data = requests.get(image_url).content
        with open(temp_path, 'wb') as f:
            f.write(img_data)
            
        print(f"\n✅ GÖRSEL TESTİ BAŞARILI!")
        print(f"URL: {image_url}")
        print(f"Lokal Dosya: {os.path.abspath(temp_path)}")

    except Exception as e:
        logging.error(f"Image Test Failed: {e}")

if __name__ == "__main__":
    test_image()

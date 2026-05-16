import requests
import time
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class KieClient:
    def __init__(self):
        self.api_key = os.getenv("KIE_AI_API_KEY")
        self.base_url = "https://api.kie.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_video_task(self, prompt, model="kling-3.0/video"):
        """
        Kie AI üzerinde video üretim görevi oluşturur.
        """
        url = f"{self.base_url}/jobs/createTask"
        payload = {
            "model": model,
            "input": {
                "prompt": prompt,
                "duration": "5",
                "aspect_ratio": "16:9",
                "mode": "std",
                "multi_shots": False,
                "sound": True
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == 200:
            return data["data"]["taskId"]
        else:
            raise Exception(f"Kie AI Task Creation Failed: {data.get('msg')}")

    def poll_status(self, task_id, interval=30, max_attempts=60):
        """
        Görevin tamamlanmasını bekler.
        """
        url = f"{self.base_url}/jobs/recordInfo?taskId={task_id}"
        
        for attempt in range(max_attempts):
            logging.info(f"Polling Kie AI task status (Attempt {attempt+1}/{max_attempts})...")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # recordInfo'da code 200 olsa bile state'e bakmalıyız
            # resultJson içinden parse edeceğiz
            state = data.get("data", {}).get("state")
            
            if state == "success":
                import json
                result_json_str = data["data"].get("resultJson")
                if result_json_str:
                    result_data = json.loads(result_json_str)
                    urls = result_data.get("resultUrls", [])
                    if urls:
                        return urls[0]
                raise Exception("Kie AI task success but no URL found.")
            
            elif state in ["failed", "fail"]:
                fail_msg = data["data"].get("failMsg", "Unknown error")
                raise Exception(f"Kie AI Task Failed: {fail_msg}")
            
            elif state in ["processing", "waiting", "pending"]:
                time.sleep(interval)
            else:
                logging.warning(f"Unexpected state: {state}")
                time.sleep(interval)
                
        raise Exception("Kie AI Task Timeout")

    def download_video(self, video_url, output_path):
        """
        Üretilen videoyu indirir.
        """
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_path

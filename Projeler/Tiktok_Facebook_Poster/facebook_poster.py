import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

def post_video_to_facebook(video_path, description):
    """
    Uploads a video to a Facebook Page using the Graph API.
    """
    if not PAGE_ID or not PAGE_ACCESS_TOKEN:
        print("Error: FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN is missing in .env")
        return False

    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos"
    
    # We use multipart/form-data to upload the local video file
    try:
        with open(video_path, 'rb') as video_file:
            files = {
                'source': video_file
            }
            data = {
                'access_token': PAGE_ACCESS_TOKEN,
                'description': description
            }
            
            print(f"Uploading video {video_path} to Facebook...")
            response = requests.post(url, data=data, files=files)
            
            if response.status_code == 200:
                print("Successfully posted video to Facebook!")
                print("Response:", response.json())
                return True
            else:
                print(f"Failed to post video. Status code: {response.status_code}")
                print("Response:", response.text)
                return False
    except Exception as e:
        print(f"Exception during Facebook upload: {e}")
        return False

if __name__ == "__main__":
    # Test uploading
    test_file = input("Enter path to a video file: ")
    test_desc = input("Enter a description: ")
    if test_file and test_desc:
        post_video_to_facebook(test_file, test_desc)

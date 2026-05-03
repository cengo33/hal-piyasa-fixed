import os
import sys
from tiktok_downloader import download_tiktok_video
from facebook_poster import post_video_to_facebook

def process_tiktok_to_facebook(tiktok_url, custom_description=None):
    print(f"Starting process for: {tiktok_url}")
    
    # 1. Download TikTok video
    print("Downloading video from TikTok...")
    video_path, video_title = download_tiktok_video(tiktok_url)
    
    if not video_path or not os.path.exists(video_path):
        print("Failed to download video. Aborting.")
        return False
        
    print(f"Video downloaded successfully: {video_path}")
    
    # 2. Prepare description
    description = custom_description if custom_description else f"{video_title}\n\n#tarım #ziraat #çiftçi"
    
    # 3. Upload to Facebook
    print("Uploading to Facebook Page...")
    success = post_video_to_facebook(video_path, description)
    
    # 4. Cleanup (optional)
    if success:
        print("Process completed successfully!")
        # Uncomment below to delete the video after successful upload
        # os.remove(video_path)
        # print(f"Deleted local file: {video_path}")
    else:
        print("Failed to upload video to Facebook.")
        
    return success

if __name__ == "__main__":
    print("=== TikTok to Facebook Page Auto-Poster ===")
    print("This script downloads a TikTok video and uploads it to your Facebook Page.")
    
    while True:
        url = input("\nEnter TikTok URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
            
        if not url:
            continue
            
        desc = input("Enter description for Facebook (leave blank to use TikTok title): ").strip()
        
        process_tiktok_to_facebook(url, desc if desc else None)

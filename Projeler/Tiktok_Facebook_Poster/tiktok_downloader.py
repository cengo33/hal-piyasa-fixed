import yt_dlp
import os

def download_tiktok_video(url, output_path="downloads"):
    """
    Downloads a TikTok video without watermark using yt-dlp.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    ydl_opts = {
        'outtmpl': f'{output_path}/%(id)s.%(ext)s',
        'quiet': False,
        'no_warnings': True,
        # yt-dlp usually tries to fetch the best video, which for TikTok is often the unwatermarked version
        # Use single format to avoid ffmpeg requirement (b)
        'format': 'b',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get('id', None)
            ext = info_dict.get('ext', 'mp4')
            video_title = info_dict.get('title', 'Tiktok Video')
            
            file_path = f"{output_path}/{video_id}.{ext}"
            return file_path, video_title
    except Exception as e:
        print(f"Error downloading TikTok video: {e}")
        return None, None

if __name__ == "__main__":
    # Test with a sample URL if needed
    test_url = input("Enter a TikTok URL to test download: ")
    if test_url:
        path, title = download_tiktok_video(test_url)
        print(f"Downloaded to: {path}")
        print(f"Title: {title}")

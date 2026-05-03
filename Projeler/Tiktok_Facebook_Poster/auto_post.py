import os
import time
from main import process_tiktok_to_facebook

LINKS_FILE = "links.txt"

def run_auto_post():
    print("=== Auto Post Started ===")
    
    if not os.path.exists(LINKS_FILE):
        print(f"Error: {LINKS_FILE} not found. Please add TikTok URLs to this file.")
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print(f"{LINKS_FILE} is empty. No videos to post.")
        return

    # Take the first line
    first_line = lines[0]
    
    # Parse URL and optional description (separated by comma or pipe)
    parts = first_line.split('|', 1)
    url = parts[0].strip()
    desc = parts[1].strip() if len(parts) > 1 else None

    print(f"Processing URL: {url}")
    success = process_tiktok_to_facebook(url, desc)

    if success:
        # Remove the processed line from the file
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            for line in lines[1:]:
                f.write(line + "\n")
        print("Successfully posted and removed from queue.")
    else:
        print("Failed to post. Keeping in queue for the next run.")

if __name__ == "__main__":
    run_auto_post()

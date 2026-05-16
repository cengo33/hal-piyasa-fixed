import os
import time
import json
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# State management
is_running = False
logs = []

def add_log(message, type="info"):
    log_entry = {"time": time.strftime("%H:%M:%S"), "message": message, "type": type}
    logs.append(log_entry)
    if len(logs) > 100:
        logs.pop(0)
    socketio.emit('new_log', log_entry)
    logger.info(message)

def run_inviter(post_url):
    global is_running
    is_running = True
    add_log(f"Starting invitation process for: {post_url}", "success")
    
    with sync_playwright() as p:
        # Launch browser with persistence for cookies
        user_data_dir = os.path.join(os.getcwd(), "fb_session")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, # Set to False so user can see/login if needed
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.new_page()
        
        try:
            add_log("Navigating to Facebook...")
            page.goto(post_url)
            
            # Check if we need to login
            if "login" in page.url:
                add_log("Please login to Facebook in the browser window.", "warning")
                # Wait for user to login manually if needed, or check for session
                page.wait_for_selector('text="Reactions"', timeout=60000)
            
            # Find the reactions link/button and click it
            add_log("Searching for reactions...")
            # This selector might need adjustment based on FB's dynamic classes
            # Usually it's something like "span[role='button']" containing numbers
            try:
                # Try clicking the likes/reactions summary
                reactions_selector = "span[role='toolbar']" # This is a placeholder
                # More reliable: look for the count
                page.click("a[href*='reaction/profile']", timeout=10000)
                add_log("Opened reactions modal.", "info")
            except Exception as e:
                add_log(f"Could not find reactions modal: {str(e)}", "error")
                return

            # Wait for the modal to load
            page.wait_for_selector("div[role='dialog']", timeout=10000)
            
            invite_count = 0
            while is_running:
                # Find all "Invite" buttons
                # The text "Invite" might be localized, so we should consider "Davet Et" for Turkish users
                invite_buttons = page.query_selector_all('div[role="button"]:has-text("Invite"), div[role="button"]:has-text("Davet Et")')
                
                if not invite_buttons:
                    add_log("No more invite buttons found on current view. Scrolling...", "info")
                    # Scroll the modal
                    modal = page.query_selector("div[role='dialog'] .m9osr9ce") # FB modal content class is often dynamic
                    if modal:
                        page.evaluate("arg => arg.scrollTop += 500", modal)
                    else:
                        page.keyboard.press("PageDown")
                    
                    time.sleep(2)
                    # Check again
                    invite_buttons = page.query_selector_all('div[role="button"]:has-text("Invite"), div[role="button"]:has-text("Davet Et")')
                    if not invite_buttons:
                        add_log("Finished processing reactions.", "success")
                        break

                for btn in invite_buttons:
                    if not is_running: break
                    try:
                        # Ensure button is visible
                        btn.scroll_into_view_if_needed()
                        btn.click()
                        invite_count += 1
                        add_log(f"Sent invitation #{invite_count}", "info")
                        time.sleep(1) # Small delay to avoid rate limits
                    except Exception as e:
                        logger.error(f"Error clicking button: {e}")
                
                time.sleep(2)

        except Exception as e:
            add_log(f"Error during execution: {str(e)}", "error")
        finally:
            browser.close()
            is_running = False
            add_log("Process completed.", "success")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global is_running
    if is_running:
        return jsonify({"status": "error", "message": "Already running"})
    
    post_url = request.json.get('url')
    if not post_url:
        return jsonify({"status": "error", "message": "URL is required"})
    
    import threading
    threading.Thread(target=run_inviter, args=(post_url,)).start()
    return jsonify({"status": "success"})

@app.route('/stop', methods=['POST'])
def stop():
    global is_running
    is_running = False
    return jsonify({"status": "success"})

@app.route('/logs')
def get_logs():
    return jsonify(logs)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)

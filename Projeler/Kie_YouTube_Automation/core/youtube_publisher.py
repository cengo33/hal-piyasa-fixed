import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for YouTube Upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class YouTubePublisher:
    def __init__(self, credentials_path="credentials.json", token_path="token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.youtube = self._get_service()

    def _get_service(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"YouTube API Credentials file not found at {self.credentials_path}. "
                        "Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        return build('youtube', 'v3', credentials=creds)

    def upload_video(self, file_path, title, description, category_id="22", privacy_status="public"):
        """
        YouTube'a video yükler.
        """
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }

        media = MediaFileUpload(
            file_path,
            mimetype='video/*',
            resumable=True
        )

        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        logging.info(f"Uploading video: {title}...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logging.info(f"Upload progress: {int(status.progress() * 100)}%")

        logging.info(f"Video uploaded successfully! ID: {response['id']}")
        return response['id']

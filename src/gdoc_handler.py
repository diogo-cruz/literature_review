import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pathlib import Path
import pickle

class GoogleDocHandler:
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    
    def __init__(self, doc_id: str):
        """Initialize the Google Docs handler.
        
        Args:
            doc_id: The ID of the Google Doc to access
        """
        self.doc_id = doc_id
        self.creds = self._get_credentials()
        self.service = build('docs', 'v1', credentials=self.creds)
        
    def _get_credentials(self) -> Credentials:
        """Get or refresh Google API credentials."""
        creds = None
        token_path = Path.home() / '.gdocs_token.pickle'
        
        # Load existing credentials if available
        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.getenv('GOOGLE_CREDENTIALS_PATH'),
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            # Save credentials
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        return creds
        
    def get_document_content(self) -> str:
        """Get the content of the Google Doc.
        
        Returns:
            The text content of the document
        """
        document = self.service.documents().get(documentId=self.doc_id).execute()
        content = document.get('body').get('content')
        
        text = ""
        for element in content:
            if 'paragraph' in element:
                for para_element in element['paragraph']['elements']:
                    if 'textRun' in para_element:
                        text += para_element['textRun']['content']
                        
        return text.strip() 
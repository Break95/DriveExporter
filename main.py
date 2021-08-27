# Drive Exporter

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


mime_odt = {
    'document': 'application/vnd.oasis.opendocument.text',
    'spreadsheet': 'application/x-vnd.oasis.opendocument.spreadsheet',
    'presentation': 'application/vnd.oasis.opendocument.presentation'
}

mime_gdocs = {
   'document': 'application/vnd.google-apps.document',
   'spreadsheet': 'application/vnd.google-apps.spreadsheet',
   'presentation': 'application/vnd.google-apps.presentation'
}

def authentication():
   scopes = 'https://www.googleapis.com/auth/drive'
   creds = None

   if os.path.exists('creds/token.json'):
      creds = Credentials.from_authorized_user_file('creds/token.json', scopes)

   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file(
            'creds/client_secret.json', scopes)
         creds = flow.run_local_server(port=0)
      with open('creds/token.json', 'w') as token:
         token.write(creds.to_json())

   return build('drive', 'v3', credentials=creds)


def parse_tree(drive):
   # Files in trash are also read along with files shared with me.
   files = drive.files().list(
      q="mimeType = 'application/vnd.google-apps.document'",
      fields="nextPageToken, files(id, name), incompleteSearch").execute().get('files', [])



   for f in files:
      print(f['name'])

   return


def export(file_id, doc_type):
   return


def human_config():
   origin = input('')
   mimes = input('Choose a format: [A]ll, [D]ocument, [S]preadsheet, [P]resentation')
   dest = input('Save new files in same folder? [Y/N]')


if __name__ == '__main__':

    drive = authentication()
    parse_tree(drive)
    # human_config()

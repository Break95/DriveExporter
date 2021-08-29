# Drive Exporter

from __future__ import print_function
import os.path
import io
import re
from odf.opendocument import load
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
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


scopes = 'https://www.googleapis.com/auth/drive'


def authentication():
   """
   """
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


def process_files(drive):
   """
   """
   while True:
      nextPageToken = None
      results = drive.files().list(
         q="mimeType = '" + mime_gdocs["document"] + "' and 'me' in owners",
         pageToken=nextPageToken,
         pageSize=1000,
         fields="nextPageToken, files(id, name)").execute()

      export_files(results.get('files', []))
      nextPageToken = results.get('nextPageToken', None)

      if not nextPageToken:
         break

   return


def export_files(files):
   """
   """
   for f in files:
         print('Exporting:' , f['name'])

         export_req = drive.files().export(
            fileId=f['id'],
            mimeType=mime_odt["document"])

         fh = io.BytesIO()
         downloader = MediaIoBaseDownload(fh, export_req)
         done = False

         # Wait for download to finish. For some reason if file is too big too export
         # the exception is generated during the download and not during the
         # export call. ??????????
         try:
            while done is False:
               status, done = downloader.next_chunk()
            load(fh).save('/tmp/' + re.escape(f['name'].replace('/', '_')))
         except:
               print('\tError exporting ', f['name'])

   return


def delete_files(drive):
   return


def query_builder(config):
   """
   Buils the query for the Drive API call using the provided parameters.

   Arguments:
   config -- Dictionary containing the configured parameters for the Drive API call.
   """
   return


def condig_params(params):
   return


def config_human():
   """
   """
   origin = input('Choose an origin: [M]y Dirve, [S]hared with me, [B]oth ')
   mimes = input('Choose a format: [A]ll, [D]ocument, [S]preadsheet, [P]resentation ')
   dest = input('Save new files in same folder? [Y/N] ')


if __name__ == '__main__':

    drive = authentication()
    process_files(drive)
    # human_config()

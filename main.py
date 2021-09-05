# Drive Exporter

from __future__ import print_function
import os.path
import io
import sys
import re
import tempfile
from datetime import datetime
from odf.opendocument import load
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


mime_odt = {
    'application/vnd.google-apps.document': 'application/vnd.oasis.opendocument.text',
    'application/vnd.google-apps.spreadsheet': 'application/x-vnd.oasis.opendocument.spreadsheet',
    'application/vnd.google-apps.presentation': 'application/vnd.oasis.opendocument.presentation'
}


mime_gdocs = {
   'D': 'application/vnd.google-apps.document',
   'S': 'application/vnd.google-apps.spreadsheet',
   'P': 'application/vnd.google-apps.presentation'
}

query_params = {
   'origin': '',
   'mime_in': '',
   'mime_out': '',
   'keep_original': True,
   'destination': '/tmp/',
   'trashed': False
}


origin = {
   'M': '',
   'S': '',
   'B': ''
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
         q=query_builder(),
         pageToken=nextPageToken,
         pageSize=1000,
         fields="nextPageToken, files(id, name, mimeType)").execute()

      # Export files of the current page.
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
            mimeType=mime_odt[f['mimeType']])

         fh = io.BytesIO()
         downloader = MediaIoBaseDownload(fh, export_req)
         done = False

         # Wait for download to finish. For some reason if file is too big too export
         # the exception is generated during the download and not during the
         # export call. ??????????
         try:
            while done is False:
               status, done = downloader.next_chunk()
            load(fh).save(path + re.escape(f['name'].replace('/', '_')))
         except:
               print('\tError exporting ', f['name'])

   return


def delete_files(drive):
   return


def query_builder():
   """
   Buils the query for the Drive API call using the provided parameters.
   """
   query = "("
   print(query_params['mime_in'])
   for mime_type in query_params['mime_in']:
      query = query + "mimeType='" + mime_type + "' or "

   query = query[:len(query) - 3] + ") and "

   query += "'me' in owners"
   print(query)
   return query


def config_params():
   return


def config_human():
   """
   """
   origin = input('Choose an origin: [M]y Dirve, [S]hared with me, [B]oth ')
   query_params['origin'] = origin


   trashed = input('Include trashed files [Y/N]? (Note: Trashed files only include those deleted by you where you were the owner) ').upper()
   if trashed == 'Y':
      query_params['trashed'] = True


   mime_in = input('Choose a format: [A]ll, [D]ocument, [S]preadsheet, [P]resentation ').upper()
   if mime_in == 'A':
     query_params['mime_in'] = mime_gdocs.values()
     query_params['mime_out'] = mime_odt.values()
   else:
      query_params['mime_in'] = [mime_gdocs[mime_in]]
      query_params['mime_out'] = mime_odt[mime_gdocs[mime_in]]


   dest = input('Specify a path to store the files (Default is "/tmp/"): ')
   if os.path.exists(dest):
      query_params['destination'] = dest


   keep = input('Keep original file [(Y)/n]? ').lower()
   if keep == 'n':
      query_params['keep_original'] = False

path = os.getcwd() + '/exports/' + datetime.now().strftime('%c') + '/'

if __name__ == '__main__':
   if(not os.path.isdir(os.getcwd() + '/exports/')):
      os.mkdir(os.getcwd() + '/exports')

   os.mkdir(path)

   if len(sys.argv) == 1:
      config_human()
   else:
      config_params()

   drive = authentication()
   process_files(drive)

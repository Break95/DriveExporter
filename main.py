# Drive Exporter

from __future__ import print_function
import os.path
import io
import sys
import re
from datetime import datetime
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


mime_human_outs  = {
   'application/vnd.google-apps.document': ['Document', '[P]DF, [O]DF'],
   'application/vnd.google-apps.spreadsheet': ['Spreadsheet', '[C]SV, [P]DF, [O]DF'],
   'application/vnd.google-apps.presentation' :  ['Presentation', '[P]DF, [O]DF']
}

mime_gdocs = {
   'D': 'application/vnd.google-apps.document',
   'S': 'application/vnd.google-apps.spreadsheet',
   'P': 'application/vnd.google-apps.presentation'
}


mime_export = {
   'P': 'application/pdf',
   'C': 'text/csv'
}

config = {
   'origin': '',
   'mime_in': [],
   'mime_out': [],
   'keep_original': True,
   'destination': '/tmp/',
   'trashed': False
}


origin = {
   'M': '"me" in owners',
   'S': 'sharedWithMe',
   'B': 'sharedWithMe and "me" in owners'
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

      if not nextPageToken: #If we have finished with all the pages end.
         break

   return

def export_files(files):
   """
   """
   for f in files:
      print('Exporting:' , f['name'])

      export_req = drive.files().export(
         fileId=f['id'],
         mimeType=config['mime_out'][(config['mime_in']).index(f['mimeType'])])

      file_name = path + f['name'].replace('/','_')

      fh = io.FileIO(file_name, 'wb')
      downloader = MediaIoBaseDownload(fh, export_req)
      done = False

      # Wait for download to finish. For some reason if file is too big too export
      # the exception is generated during the download and not during the
      # export call. ??????????
      try:
         while done is False:
            status, done = downloader.next_chunk()

      except:
         print('\tError exporting ', f['name'])

   return


def delete_files(drive):
   print('WARNING! ALL FETCHED FILES. EXPORTED OR NOT (DUE TO ERRORS). WILL BE DOWNLOADED.')
   return


def query_builder():
   """
   Buils the query for the Drive API call using the provided parameters.
   """
   query = "("
   print(config['mime_in'])
   for mime_type in config['mime_in']:
      query = query + "mimeType='" + mime_type + "' or "

   query = query[:len(query) - 3] + ") and "

   query += "'me' in owners"
   return query


def set_config_params():
   return


def set_config_human():
   """
   """
   origin = ''
   while origin not in ['M', 'm', 'S', 's', 'B', 'b']:
      origin = input('Choose an origin [M]y Dirve, [S]hared with me, [B]oth: ')
   config['origin'] = origin


   trashed = input('Include trashed files [Y/N]? (Note: Trashed files only include those deleted by you where you were the owner) ').upper()
   if trashed == 'Y':
      config['trashed'] = True


   mime_in = input('Choose a format: [A]ll, [D]ocument, [S]preadsheet, [P]resentation ').upper()
   if mime_in == 'A':
      config['mime_in'] = list(mime_gdocs.values())
   else:
      config['mime_in'] = [mime_gdocs[mime_in]]

   for mime in config['mime_in']:
      export_type = ''

      while export_type not in ['O', 'o', 'C', 'c', 'P', 'p']:
         export_type = input('Choose an output format for ' +
                                            mime_human_outs[mime][0] + ' ' +
                                            mime_human_outs[mime][1] + ': ')

      if(export_type in ['O', 'o']):
         config['mime_out'].append(mime_odt[mime])
      else:
         config['mime_out'].append(mime_export[export_type.upper()])


   dest = input('Specify a path to store the files (Default is "./exports"): ')
   if os.path.exists(dest):
      config['destination'] = dest


   keep = input('Keep original file [(Y)/n]? ').lower()
   if keep == 'n':
      config['keep_original'] = False

path = os.getcwd() + '/exports/' + datetime.now().strftime('%c') + '/'

if __name__ == '__main__':
   if(not os.path.isdir(os.getcwd() + '/exports/')):
      os.mkdir(os.getcwd() + '/exports')

   os.mkdir(path)

   # Configuration
   if len(sys.argv) == 1:
      set_config_human()
   else:
      set_config_params()

   # Auth
   drive = authentication()

   # Export & Download
   process_files(drive)

   # Remove original if requested.
   if(not config['keep_original']):
      delete_files()

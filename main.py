# Drive Exporter

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

mime_types = {
    'docuemnt': 'application/vnd.oasis.opendocument.text',
    'spreadsheet': 'application/x-vnd.oasis.opendocument.spreadsheet',
    'presentation': 'application/vnd.oasis.opendocument.presentation'
}

def authentication():
   scopes = 'https://www.googleapis.com/auth/drive'
   store = file.Storage('storage.json')
   creds = store.get()
   if not creds or creds.invalid:
       flow = client.flow_from_clientsecrets('client_id.json', scopes)
       creds = tools.run_flow(flow, store)
       drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return drive

def parse_tree(drive):

   
def export(file_id, doc_type):

if __name__ == '__main__':
    print_hi('PyCharm')

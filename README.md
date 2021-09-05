# Drive Exporter
CLI utility to export GoogleDoc Drive files into OpenDocument, PDF, CSV and others depending on the original format.

This project uses the Google Drive API v3. This project has been developed for personal use, therefore the app is unpublished. If you want to use it you will have to:

1. Create a Google Cloud Platform project
2. Enable a Google Workspace API.
3. Add your email to test users in the Google Cloud Console: API and Services -> OAuth consent screen -> Test users. 

[Guide for steps 1 and 2](https://developers.google.com/workspace/guides/create-project)

## Current issues 
Large files (i.e. documents containing high quality images) can't be downloaded.

## Usage
The script supports passing arguments or interactively set the through the command line.

### Command Line Arguments
TODO

### Interactive
TODO


## Supported formats:
    
- Document
- Spreadsheet
- Presentation

## Application Flow 

1. Select Origin:
   - My Drive
   - TODO: Shared With Me
   - TODO: My Drive + Shared With Me
   - TODO: Optional: + Trashed
  
2. Select file types to export:
   - [A]ll formats.
   - [D]ocument.
   - [S]preadsheet.
   - [P]resentation.
   
3. TODO: Select files directories to export. Only directories containing the selected origin formats are list.

4. TODO: Options:
   - Keep originals? Yes/No.
   
## Future Functionality
- Allow parameter from console call to allow automation. 
- Be able to manage Organization/Shared Drives and Shared Files.
- Add support for other cloud drives. Dropbox, et. al.
- Support additional original formats:
  - Drawings.
- Support additional export formats:
  - Documents: PDF.
  - Spreadsheet: CSV, PDF.
  - Drawings: PNG, SVG, JPEG, PDF.
  - Presentations: PDF.
  
## Reference
- [Google Workspace and Drive MIME Types](https://developers.google.com/drive/api/v3/mime-types)
- [Google Workspace documents and export MIME types](https://developers.google.com/drive/api/v3/ref-export-formats)
- [About Shared Drives](https://developers.google.com/drive/api/v3/about-shareddrives)
- [Drive Files](https://developers.google.com/drive/api/v3/reference/files)


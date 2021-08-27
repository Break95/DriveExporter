# Drive Exporter
CLI utility to export GoogleDoc Drive files into OpenDocument format.

## Supported formats:
    
- Document
- Spreadsheet
- Presentation

## Application Flow 

1. Select Origin:
   - My Drive 
   - My Drive + Shared With Me
  
2. Select file types to export:
   - [A]ll formats.
   - [D]ocument
   - [S]preadsheet
   - [P]resentation
   
3. Select root directory/directories.
   
4. Options:
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

### Drive API v3
Google Workspace documents and export types:

- https://developers.google.com/drive/api/v3/ref-export-formats

Shared Drives: 

- https://developers.google.com/drive/api/v3/shared-drives-diffs
- https://developers.google.com/drive/api/v3/about-shareddrives
- https://developers.google.com/drive/api/v3/resource-keys


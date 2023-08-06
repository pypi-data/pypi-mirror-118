import io
import os.path
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from .auth import Auth
# from auth import Auth

class Transfer:
    def upload_file(self, file_path, dest_folder = None):
        creds = Auth().verify_token()

        if creds:
            service = build('drive', 'v3', credentials=creds)

            folder_id = None
            file_metadata = None
            file_name = os.path.basename(file_path)

            file_src = Path(file_path)
            if file_src.is_dir():
                raise ValueError('you can only upload a file.')
            if not file_src.is_file():
                raise ValueError('file is not exist.')

            if dest_folder:
                folder_metadata = {
                    'name': dest_folder,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder_result = service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder_result.get('id')

                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
            else:
                file_metadata = {
                    'name': file_name
                }                

            # upload file
            media = MediaFileUpload(file_path, resumable=True)
            file_result = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('%s(%s) is uploaded.' % (file_name, file_result))

        else:
            print('verification failed. please login.')

    def download_file(self, file_id):
        creds = Auth().verify_token()
        
        file_dict = {}
        count = 0

        if creds:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            result = service.files().get(fileId=file_id).execute()

            # add file information to dictionary
            file_dict[0] = {}
            file_dict[0]['id'] = result['id']
            file_dict[0]['name'] = result['name']
            file_dict[0]['mimeType'] = result['mimeType']
            file_dict[0]['path'] = '.'
            count = count + 1

            curr_file = 0
            while curr_file < count:
                print(file_dict[curr_file])

                if file_dict[curr_file]['mimeType'] == 'application/vnd.google-apps.folder':
                    items = self.get_files_from_folder(service, file_dict[curr_file]['id'])
                    folder_name = file_dict[curr_file]['name']
                    folder_path = file_dict[curr_file]['path'] 
                    child_path = f'{folder_path}/{folder_name}'

                    for item in items:
                        file_dict[count] = {}
                        file_dict[count]['id'] = item['id']
                        file_dict[count]['name'] = item['name']
                        file_dict[count]['mimeType'] = item['mimeType']
                        file_dict[count]['path'] = child_path
                        count = count + 1

                    # create folder with current name
                    # Path(child_path).mkdir(parents=True, exist_ok=True)
                    Path(child_path).mkdir(parents=False, exist_ok=True)
                    
                else:
                    file_name = file_dict[curr_file]['name']
                    file_id = file_dict[curr_file]['id']
                    file_path = file_dict[curr_file]['path']
                    
                    request = service.files().get_media(fileId=file_id)
                    fh = io.FileIO(f'{file_path}/{file_name}', 'wb')

                    downloader = MediaIoBaseDownload(fh, request)
                    done = False

                    print(f'download {file_name}')
                    while done is False:
                        status, done = downloader.next_chunk()
                        print('download %d%%.' % int(status.progress() * 100))
                
                curr_file = curr_file + 1
        else:
            print('verification failed. please login.')
        
    def get_files_from_folder(self, service, folder_id):
        results = service.files().list(
            q=f'\'{folder_id}\' in parents', pageSize=10, fields='nextPageToken, files(id, name, mimeType)').execute()

        items = results.get('files', [])
        return items
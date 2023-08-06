from googleapiclient.discovery import build
from .auth import Auth
# from auth import Auth

class Search:
    def list_all_files(self):
        creds = Auth().verify_token()

        if creds:
            service = build('drive', 'v3', credentials=creds)

            results = service.files().list(
                q='trashed = false', pageSize=10, fields='nextPageToken, files(id, name)').execute()
            items = results.get('files', [])

            if not items:
                print('no files found.')
            else:
                for item in items:
                    print(u'{0} ({1})'.format(item['name'], item['id']))
        else:
            print('verification failed. please login.')

    def search_keyword(self, keyword):
        creds = Auth().verify_token()

        if creds:
            service = build('drive', 'v3', credentials=creds)

            results = service.files().list(
                q=f'name contains \'{keyword}\' and trashed = false', pageSize=10, fields='nextPageToken, files(id, name)').execute()
            items = results.get('files', [])

            if not items:
                print('no files found.')
            else:
                for item in items:
                    print(u'{0} ({1})'.format(item['name'], item['id']))
        else:
            print('verification failed. please login.')

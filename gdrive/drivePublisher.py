from apiclient import discovery
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

class Gpublisher():
	def __init__(self):
		scope = 'https://www.googleapis.com/auth/drive'
		store = file.Storage('gdrive/storage.json')
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets('gdrive/credentials.json', scope)
			credentials = tools.run_flow(flow, store)
		self.gdrive = discovery.build('drive', 'v3', http=credentials.authorize(Http()))

	def upload(self, imagePath, folderID='16gFypOom7AEcIwuH50Bnt2TjLWx1JZPE'):
		fileMetadata = {
			'name': [imagePath],
			'parents': [folderID]
		}
		media = MediaFileUpload(imagePath,
								mimetype='image/jpeg',
								resumable=True)
		file = self.gdrive.files().create(body=fileMetadata,
											media_body=media,
											fields='id').execute()
		return file.get('id')

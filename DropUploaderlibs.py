#DropUploaderlibs.py

# Include the Dropbox SDK
# you have to install the Dropbox SDK first go to: https://www.dropbox.com/developers/core/sdks/python and install first

import dropbox
import ConfigParser, argparse
import sys, getopt

# Reading conffile DropUploader.conf
def connect(conffile):

	conffilePath = conffile
	config = ConfigParser.RawConfigParser()
	config.read(conffilePath)
	app_key = config.get('main', 'app_key')
	app_secret = config.get('main', 'app_secret')
	access_token = config.get('main', 'access_token')

	# Checking for API values
	if app_key == '' or app_secret == '':
		print 'Please add app_key and app_secret values in ' + conffilePath
		exit(-1)

	if access_token == '':
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		# Have the user sign in and authorize this token
		authorize_url = flow.start()
		print '1. Go to: ' + authorize_url
		print '2. Click "Allow" (you might have to log in first)'
		print '3. Copy the authorization code.'
		code = raw_input("Enter the authorization code here: ").strip()

		# This will fail if the user enters an invalid authorization code
		try:
			access_token, user_id = flow.finish(code)
		except:
			print 'Something is Wrong, you may enter an incorrect code'
			exit (1)

		# Let's write the access_token to the conffile
		config.set('main', 'access_token', access_token)
		with open(conffilePath, 'wb') as conffile:
			config.write(conffile)

	client = dropbox.client.DropboxClient(access_token)
	return client
	


#function that shows the content of a directory
def list(path, client):

	try:
		folder_metadata = client.metadata(path)
	except:
		print 'The Directory does not exist'
		sys.exit(-1)

	print folder_metadata['is_dir']
	if folder_metadata['is_dir'] == "False":
		print 'This is not a Directory'
		sys.exit(1)

	for I in folder_metadata['contents']:
		if I['is_dir'] == True:
			item_type = 'Dir'
		else:
			item_type = 'File'

		print item_type, I['size'], I['modified'], I['path']


#function to upload a list of files
def uploadFile(filelist, path, client):
	for localFile in filelist:
		remoteFile = path +'/'+ localFile
		try:
			fd = open(localFile, 'rb')
		except:
			print 'An error occur when try to open the local File'
			print 'Ommiting...'
		
		try:
			response = client.put_file(remoteFile, fd)
			
		except:
			print 'An error occur when try to upload the File'
			print 'Ommiting...'
			print response

		#print 'The  file %{localFile} was successfull uploaded to the remote Directory %{path}, %{response['size']} has been transfered' 


# Function to delete a list of files
def deleteFile(filelist, path, client):
	for remoteFile in filelist:
		try:
			fullPath = path+'/'+remoteFile	
			client.file_delete(fullPath)
		except:
			print 'An error occurs while deleting the file'
			print 'Ommiting...'

# Function to Download a list of files
def downloadFile (filelist, path, client):
	for remoteFile in filelist:
		try:
			out = open(remoteFile, 'wb')
			with client.get_file(path+'/'+remoteFile) as f:
				out.write(f.read())
		except:
			print 'An Error occcurs when try do download the Remote File'

# Function to Copy a file
def copyFile(args, client):
	try:
		client.file_copy(args[0], args[1])
	except:
		print 'An error occurs when try do copy the file'

# Function to Move a file
def moveFile(args, client):
	try:
		client.file_move(args[0], args[1])
	except:
		print 'An error occurs when try do copy the file'
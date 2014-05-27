'''
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    copyright Miguel Angel Barajas Hernandez A.K.A. GnuOwned <migbarajas@gmail.com>
'''





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
def list(path):
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
def uploadFile(filelist, path):
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
def deleteFile(filelist, path):
	for remoteFile in filelist:
		try:
			fullPath = path+'/'+remoteFile	
			client.file_delete(fullPath)
		except:
			print 'An error occurs while deleting the file'
			print 'Ommiting...'

# Function to Download a list of files
def downloadFile (filelist, path):
	for remoteFile in filelist:
		try:
			out = open(remoteFile, 'wb')
			with client.get_file(path+'/'+remoteFile) as f:
				out.write(f.read())
		except:
			print 'An Error occcurs when try do download the Remote File'

# Let parse the command line arguments
argparser =argparse.ArgumentParser()

argparser.add_argument("-a", "--account", help ="Show linked account", action = "store_true" )
argparser.add_argument("-l", "--list", help = "List de Directory content", action = "store_true")
argparser.add_argument("-p", "--path", help = "Path of the Directory", default = "/")
argparser.add_argument("-u", "--upload", help = "List of Files to upload to Dropbox", default = '', nargs = '*')
argparser.add_argument("-e", "--erase", help = "List of Files to delete from Dropbox", default = '', nargs = '*')
argparser.add_argument("-d", "--download", help = "List of Files to download from Dropbox", default = '', nargs = '*')
argparser.add_argument("-c", "--conffile", help = "List of Files to download from Dropbox", default = 'DropUploader.conf', )



args = argparser.parse_args()

client = connect(args.conffile)

if args.list == True:
	list(args.path)
if args.account == True:
	account = client.account_info()
	print 'linked account: ', account['display_name']
	print 'email: ', account['email']
if args.upload != '':
	uploadFile(args.upload, args.path)
if args.erase != '':
	deleteFile(args.erase, args.path)
if args.download != '':
	downloadFile(args.download, args.path)


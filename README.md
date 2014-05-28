With this little python script, you can download, upload, delete, copy, etc files from/to Dropbox
without using your username and password.

This is a early, early, early, early release, expect broken things.


Miguel Barajas A.K.A. GnuOwned <migbarajas@gmail.com>

CONFIGURATION PROCESS
----------------------

0. Make sure you have Dropbox Python SDK go to https://www.dropbox.com/developers/core/sdks/python for help
1. Add a new APP to you account:
	a. Go to https://www.dropbox.com/developers/apps
	b. Clic on "Create App"
	c. Select "Dropbox API App"
	d. Select "Files and Datastores"
	e. Select "NO"
	f. Select "All file types"
	g. Type a App Name (wharever you like)
2. Now you have an Dropbox App Created, now let's configure DropUploaderpy
	a. Copy and paste the App Key in the DropUploader.conf file
	b. Copy and paste the App Secret in the DropUploader.conf file
	c. Save the file
3. Run DropUploader.py and follow the instructions
4. Have a lot of fun

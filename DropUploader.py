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

from DropUploaderlibs import *


# Let parse the command line arguments
argparser = argparse.ArgumentParser()

argparser.add_argument("-a", "--account", help ="Show linked account", action = "store_true" )
argparser.add_argument("-l", "--list", help = "List de Directory content", action = "store_true")
argparser.add_argument("-p", "--path", help = "Path of the Directory", default = "/")
argparser.add_argument("-u", "--upload", help = "List of Files to upload to Dropbox", default = '', nargs = '*')
argparser.add_argument("-e", "--erase", help = "List of Files to delete from Dropbox", default = '', nargs = '*')
argparser.add_argument("-d", "--download", help = "List of Files to download from Dropbox", default = '', nargs = '*')
argparser.add_argument("-C", "--conffile", help = "Configuration File", default = 'DropUploader.conf', )
argparser.add_argument("-c", "--copy", help = "Copy a File to a new Location", default = '', nargs = '*')
argparser.add_argument("-m", "--move", help = "Move a File to a new Location", default = '', nargs = '*')


args = argparser.parse_args()


# Lets connect to Dropbox
client = connect(args.conffile)

#Lets evaluate the arguments and take actions 
if args.list == True:
	list(args.path, client)
if args.account == True:
	account = client.account_info()
	print 'linked account: ', account['display_name']
	print 'email: ', account['email']
if args.upload != '':
	uploadFile(args.upload, args.path, client)
if args.erase != '':
	deleteFile(args.erase, args.path, client)
if args.download != '':
	downloadFile(args.download, args.path, client)
if args.copy != '':
	copyFile(args.copy, client)
if args.move != '':
	moveFile(args.move, client)

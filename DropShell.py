from DropUploaderlibs import *

argparser = argparse.ArgumentParser()
argparser.add_argument("-C", "--conffile", help = "Configuration File", default = 'DropUploader.conf' )
args = argparser.parse_args()


# Lets connect to Dropbox
client = connect(args.conffile)

print 'Type help for help ;)'
while True:
	command = raw_input('dropshell>')
	cmd = command.split()[0]
	if cmd == 'ls':
		if command.split()[1] == '':
			path = '/'
		else:
			path = command.split()[1]

		list(path,client)

	else:
		print 'Command not implemented yet...'




#!/usr/bin/env python

import os,sys,re

def get_files(dir,filetypes):
	tmp = os.listdir(dir)
	retfiles = []
	for x in tmp:
		for y in filetypes:
			if re.search(y+'$',x,re.IGNORECASE):
				if os.path.isfile(dir+'/'+x):
					retfiles.append(x)
	return retfiles

parameters = {}
validoptions = ['-d','-r','-e','-t']
if len(sys.argv) == 2:
	if sys.argv[1] == '--help':
		print """Available options:
	-d <dir>: Convert files in <dir>. Default is current working dir.
	-t jpeg,jpg: Types of files to convert (case insensative). Default is jpeg,jpg. 
	-e <path of convert binary>: Absolute path of convert binary from ImageMagik package. Default /usr/local/bin/convert
	-r <resize>: Resize to new size. Default is 640x480.
		"""
		print """Note:
	<resize> directory is created in <dir> and all files are stored in that."""
		sys.exit(0)
	else:
		print "Invalid parameter passed. Try '--help'."
		sys.exit(1)
if not len(sys.argv)%2:
	print "invalid number of parameters"
	sys.exit(1)

for x in range(1,len(sys.argv),2):
	if not sys.argv[x].startswith('-'):
		print "Invalid option passed:",sys.argv[x]
		sys.exit(1)
	parameters[sys.argv[x]] = sys.argv[x+1]

for x in parameters.keys():
	if x not in validoptions:
		print x,"is not valid option"
		sys.exit(1)

if '-d' not in parameters.keys():
	parameters['-d'] = os.getcwd()
if '-r' not in parameters.keys():
	parameters['-r'] = '640x480'
if '-e' not in parameters.keys():
	parameters['-e'] = '/usr/local/bin/convert'
if '-t' not in parameters.keys():
	parameters['-t'] = 'jpeg,jpg';

if not os.path.isfile(parameters['-e']):
	print parameters['-e'],"is not a valid file or it does not exits"
	sys.exit(1)
if not os.path.isdir(parameters['-d']):
	print parameters['-d'],"does not exists"
	sys.exit(1)

if len(parameters['-r'].split('x')) != 2:
	print parameters['-r'],"is not valid. Enter XxY where X,Y are numeric"
	sys.exit(1)

resize = {}
resize['x'],resize['y'] = parameters['-r'].split('x')

for x in resize.keys():
	if not re.search('^\d+$',resize[x]):
		print resize[x],"is not a numeric value"
		sys.exit(1)
	
if not os.path.isdir(parameters['-d']+'/'+parameters['-r']):
	try:
		os.mkdir(parameters['-d']+'/'+parameters['-r'])
	except:
		print "Error creating dir",parameters['-d']+'/'+parameters['-r']
		sys.exit(1)

files = get_files(parameters['-d'],parameters['-t'].split(','))

if not len(files):
	print "Cannot find any files for resizing."
	sys.exit(2)

for x in files:
	(stdin,stdout,stderr) = os.popen3(parameters['-e']+" -resize "+parameters['-r']+' "'+parameters['-d']+'/'+x+'" "'+parameters['-d']+'/'+parameters['-r']+'/'+x+'"')
	y = stderr.read()
	if y:
		print y
	else:
		print "Successfully converted",parameters['-d']+'/'+x 


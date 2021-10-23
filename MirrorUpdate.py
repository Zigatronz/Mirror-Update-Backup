
# Import dependencies
from genericpath import exists
import os, argparse, shutil, progressbar

def RemoveTopDir(path:str, top:str):
	return path[top.__len__():]

# Argument
parser = argparse.ArgumentParser(description='Backup a folder to a another folder by using mirror update method.')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Target folder')
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Destination folder')
parser.add_argument('-p', '--progress', action='store_true', default=False, help='Show progress rather then verbose')
args = parser.parse_args()

TargetFolder = args.input
DestinationFolder = args.output
UseProgressBar = args.progress

# Handle In-Out
if not os.path.exists(TargetFolder):
	print("Target folder does not exist!")
	exit(1)

if not os.path.exists(DestinationFolder):
	try:
		os.mkdir(DestinationFolder)
	except:
		print("Something went wrong while creating destination folder.")
		exit(2)

# Initialize Progress Bar
if UseProgressBar:
	ProgressRange = 0
	CurrentProgress = 0
	for dirPath, dirNames, Filenames in os.walk(TargetFolder):
		for filename in Filenames:
			ProgressRange += 1
	widgets = [' [', progressbar.Timer(format= 'elapsed : %(elapsed)s'), '] ',
				progressbar.Bar('*'),
				" " ,progressbar.Percentage(),
				' (', progressbar.ETA(), ') ']
	ProgBar = progressbar.ProgressBar(max_value=ProgressRange, widgets=widgets).start()

# Start Backup : Target folder ==> Destination folder
for dirPath, dirNames, Filenames in os.walk(TargetFolder):
	if not Filenames:
		if not exists(DestinationFolder + RemoveTopDir(dirPath, TargetFolder)):
			if not UseProgressBar:
				print("Create Dir : " + DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
			os.mkdir(DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
	for filename in Filenames:
		if UseProgressBar:
			CurrentProgress += 1
			ProgBar.update(CurrentProgress)
		if not exists(DestinationFolder + RemoveTopDir(dirPath, TargetFolder)):
			os.mkdir(DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
		if not os.path.exists(DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder)):
			if not UseProgressBar:
				print("Add        : " + DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
			shutil.copy2(dirPath + "\\" + filename, DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
		elif os.path.getmtime(dirPath + "\\" + filename) != os.path.getmtime(DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder)):
			if not UseProgressBar:
				print("Update     : " + DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
			os.remove(DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
			shutil.copy2(dirPath + "\\" + filename, DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
		elif os.path.getsize(dirPath + "\\" + filename) != os.path.getsize(DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder)):
			if not UseProgressBar:
				print("Replace    : " + DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
			os.remove(DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))
			shutil.copy2(dirPath + "\\" + filename, DestinationFolder + RemoveTopDir(dirPath + "\\" + filename, TargetFolder))

# Delete Non Exist Subdir Files/Folders : Destination folder != Target folder : Del(Destination folder)
#remove files first
for dirPath, dirNames, Filenames in os.walk(DestinationFolder):
	for filename in Filenames:
		if not os.path.exists(TargetFolder + RemoveTopDir(dirPath + "\\" + filename, DestinationFolder)):
			if not UseProgressBar:
				print("Remove File: " + dirPath + "\\" + filename)
			os.remove(dirPath + "\\" + filename)
#remove folders
for dirPath, dirNames, Filenames in os.walk(DestinationFolder):
	if not Filenames:
		if not exists(TargetFolder + RemoveTopDir(dirPath, DestinationFolder)):
			if not UseProgressBar:
				print("Remove Dir : " + dirPath)
			os.rmdir(dirPath)

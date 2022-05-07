
# Import dependencies
import os, argparse, shutil, progressbar

def RemoveTopDir(path:str, top:str):
	return path[top.__len__():]

# Argument
parser = argparse.ArgumentParser(description='Backup a folder to an another folder by using mirror update method.')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Target folder')
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Destination folder')
parser.add_argument('-p', '--progress', action='store_true', default=False, help='Show progress rather then verbose')
parser.add_argument('-nm', '--nomodify', action='store_true', default=False, help='Do not compare for file modification date')
parser.add_argument('-ns', '--nosize', action='store_true', default=False, help='Do not compare for file size')
parser.add_argument('-nd', '--nodelete', action='store_true', default=False, help='Do not delete files and folders that ONLY exist on the destination')
parser.add_argument('-nf', '--nofail', action='store_true', default=False, help='Ignore fail and keep the thing running')
args = parser.parse_args()

TargetFolder = args.input
DestinationFolder = args.output
UseProgressBar = args.progress
NoCModify = args.nomodify
NoCSize = args.nosize
NoDelete = args.nodelete
NoFail = args.nofail

# Handle In-Out
if not NoFail:
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
		if not os.path.exists(DestinationFolder + RemoveTopDir(dirPath, TargetFolder)):
			if not UseProgressBar:
				print("Create Dir : " + DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
			try:
				os.mkdir(DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
			except:
				print("FAILED to Create Dir : " + DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
				if not NoFail:
					exit()
	for filename in Filenames:
		if UseProgressBar:
			CurrentProgress += 1
			ProgBar.update(CurrentProgress)
		if not os.path.exists(DestinationFolder + RemoveTopDir(dirPath, TargetFolder)):
			os.mkdir(DestinationFolder + RemoveTopDir(dirPath, TargetFolder))
		if not os.path.exists(DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder)):
			if not UseProgressBar:
				print("Add        : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			try:
				shutil.copy2(os.path.join(dirPath, filename), DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			except:
				print("FAILED to Add        : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
				if not NoFail:
					exit()
		elif os.path.getmtime(os.path.join(dirPath, filename)) != os.path.getmtime(DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder)) and not NoCModify:
			if not UseProgressBar:
				print("Update     : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			try:
				os.remove(DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
				shutil.copy2(os.path.join(dirPath, filename), DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			except:
				print("FAILED to Update     : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
				if not NoFail:
					exit()
		elif os.path.getsize(os.path.join(dirPath, filename)) != os.path.getsize(DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder)) and not NoCSize:
			if not UseProgressBar:
				print("Replace    : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			try:
				os.remove(DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
				shutil.copy2(os.path.join(dirPath, filename), DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
			except:
				print("FAILED to Replace    : " + DestinationFolder + RemoveTopDir(os.path.join(dirPath, filename), TargetFolder))
				if not NoFail:
					exit()

# Delete Non Exist Subdir Files/Folders : Destination folder != Target folder : Del(Destination folder)
if not NoDelete:
	for dirPath, dirNames, Filenames in os.walk(DestinationFolder):
		for filename in Filenames:
			if not os.path.exists(TargetFolder + RemoveTopDir(os.path.join(dirPath, filename), DestinationFolder)):
				if os.path.exists(os.path.join(dirPath, filename)):
					if not UseProgressBar:
						print("Remove File: " + os.path.join(dirPath, filename))
					os.remove(os.path.join(dirPath, filename))
		if not Filenames:
			if not os.path.exists(TargetFolder + RemoveTopDir(dirPath, DestinationFolder)):
				if os.path.exists(dirPath):
					if not UseProgressBar:
						print("Remove Dir : " + dirPath)
					try:
						shutil.rmtree(dirPath)
					except:
						print("FAILED to Remove Dir : " + dirPath)
						if not NoFail:
							exit()

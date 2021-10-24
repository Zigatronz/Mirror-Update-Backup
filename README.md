# Mirror Update Backup
Backup a folder to an another folder by using mirror update method.

# How to use
## Install requirement
    pip install -r requirements.txt
## Using argument
      -h, --help       show this help message and exit.
      -i, --input      Target folder.
      -o, --output     Destination folder.
      -p, --progress   Show progress rather then verbose.
      -nm, --nomodify  Do not compare for file modification date.
      -ns, --nosize    Do not compare for file size.
      -nd, --nodelete  Do not delete files and folders that ONLY exist on the destination.
### For example :
      MirrorUpdate.py -i "Folder to backup" -o "Backup folder"
      MirrorUpdate.py -i "Folder to backup" -o "Backup folder" -p
      MirrorUpdate.py -i "Folder to backup" -o "Backup folder" -p -nm
      MirrorUpdate.py --input "Folder to backup" --output "Backup folder" --progress
# How it's work
1. **Copy/Replace** all **target files and folders** to **destination folder** as the destination folder **does not have it** or **got deference in terms of size or modification date**.
2. Delete all files and folders that **ONLY** available on **destination folder**.
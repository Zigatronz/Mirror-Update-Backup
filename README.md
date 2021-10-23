# Mirror Update Backup
Backup a folder to an another folder by using mirror update method.

# How to use
## Install requirement
    pip install -r requirements.txt
## Using argument
      -h, --help      show this help message and exit.
      -i, --input     Target folder.
      -o, --output    Destination folder.
      -p, --progress  Show progress rather then verbose.
### For example :
      MirrorUpdate.py -i "Folder to backup" -o "Backup folder"
      MirrorUpdate.py -i "Folder to backup" -o "Backup folder" -p
      MirrorUpdate.py --input "Folder to backup" --output "Backup folder"
      MirrorUpdate.py --input "Folder to backup" --output "Backup folder" --progress
# How it's work
1. **Copy/Replace** all **target files and folders** to **destination folder** as the destination folder **does not have it** or **got deference in terms of size or modification date**.
2. Delete all files and folders that **ONLY** available on **destination folder**.
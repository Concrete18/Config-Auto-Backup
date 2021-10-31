# Misc. File Backup

This script allows you to set many files or folders to be backed up when run this program. The backups are kept with dated folders with a set number of previous backups kept in case of corruption.
Backups only occur if the current file/folder has a different hash compared to the last backup.

## Features

* Backs up all files/folders set in the config.
* Uses hashing to check if it should backup an entry or not.
* Keeps the last 3(configurable) backups to be sure that you can restore to your last working version.
* Hash checks allow you to backup anytime you want to backup a file without worrying about have 3 identical redundant backups for other entries.

## config example

```json
{
    "settings":
        {
            "backup_destination":"Backup Folder",
            "backup_redundancy":3,
            "backup_only":true
        },
    "backup_targets":
        {
            "Git_Config":"C:/Users/Michael/.gitconfig",
            "Bash_Config":"C:/Users/Michael/.bashrc",
            "Bash_Profile":"C:/Users/Michael/.bash_profile",
            "TriggerCMD":"C:/AHKScripts"
        }
}
```

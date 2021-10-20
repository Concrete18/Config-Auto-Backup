# Misc. File Backup

This script allows you to set many files or folders to be backed up when run. The backups are kept with dated folders with a set number of previous backups kept in case of corruption.

## config example

```json
{
    "settings":
        {
            "backup_destination":"Backup Folder",
            "backup_redundancy":3
        },
    "backup_targets":
        {
            "Git_Config":"C:/Users/Michael/.gitconfig",
            "Bash_Config":"C:/Users/Michael/.bashrc",
            "Bash_Profile":"C:/Users/Michael/.bash_profile",
            "TriggerCMD":"C:/AHKScripts",
            "Windows_Terminal":"C:/Users/Michael/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json"
        }
}

```

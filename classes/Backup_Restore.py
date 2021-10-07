import datetime as dt
import shutil
import json
import sys
import os
import hashlib
from checksumdir import dirhash


class Backup_Restore:

    config_path = 'config.json'
    with open('config.json') as json_file:
        data = json.load(json_file)
    backup_location = data['settings']['backup_destination']
    backup_redundancy = data['settings']['backup_redundancy']
    backup_targets = data['backup_targets']


    def check(self):
        '''
        Checks for any paths that do not exists and sets up the found_paths list.
        '''
        self.found_paths = {}
        missing_entries = []
        for target, path in self.backup_targets.items():
            if os.path.exists(path):
                self.found_paths[target] = path
            else:
                missing_entries.append(target)
        return missing_entries


    def delete_oldest(self):
        '''
        Deletest the oldest backups so only the newest specified in backup_redundancy is left.
        '''
        backup_list = []
        for file in os.scandir(self.backup_location):
            backup_list.append(file.path)
        if len(backup_list) <= self.backup_redundancy:
            print(f'{self.backup_redundancy} or Less Backups.')
            return
        else:
            print(f'More than {self.backup_redundancy} backups.\nDeleting oldest backups now.')
            sorted_list = sorted(backup_list, key=os.path.getctime, reverse=True)
            for i in range(self.backup_redundancy, len(backup_list)):
                shutil.rmtree(sorted_list[i])
    

    def open_config(self):
        '''
        Opens the config file for editing.
        '''
        os.startfile(self.config_path)

    
    def hash_file(self, file):
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()


    def hash_check(self, dir_file1, dir_file2):
        '''
        Checks the hash of the two directories or files to see if they are the different.
        '''
        if os.path.isdir(dir_file1):
            hash1 = dirhash(dir_file1, 'md5')
            hash2 = dirhash(dir_file2, 'md5')
        else:
            hash1 = self.hash_file(dir_file1)
            hash2 = self.hash_file(dir_file2)
        return hash1 == hash2


    def Backup(self):
        '''
        Runs a back up of all files and folders from the config.json that exist and have been changed.
        '''
        current_time = dt.datetime.now().strftime("Date %m-%d-%y Time %H-%M-%S")
        for target, path in self.found_paths.items():
            if self.hash_check(path, path):
                continue
            backup_path = os.path.join(self.backup_location, target, current_time)
            full_path = os.path.join(self.backup_location, backup_path)
            last_backup = sorted(os.path.join(self.backup_location, target), key=os.path.getctime, reverse=True)[0]
            os.mkdir(full_path)
            final_dest = os.path.join(base_folder, os.path.basename(path))
            if not os.path.isdir(final_dest):
                os.mkdir(base_folder)
            if os.path.isfile(path):
                shutil.copy(path, final_dest)
            else:
                shutil.copytree(path, final_dest)
            print(f'Backed Up: {target} from {path}')
            print()


    def Restore(self):
        '''
        Asks what you want to restore then restores it to its set location.
        '''
        print('Restore Function Incomplete')

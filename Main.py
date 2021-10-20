import shutil, os, json, hashlib
from checksumdir import dirhash
import datetime as dt


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
        print('\nChecking for missing target paths.')
        self.found_paths = {}
        missing_entries = []
        for target, path in self.backup_targets.items():
            if os.path.exists(path):
                self.found_paths[target] = path
            else:
                missing_entries.append(target)
        if len(missing_entries) > 0:
            print('Missing entries found:\n', ", ".join(missing_entries))


    def delete_oldest(self, folder, debug=False):
        '''
        Deletest the oldest backups so only the newest specified in backup_redundancy is left.
        '''
        backup_list = []
        for file in os.scandir(folder):
            backup_list.append(file.path)
        if len(backup_list) > self.backup_redundancy:
            if debug:
                print(f'More than {self.backup_redundancy} backups.\nDeleting oldest backups now.')
            sorted_list = sorted(backup_list, key=os.path.getctime, reverse=True)
            for i in range(self.backup_redundancy, len(backup_list)):
                shutil.rmtree(sorted_list[i])
        else:
            if debug:
                print(f'{self.backup_redundancy} or Less Backups.')
    

    def open_config(self):
        '''
        Opens the config file for editing.
        '''
        os.startfile(self.config_path)

    
    def hash_file(self, file):
        '''
        ph
        '''
        BUF_SIZE = 65536
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
        try:
            if os.path.isdir(dir_file1):
                hash1 = dirhash(dir_file1, 'md5')
                hash2 = dirhash(dir_file2, 'md5')
            else:
                hash1 = self.hash_file(dir_file1)
                hash2 = self.hash_file(dir_file2)
            return hash1 == hash2
        except PermissionError:
            print(f'Hash Check failed for {dir_file1}')
            return True


    def add(self):
        '''
        ph
        '''
        print('WIP Feature')


    def backup(self, check_hash=False):
        '''
        Runs a back up of all files and folders from the config.json that exist and have been changed.
        '''
        # creates backup folder if it does not exist
        if not os.path.isdir(self.backup_location):
            os.mkdir(self.backup_location)
        for target, path in self.found_paths.items():
            # gets last backup location and checks its hash with the current path hash
            if len(os.listdir(self.backup_location)) > 0 and check_hash:
                backup_list = []
                backups = os.scandir(os.path.join(self.backup_location, target))
                for file in backups:
                    backup_list.append(file.path)
                last_backup = sorted(backup_list, key=os.path.getctime, reverse=True)[0]
                if self.hash_check(path, last_backup):
                    continue
            # copies to backup folder
            current_time = dt.datetime.now().strftime("Date %m-%d-%y Time %H-%M-%S")
            dest = os.path.join(self.backup_location, target, current_time)
            if os.path.isfile(path):
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                shutil.copy(path, dest)
            else:
                shutil.copytree(path, dest)
            backup_path = os.path.join(self.backup_location, target)
            self.delete_oldest(backup_path)
            print(f'\nBacked Up: {target} from {path}')


    def restore(self):
        '''
        Asks what you want to restore then restores it to its set location.
        '''
        print('Restore Function Incomplete')


class Main:

    App = Backup_Restore()


    def run(self):
        '''
        ph
        '''
        try:
            print('Multi Backup System')
            self.App.check()
            # response = input('\n\nWhat would you like to do?\n1. Backup\n2. Restore\n')
            response = '1'
            if response == '1':
                self.App.backup()
            elif response == '2':
                self.App.restore()
            elif response == '3':
                # TODO add new file
                self.App.add()
            else:
                print('Unknown Response')
                input()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    Main().run()

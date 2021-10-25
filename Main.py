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
            print(f'Missing entries found:\n{", ".join(missing_entries)}')

    def delete_oldest(self, folder, debug=False):
        '''
        Deletest the oldest backups so only the newest specified in backup_redundancy is left.
        '''
        backup_list = [file.path for file in os.scandir(folder)]
        total_backups = len(backup_list)
        if total_backups > self.backup_redundancy:
            if debug:
                print(f'More than {self.backup_redundancy} backups.\nDeleting oldest backups now.')
            sorted_list = sorted(backup_list, key=os.path.getctime, reverse=True)
            for i in range(self.backup_redundancy, total_backups):
                shutil.rmtree(sorted_list[i])
        elif debug:
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

    def get_hash(self, dir_file):
        '''
        Gets hash of the given file or folder..
        '''
        if os.path.isdir(dir_file):
            return dirhash(dir_file, 'md5')
        else:
            return self.hash_file(dir_file)

    def add(self):
        '''
        ph
        '''
        print('WIP Feature')

    def backup(self, check_hash=True):
        '''
        Runs a back up of all files and folders from the config.json that exist and have been changed.
        '''
        # creates backup folder if it does not exist
        if not os.path.isdir(self.backup_location):
            os.mkdir(self.backup_location)
        for target, path in self.found_paths.items():
            current_hash = self.get_hash(path)
            # gets last backup location and checks its hash with the current path hash
            if os.path.isdir(os.path.join(self.backup_location, target)) and check_hash:
                backups = os.scandir(os.path.join(self.backup_location, target))
                backup_list = [file.path for file in backups]
                last_backup = sorted(backup_list, key=os.path.getctime, reverse=True)[0]
                # TODO check if sorting works even if the hash is different for each.
                print(backup_list)
                print(last_backup)
                previous_hash = last_backup.split(' ')[-1]
                if current_hash == previous_hash:
                    print(f'\nSkipping {target} due to no changes since last backup.')
                    continue
            # copies to backup folder
            current_time = dt.datetime.now().strftime("Date %m-%d-%y Time %H-%M-%S")
            dest = os.path.join(self.backup_location, target, f'{current_time} {current_hash}')
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
                input('Unknown Response')
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    Main().run()

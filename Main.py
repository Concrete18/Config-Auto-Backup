import shutil, os, subprocess, json, hashlib, time, math
from checksumdir import dirhash
import datetime as dt
import time


class ConfigClass:
    '''
    Config load and creation class.
    '''


    def load(self):
        self.config_path = 'config.json'
        if os.path.exists(os.path.join(os.getcwd(), self.config_path)):
            with open(self.config_path) as json_file:
                self.data = json.load(json_file)
            backup_location = self.data['settings']['backup_destination']
            backup_redundancy = self.data['settings']['backup_redundancy']
            backup_only = self.data['settings']['backup_only']
            backup_entries = self.data['backup_entries']
            return backup_location, backup_redundancy, backup_only, backup_entries
        else:
            data = {
                "settings":
                    {
                        "backup_destination": "Backup Folder",
                        "backup_redundancy": 3,
                        "backup_only": True
                    },
                "backup_entries":
                    {
                        "Example_Path": "README.md",
                    }
            }
            self.save_to_json(data)
            subprocess.Popen(["notepad.exe", self.config_path])
            input('Set up your config save.\nPress Enter when finished.\n')
            backup_location = data['settings']['backup_destination']
            backup_redundancy = data['settings']['backup_redundancy']
            backup_only = data['settings']['backup_only']
            backup_entries = data['backup_entries']
            return backup_location, backup_redundancy, backup_only, backup_entries
    
    def save_to_json(self, data):
        '''
        Saves data into json format with the given filename.
        '''
        json_object = json.dumps(data, indent = 4)
        with open(self.config_path, "w") as outfile:
            outfile.write(json_object)
    
    def add_entry(self, entry_name, entry_path):
        '''
        Adds a new entry to the config with the given `entry_name` and `entry_path`.
        '''
        self.data['backup_entries'][entry_name] = entry_path
        self.save_to_json(self.data)
        print(f'\nAdded {entry_name} to the config with the following path.\n{entry_path}')

    def open(self):
        '''
        Opens the config file for editing.
        '''
        os.startfile(self.config_path)


class FileClass:
    '''
    File Access Class
    '''

    def __init__(self, backup_location, backup_redundancy, backup_only, backup_entries) -> None:
        self.backup_location = backup_location
        self.backup_redundancy = backup_redundancy
        self.backup_only = backup_only
        self.backup_entries = backup_entries


    def log_return(func):
        '''
        Prints `func` name and its return.
        '''
        def wrapped(*args, **kwargs):
            print(f'Running {func.__name__}')
            value = func(*args, **kwargs)
            print(f'Return Value: {value}')
            return value
        return wrapped

    def benchmark(func):
        '''
        Prints `func` name and its benchmark time.
        '''
        def wrapped(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = round(end-start, 2)
            print(f'{func.__name__} Completion Time: {elapsed}')
            return value
        return wrapped

    def path_check(self):
        '''
        Checks for any paths that do not exists and sets up the found_paths list.
        '''
        print('\nChecking for missing target paths:')
        self.found_paths = {}
        missing_entries = []
        for target, path in self.backup_entries.items():
            if os.path.exists(path):
                self.found_paths[target] = path
            else:
                missing_entries.append(target)
        if len(missing_entries) > 0:
            print(f'Missing entries found:\n{", ".join(missing_entries)}')
        else:
            print('All entries found.')

    @staticmethod
    def convert_size(directory):
        '''
        Converts size of `directory` to best fitting unit of measure.
        '''
        total_size = 0
        for path, dirs, files in os.walk(directory):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
        if total_size > 0:
            size_name = ("B", "KB", "MB", "GB", "TB")
            try:
                i = int(math.floor(math.log(total_size, 1024)))
                p = math.pow(1024, i)
                s = round(total_size / p, 2)
                return f'{s} {size_name[i]}'
            except ValueError:
                return '0 bits'
        else:
            return '0 bits'

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

    def hash_file(self, file_path):
        '''
        Creates a hash for the given `file_path`.
        '''
        BUF_SIZE = 65536
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
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

    # @benchmark
    def backup(self, check_hash=True):
        '''
        Runs a back up of all files and folders from the config.json that exist and have been changed.
        '''
        # creates backup folder if it does not exist
        if not os.path.isdir(self.backup_location):
            os.mkdir(self.backup_location)
        skipped = []
        backed_up = []
        for target, path in self.found_paths.items():
            current_hash = self.get_hash(path)
            # gets last backup location and checks its hash with the current path hash
            if os.path.isdir(os.path.join(self.backup_location, target)) and check_hash:
                backups = os.scandir(os.path.join(self.backup_location, target))
                backup_list = [file.path for file in backups]
                last_backup = sorted(backup_list, key=os.path.getctime, reverse=True)[0]
                previous_hash = last_backup.split(' ')[-1]
                if current_hash == previous_hash:
                    skipped.append(target)
                    continue
            # copies to backup folder
            current_time = dt.datetime.now().strftime("Date %m-%d-%y Time %H-%M-%S")
            dest = os.path.join(self.backup_location, target, f'{current_time} Hash {current_hash}')
            if len(backed_up) == 0:
                print('Backing up files.')
            if os.path.isfile(path):
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                shutil.copy(path, dest)
            else:
                shutil.copytree(path, dest)
            backed_up.append(target)
            backup_path = os.path.join(self.backup_location, target)
            self.delete_oldest(backup_path)
        if len(backed_up) > 0:
            print(f'\nBacked up:\n{", ".join(backed_up)}')
        if len(skipped) > 0:
            print(f'\nNo changes since last back up:\n{", ".join(skipped)}')

    def restore(self):
        '''
        Asks what you want to restore then restores it to its set location.
        '''
        # TODO finish restore
        print('\nWhat do you want to restore?\nType the number for the backup.')
        backups = [f'{index}: {entry}' for index, entry in enumerate(self.backup_entries.keys())]
        input("\n".join(backups))


def run():
    '''
    Runs the entire program.
    '''
    try:
        title = 'Multi Backup System'
        # loads config
        Config = ConfigClass()
        backup_location, backup_redundancy, backup_only, backup_entries = Config.load()
        # sets up file object
        File = FileClass(backup_location, backup_redundancy, backup_only, backup_entries)
        print(title)
        print(f'Size of Backup: {File.convert_size(File.backup_location)}')
        File.path_check()
        if File.backup_only:
            response = 1
        else:
            response = int(input('\n\nWhat would you like to do?\n1. Backup\n2. Restore\n3. Add\n4. Open Config\n') or 1)
        if response == 1:
            File.backup()
        elif response == 2:
            File.restore()
        elif response == 3:
            name = input('\nWhat is the name of your new file/folder you want to backup?')
            path = input('\nWhat is the path that will be backed up?')
            Config.add_entry(name, path)
            print('If you want to add more at one time, edit the config file directly.')
        elif response == 4:
            Config.open()
        else:
            input('Unknown Response')
        print(f'\nFinished running {title}')
    except KeyboardInterrupt:
        exit()
    response = input('\nType 1 to Open Backup Folder\nPress Enter to Close\n')
    if response == '1':
        subprocess.Popen(f'explorer "{File.backup_location}"')


if __name__ == '__main__':
    run()

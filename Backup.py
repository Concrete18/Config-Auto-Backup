from tkinter import messagebox, filedialog
import shutil
import json
import datetime as dt
import os

class Backup_App:

    def __init__(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
        self.backup_location = data['settings']['backup_destination']
        self.backup_redundancy = data['settings']['backup_redundancy']
        self.backup_targets = data['backup_targets']


    def Delete_Oldest(self):
        '''Deletest the oldest backups so only the the newest specified in backup_redundancy is left.'''
        backup_list = []
        dir = self.backup_location
        for file in os.listdir(dir):
            file = os.path.join(dir, file)
            backup_list.append(file)
        if len(backup_list) < 4:
            print(f'{self.backup_redundancy} or Less Backups.')
            return
        else:
            print(f'More then {self.backup_redundancy} backups.\nDeleting oldest now.')
            sorted_list = sorted(backup_list, key=os.path.getctime, reverse=True)
            for i in range(self.backup_redundancy, len(backup_list)):
                shutil.rmtree(sorted_list[i])


    def Backup(self):
        '''Backups up the entered folder.'''
        current_time = dt.datetime.now().strftime("%d-%m-%y %H-%M")
        dest = os.path.join(self.backup_location, current_time)
        for item, loc in self.backup_targets.items():
            final_dest = os.path.join(dest, item)
            # try:
            if os.path.isfile(loc):
                print(loc)
                shutil.copy(loc, final_dest)
            else:
                shutil.copytree(loc, final_dest)
            print(f'Backed Up: {item} from {loc}')
            # except FileNotFoundError:
            #     print('No Action Completed - File location does not exist.')
            # except FileExistsError:
            #     print('No Action Completed - Save Already Backed up.')
            print()


    def Restore(self):
        '''Asks what you want to restore then restores it to is set location.'''
        pass


if __name__ == '__main__':
    Configs = Backup_App()
    # input('Would you like to backup your files?')
    Configs.Backup()
    Configs.Delete_Oldest()

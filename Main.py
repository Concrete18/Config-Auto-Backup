from Backup import Backup_App

Configs = Backup_App()

response = input('Multi Backup System\n\nWhat would you like to do?\n1. Backup\n2. Restore\n')
if response == '1':
    Configs.Backup()
    Configs.Delete_Oldest()
elif response == '2':
    Configs.Restore()
else:
    print('Unknown Response')
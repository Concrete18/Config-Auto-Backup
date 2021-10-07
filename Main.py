from classes.Backup_Restore import Backup_Restore

class Main:

    App = Backup_Restore()


    def run(self):
        '''
        ph
        '''
        try:
            print('Multi Backup System')
            # prints missing backup targets
            print('\nChecking for missing target paths.')
            missing_entries = ", ".join(self.App.check())
            print(missing_entries)
            response = input('\n\nWhat would you like to do?\n1. Backup\n2. Restore\n')
            if response == '1':
                self.App.Backup()
                self.App.Delete_Oldest()
            elif response == '2':
                self.App.Restore()
            else:
                print('Unknown Response')
                input()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    Main().run()

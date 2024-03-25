from setup import *
from PySide6.QtCore import QProcess, QProcessEnvironment
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

# Message
print('Migration Assistant needs to run as root.')
# Request users password
sub.run(['sudo', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE)
# sub.run(['pkexec', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE)
# Clear terminal
sub.run(['clear'], stdout=sub.PIPE, stderr=sub.PIPE)
# Open Migration Assistant
sub.run(['python3', SRC_MIGRATION_ASSISTANT_PY], stdout=sub.PIPE, stderr=sub.PIPE)

# class CallMigrationTool(QWidget):
#     def __init__(self):
#         super(CallMigrationTool, self).__init__()

#         # Call for root
#         if not self.access_root():
#             print('Exiting...')
#             sys.exit()
#         else:
#             # Ask for user's password
#             #command = ['pkexec', 'python3']
#             #auth_process = sub.run(command, stdout=sub.PIPE, stderr=sub.PIPE, input=b'password_here'.decode(), text=True, check=False)
#             directory_path = str(SRC_MIGRATION_ASSISTANT_PY.split('/')[:-1])
#             directory_path = '/home/macbook/.local/share/timemachine/src'
#             #print(os.path.join(directory_path))
#             #exit()

#             auth_process = sub.run(['pkexec', 'python3', SRC_MIGRATION_ASSISTANT_PY], stdout=sub.PIPE, stderr=sub.PIPE, text=True, check=False, cwd=directory_path)

#             print("stdout:", auth_process.stdout)
#             print("stderr:", auth_process.stderr)

#     def access_root(self):
#         reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to execute the command?', QMessageBox.Yes | QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             return True
#         else:
#             return False

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     MAIN = CallMigrationTool()
#     MAIN.show()
#     sys.exit(app.exec())

## Message
#print('Migration Assistant needs to run as root.')

## Request user's password and execute the script with pkexec
#auth_process = sub.run(['pkexec', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE)

## Print stdout and stderr of the authentication process for debugging
#print("stdout:", auth_process.stdout.decode())
#print("stderr:", auth_process.stderr.decode())
#print("stderr:", type(auth_process.stderr.decode()))

#if 'Error' in auth_process.stderr.decode():
    #print('ø***')
## Clear terminal
#sub.run(['clear'], stdout=sub.PIPE, stderr=sub.PIPE)
## Open Migration Assistant
#sub.run(['python3', SRC_MIGRATION_ASSISTANT_PY], stdout=sub.PIPE, stderr=sub.PIPE)

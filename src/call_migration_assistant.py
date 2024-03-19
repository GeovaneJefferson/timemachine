from setup import *

# Message
print('Migration Assistant needs to run as root.')
# Request users password
sub.run(['sudo', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE)
# sub.run(['pkexec', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE)
# Clear terminal
sub.run(['clear'], stdout=sub.PIPE, stderr=sub.PIPE)
# Open Migration Assistant
sub.run(['python3', SRC_MIGRATION_ASSISTANT_PY], stdout=sub.PIPE, stderr=sub.PIPE)

#from setup import *


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

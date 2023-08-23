from setup import *

# sub.run(['sudo', 'python3', *sys.argv])
# Message
print('Migration Assistant needs to run as root.')
# Request users password
sub.run(['sudo', 'python3', *sys.argv])
# Clear terminal
sub.run(['clear'])
# Open Migration Assistant
sub.Popen(["python3", SRC_MIGRATION_ASSISTANT_PY])
 

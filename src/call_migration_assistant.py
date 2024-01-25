from setup import *

# Message
print('Migration Assistant needs to run as root.')
# Request users password
sub.run(['sudo', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE).wait()
# sub.run(['pkexec', 'python3', *sys.argv], stdout=sub.PIPE, stderr=sub.PIPE).wait()
# Clear terminal
sub.run(['clear'], stdout=sub.PIPE, stderr=sub.PIPE).wait()
# Open Migration Assistant
sub.run(['python3', SRC_MIGRATION_ASSISTANT_PY], stdout=sub.PIPE, stderr=sub.PIPE).wait()
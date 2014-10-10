import subprocess

def execute_cask_command(command=None):
    cmd = 'search'
    if command == 'list':
        cmd = 'list'
    elif command == 'alfred':
        cmd = 'alfred status'

    result, _ = subprocess.Popen('export PATH=/usr/local/bin:$PATH && /usr/local/bin/brew cask %s' %
                                cmd, shell=True, stdout=subprocess.PIPE).communicate()
    return result
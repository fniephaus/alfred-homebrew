import os
from workflow import Workflow, PasswordNotFound


def get_all_casks():
    return os.popen('/usr/local/bin/brew cask search').readlines()[1:]


def get_installed_casks():
    return os.popen('/usr/local/bin/brew cask list').readlines()


def get_alfred_status():
    return os.popen('/usr/local/bin/brew cask alfred status').readlines()[0].split('\n')[0]

if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('cask_all', get_all_casks())
    wf.cache_data('cask_installed', get_installed_casks())
    wf.cache_data('cask_alfred_status', get_alfred_status())

    print get_installed_casks()
import os
from workflow import Workflow, PasswordNotFound


def get_all_packages():
    return os.popen('/usr/local/bin/brew search').readlines()


def get_installed_packages():
    return os.popen('/usr/local/bin/brew list --versions').readlines()


def get_info():
    return os.popen('/usr/local/bin/brew info').readlines()[0]

if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('brew_all', get_all_packages())
    wf.cache_data('brew_installed', get_installed_packages())
    wf.cache_data('brew_info', get_info())

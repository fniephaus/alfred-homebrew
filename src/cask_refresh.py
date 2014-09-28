import subprocess
from workflow import Workflow, PasswordNotFound


def get_all_casks():
    cmd, err = subprocess.Popen(
        ['/usr/local/bin/brew', 'cask', 'search'], stdout=subprocess.PIPE).communicate()
    return cmd.splitlines()[1:]


def get_installed_casks():
    cmd, err = subprocess.Popen(
        ['/usr/local/bin/brew', 'cask', 'list'], stdout=subprocess.PIPE).communicate()
    return cmd.splitlines()


if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('cask_all', get_all_casks())
    wf.cache_data('cask_installed', get_installed_casks())

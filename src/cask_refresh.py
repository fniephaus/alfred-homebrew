import subprocess

from workflow import Workflow, PasswordNotFound


def get_all_casks():
    result = execute_cask_command('search')
    return result.splitlines()[1:]


def get_installed_casks():
    result = execute_cask_command('list')
    return result.splitlines()


def execute_cask_command(command=None):
    if command not in ['search', 'list', 'alfred status']:
        return None

    # workaround PATH problems
    result, err = subprocess.Popen('export PATH=/usr/local/bin:$PATH && /usr/local/bin/brew cask %s' %
                                   command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if err != '':
        return err

    return result


if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('cask_all_casks', get_all_casks())
    wf.cache_data('cask_installed_casks', get_installed_casks())

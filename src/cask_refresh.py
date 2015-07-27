import os
import subprocess

from workflow import Workflow, PasswordNotFound

WF = Workflow()


def get_all_casks():
    result = execute_cask_command('search')
    return result.splitlines()[1:]


def get_installed_casks():
    result = execute_cask_command('list')
    return result.splitlines()


def execute_cask_command(command):
    if command not in ['search', 'list', 'alfred status']:
        return None

    # workaround PATH and Caskroom problems
    os.environ['PATH'] += os.pathsep + '/usr/local/bin'

    opts = WF.settings.get('HOMEBREW_CASK_OPTS', None)

    options = ''
    if opts:
        if all(k in opts for k in ('appdir', 'caskroom')):
            options = '--appdir=%s --caskroom=%s' % (opts['appdir'], opts['caskroom'])
        else:
            err = 'Config'

    result, err = subprocess.Popen(
        '/usr/local/bin/brew cask %s %s' % (options, command), shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if 'sudo' in result:
        err = 'Config'

    if err != '':
        return err

    return result


if __name__ == '__main__':
    WF.cache_data('cask_all_casks', get_all_casks())
    WF.cache_data('cask_installed_casks', get_installed_casks())

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
    commands = ['export PATH=/usr/local/bin:$PATH']

    opts = WF.settings.get('HOMEBREW_CASK_OPTS', None)

    if opts:
        if all(k in opts for k in ('appdir', 'caskroom')):
            cmd = 'export HOMEBREW_CASK_OPTS="--appdir=%s --caskroom=%s"' % (opts['appdir'], opts['caskroom'])
            commands.append(cmd)
        else:
            err = 'Config'

    commands.append('/usr/local/bin/brew cask %s' % command)

    result, err = subprocess.Popen(
        ' && '.join(commands), shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if not opts and 'sudo' in result:
        err = 'Config'

    if err != '':
        return err

    return result


if __name__ == '__main__':
    WF.cache_data('cask_all_casks', get_all_casks())
    WF.cache_data('cask_installed_casks', get_installed_casks())

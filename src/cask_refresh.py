from workflow import Workflow, PasswordNotFound

from cask_helpers import execute_cask_command


def get_all_casks():
    result = execute_cask_command()
    return result.splitlines()[1:]


def get_installed_casks():
    result = execute_cask_command('list')
    return result.splitlines()


if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('cask_all', get_all_casks())
    wf.cache_data('cask_installed', get_installed_casks())

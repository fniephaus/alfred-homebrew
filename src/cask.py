import sys
import os
import subprocess

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background
import cask_refresh

ACTIONS = [
    {
        'name': 'install',
        'description': 'Install new casks',
        'autocomplete': 'install ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'uninstall',
        'description': 'Uninstall casks',
        'autocomplete': 'uninstall ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'search',
        'description': 'Search casks',
        'autocomplete': 'search ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'list',
        'description': 'List installed casks',
        'autocomplete': 'list ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'update',
        'description': 'Update brew casks',
        'autocomplete': '',
        'arg': 'brew cask update',
        'valid':  True
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew cask doctor',
        'valid':  True
    },
    {
        'name': 'home',
        'description': 'Open the homepage of a cask',
        'autocomplete': 'home',
        'arg': '',
        'valid': False
    },
    {
        'name': 'clear',
        'description': 'Clear workflow cache',
        'autocomplete': 'workflow:delcache',
        'arg': '',
        'valid': False
    },
    {
        'name': 'alfred',
        'description': 'Modify Alfred\'s scope to include the Caskroom',
        'autocomplete': 'alfred',
        'arg': '',
        'valid': False
    }
]


def search_key_for_action(action):
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)


def complete(wf):
    global ACTIONS

    if wf.update_available:
        subtitle = 'New: %s' % wf.update_info['body']
        wf.add_item("An update is available!", subtitle,
                    autocomplete='workflow:update', valid=False)

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query and query.startswith('install'):
        filter_all_casks(query)
    elif query and query.startswith('uninstall'):
        filter_installed_casks(query)
    elif query and query.startswith('list'):
        filter_installed_casks(query)
    elif query and query.startswith('search'):
        filter_all_casks(query)
    elif query and query.startswith('alfred'):
        info, _ = subprocess.Popen('export PATH=/usr/local/bin:$PATH && /usr/local/bin/brew cask alfred status', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
        wf.add_item(info)
        if 'not linked' in info:
            wf.add_item('Add Caskroom to alfred search paths', arg='brew cask alfred link', valid=True)
        else:
            wf.add_item('Remove Caskroom from Alfred search paths', arg='brew cask alfred unlink', valid=True)
    else:
        if query:
            ACTIONS = wf.filter(
                query, ACTIONS, key=search_key_for_action, match_on=MATCH_SUBSTRING)

        for action in ACTIONS:
                wf.add_item(action['name'], action['description'], uid=action[
                            'name'], autocomplete=action['autocomplete'], arg=action['arg'], valid=action['valid'])

    wf.send_feedback()

    cmd = ['/usr/bin/python', wf.workflowfile('cask_refresh.py')]
    run_in_background('cask_refresh', cmd)


def filter_all_casks(query):
    formulas = wf.cached_data('cask_all', max_age=0)
    query_filter = query.split()
    if len(query_filter) > 1:
        formulas = wf.filter(query_filter[1],
                             formulas, match_on=MATCH_SUBSTRING)

    for formula in formulas:
        formula = formula.rsplit()
        name = formula[0]

        if query.startswith('install'):
            wf.add_item(
                name, "Install", arg='brew cask install %s' %
                name, valid=True)
        else:
            wf.add_item(name, "Open homepage", arg='brew cask home %s' %
                        name, valid=True)


def filter_installed_casks(query):
    formulas = wf.cached_data('cask_installed', cask_refresh.get_installed_casks, max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        formulas = wf.filter(query_filter[1],
                             formulas, match_on=MATCH_SUBSTRING)

    for formula in formulas:
        if query.startswith('uninstall'):
            wf.add_item(formula, "Uninstall", arg='brew cask uninstall %s' %
                        name, valid=True)
        else:
            wf.add_item(
                formula, "Open homepage", arg='brew cask home %s' % formula, valid=True)


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'fniephaus/alfred-homebrew',
        'version': 'v1.1',
    })
    sys.exit(wf.run(complete))

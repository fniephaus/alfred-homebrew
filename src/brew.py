import sys
import os
from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background
import brew_refresh

FORMULA_URL = 'https://github.com/Homebrew/homebrew/tree/master/Library/Formula'

ACTIONS = [
    {
        'name': 'install',
        'description': 'Install new packages',
        'autocomplete': 'install ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'uninstall',
        'description': 'Uninstall packages',
        'autocomplete': 'uninstall ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'search',
        'description': 'Search packages',
        'autocomplete': 'search ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'list',
        'description': 'List installed packages',
        'autocomplete': 'list ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'update',
        'description': 'Update brew packages',
        'autocomplete': '',
        'arg': 'brew update',
        'valid':  True
    },
    {
        'name': 'upgrade',
        'description': 'Upgrade brew packages',
        'autocomplete': '',
        'arg': 'brew upgrade',
        'valid':  True
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew doctor',
        'valid':  True
    },
    {
        'name': 'info',
        'description': 'Show info',
        'autocomplete': 'info',
        'arg': '',
        'valid': False
    },
    {
        'name': 'clear',
        'description': 'Clear workflow cache',
        'autocomplete': 'workflow:delcache',
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
        wf.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query and query.startswith('install'):
        filter_all_packages(query)
    elif query and query.startswith('uninstall'):
        filter_installed_packages(query)
    elif query and query.startswith('list'):
        filter_installed_packages(query)
    elif query and query.startswith('search'):
        filter_all_packages(query)
    elif query and query.startswith('info'):
        info = wf.cached_data('brew_info', max_age=3600)
        if not info:
            info = brew_refresh.get_info()
        wf.add_item(info, autocomplete='')
    else:
        if query:
            ACTIONS = wf.filter(
                query, ACTIONS, key=search_key_for_action, match_on=MATCH_SUBSTRING)

        for action in ACTIONS:
                wf.add_item(action['name'], action['description'], uid=action[
                            'name'], autocomplete=action['autocomplete'], arg=action['arg'], valid=action['valid'])

    wf.send_feedback()
    refresh_cache(wf)


def filter_all_packages(query):
    formulas = wf.cached_data('brew_all', max_age=3600)
    if not formulas:
        formulas = brew_refresh.get_all_packages()

    query_filter = query.split()
    if len(query_filter) > 1:
        formulas = wf.filter(query_filter[1],
                             formulas, match_on=MATCH_SUBSTRING)

    for formula in formulas:
        if query.startswith('install'):
            wf.add_item(formula, "Install", arg='brew install %s' %
                        formula, valid=True)
        else:
            wf.add_item(formula, "Open on GitHub", arg='open %s/%s.rb' %
                        (FORMULA_URL, formula), valid=True)


def filter_installed_packages(query):
    formulas = wf.cached_data('brew_installed', max_age=3600)
    if not formulas:
        formulas = brew_refresh.get_installed_packages()

    query_filter = query.split()
    if len(query_filter) > 1:
        formulas = wf.filter(query_filter[1],
                             formulas, match_on=MATCH_SUBSTRING)

    for formula in formulas:
        name = formula.split(' ')[0]
        if query.startswith('uninstall'):
            wf.add_item(formula, "Uninstall", arg='brew uninstall %s' %
                        name, valid=True)
        else:
            wf.add_item(
                formula, "Open on GitHub", arg='open %s/%s.rb' % (FORMULA_URL, name), valid=True)


def refresh_cache(wf):
    cmd = ['/usr/bin/python', wf.workflowfile('brew_refresh.py')]
    run_in_background('brew_refresh', cmd)

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'fniephaus/alfred-homebrew',
        'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
    })
    sys.exit(wf.run(complete))

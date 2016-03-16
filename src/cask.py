#!/usr/bin/python
# encoding: utf-8

import os
import subprocess

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

import cask_actions
import cask_refresh
import helpers as h

WF = Workflow(update_settings={
    'github_slug': 'fniephaus/alfred-homebrew',
    'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
})

DEFAULT_SETTINGS = {
    'HOMEBREW_CASK_OPTS': {
        'appdir': '/Applications',
        'caskroom': '/usr/local/Caskroom'
    }
}

OPEN_HELP = 'open https://github.com/fniephaus/alfred-homebrew && exit'


def edit_settings():
    # Create default settings if they not exist
    if (not os.path.exists(WF.settings_path) or
            not WF.settings.get('HOMEBREW_CASK_OPTS', None)):
        for key in DEFAULT_SETTINGS:
            WF.settings[key] = DEFAULT_SETTINGS[key]
    # Edit settings
    subprocess.call(['open', WF.settings_path])


def get_all_casks(query):
    formulas = WF.cached_data('cask_all_casks', cask_refresh.get_all_casks,
                              max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_installed_casks(query):
    formulas = WF.cached_data(
        'cask_installed_casks', cask_refresh.get_installed_casks, max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def cask_not_installed():
    return cask_refresh.execute_cask_command('search').startswith('Error')


def cask_not_configured():
    return cask_refresh.execute_cask_command('search').startswith('Config')


if __name__ == '__main__':
    if WF.update_available:
        WF.add_item('An update is available!',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=h.get_icon(WF, 'cloud-download'))

    if WF.cached_data('cask_not_installed', cask_not_installed, max_age=0):
        WF.add_item('Cask does not seem to be installed!',
                    'Hit enter to see what you need to do...',
                    arg='open http://caskroom.io/ && exit',
                    valid=True,
                    icon='cask.png')
        WF.add_item('I trust this workflow',
                    'Hit enter to install cask...',
                    arg='brew install caskroom/cask/brew-cask',
                    valid=True,
                    icon='cask.png')
        # delete cached file
        WF.cache_data('cask_not_installed', None)
    elif WF.cached_data('cask_not_configured', cask_not_configured, max_age=0):
        WF.add_item('Cask does not seem to be properly configured!',
                    'Hit enter to see what you need to do...',
                    arg=OPEN_HELP,
                    valid=True,
                    icon='cask.png')

        config = next(a for a in cask_actions.ACTIONS if a.name == 'config')
        WF.add_item(config['name'], config['description'],
                    uid=config['name'],
                    autocomplete=config['autocomplete'],
                    arg=config['arg'],
                    valid=config['valid'],
                    icon=h.get_icon(WF, 'chevron-right'))

        query = WF.args[0] if len(WF.args) else None
        if query and query.startswith('config'):
            edit_settings()

        # delete cached file
        WF.cache_data('cask_not_configured', None)
    else:
        # extract query
        query = WF.args[0] if len(WF.args) else None

        if query and query.startswith('install'):
            for formula in get_all_casks(query):
                WF.add_item(formula, 'Install cask',
                            arg='brew cask install %s' % formula,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and any(query.startswith(x) for x in ['search', 'home']):
            for formula in get_all_casks(query):
                WF.add_item(formula, 'Open homepage',
                            arg='brew cask home %s' % formula,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('uninstall'):
            for formula in get_installed_casks(query):
                name = formula.split(' ')[0]
                WF.add_item(formula, 'Uninstall cask',
                            arg='brew cask uninstall %s' % name,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('list'):
            for formula in get_installed_casks(query):
                WF.add_item(formula, 'Open homepage',
                            arg='brew cask home %s' % formula,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('alfred'):
            info = cask_refresh.execute_cask_command('alfred status')
            for text in info.splitlines():
                WF.add_item(text, icon=h.get_icon(WF, 'info'))
            if 'linked' in info:  # make sure it's not an error
                if 'not linked' in info:
                    WF.add_item('Add Caskroom to alfred search paths',
                                arg='brew cask alfred link',
                                valid=True,
                                icon=h.get_icon(WF, 'chevron-right'))
                else:
                    WF.add_item('Remove Caskroom from Alfred search paths',
                                arg='brew cask alfred unlink',
                                valid=True,
                                icon=h.get_icon(WF, 'chevron-right'))
        elif query and query.startswith('config'):
            edit_settings()
        else:
            actions = cask_actions.ACTIONS
            # filter actions by query
            if query:
                actions = WF.filter(query, actions,
                                    key=h.search_key_for_action,
                                    match_on=MATCH_SUBSTRING)

            if len(actions) > 0:
                for action in actions:
                    WF.add_item(action['name'], action['description'],
                                uid=action['name'],
                                autocomplete=action['autocomplete'],
                                arg=action['arg'],
                                valid=action['valid'],
                                icon=h.get_icon(WF, 'chevron-right'))
            else:
                WF.add_item('No action found for "%s"' % query,
                            autocomplete='',
                            icon=h.get_icon(WF, 'info'))

        if len(WF._items) == 0:
            query_name = query[query.find(' ') + 1:]
            WF.add_item('No formula found for "%s"' % query_name,
                        autocomplete='%s ' % query[:query.find(' ')],
                        icon=h.get_icon(WF, 'info'))

    WF.send_feedback()

    # refresh cache
    cmd = ['/usr/bin/python', WF.workflowfile('cask_refresh.py')]
    run_in_background('cask_refresh', cmd)

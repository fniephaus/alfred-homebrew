#!/usr/bin/python
# encoding: utf-8

import sys
import os
import subprocess

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

import cask_refresh

WF = Workflow(update_settings={
    'github_slug': 'fniephaus/alfred-homebrew',
    'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
})


def search_key_for_action(action):
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)


def get_all_casks(query):
    formulas = WF.cached_data(
        'cask_all_casks', cask_refresh.get_all_casks, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_installed_casks(query):
    formulas = WF.cached_data(
        'cask_installed_casks', cask_refresh.get_installed_casks, max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


def cask_not_installed():
    return cask_refresh.execute_cask_command('search').startswith('Error')


if __name__ == '__main__':
    from cask_actions import ACTIONS

    if WF.update_available:
        WF.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False, icon='cask.png')

    if WF.cached_data('cask_not_installed', cask_not_installed, max_age=0):
        WF.add_item('Cask does not seem to be installed!',
                    'Hit enter to see what you need to do...', arg='open http://caskroom.io/ && exit', valid=True)
        WF.add_item('I trust this workflow',
                    'Hit enter to install cask...', arg='brew install caskroom/cask/brew-cask', valid=True)
        # delete cached file
        WF.cache_data('cask_not_installed', None)
    else:
        # extract query
        query = WF.args[0] if len(WF.args) else None

        if query and query.startswith('install'):
            for formula in get_all_casks(query):
                WF.add_item(
                    formula, "Install", arg='brew cask install %s' %
                    formula, valid=True, icon='cask.png')
        elif query and any(query.startswith(x) for x in ['search', 'home']):
            for formula in get_all_casks(query):
                WF.add_item(formula, "Open homepage", arg='brew cask home %s' %
                            formula, valid=True, icon='cask.png')
        elif query and query.startswith('uninstall'):
            for formula in get_installed_casks(query):
                name = formula.split(' ')[0]
                WF.add_item(formula, "Uninstall", arg='brew cask uninstall %s' %
                            name, valid=True, icon='cask.png')
        elif query and query.startswith('list'):
            for formula in get_installed_casks(query):
                WF.add_item(
                    formula, "Open homepage", arg='brew cask home %s' % formula, valid=True, icon='cask.png')
        elif query and query.startswith('alfred'):
            info = cask_refresh.execute_cask_command('alfred status')
            WF.add_item(info)
            if 'linked' in info:  # make sure it's not an error
                if 'not linked' in info:
                    WF.add_item('Add Caskroom to alfred search paths',
                                arg='brew cask alfred link', valid=True, icon='cask.png')
                else:
                    WF.add_item('Remove Caskroom from Alfred search paths',
                                arg='brew cask alfred unlink', valid=True, icon='cask.png')
        else:
            # filter actions by query
            if query:
                ACTIONS = WF.filter(
                    query, ACTIONS, key=search_key_for_action, match_on=MATCH_SUBSTRING)

            for action in ACTIONS:
                WF.add_item(action['name'], action['description'], uid=action[
                            'name'], autocomplete=action['autocomplete'], arg=action['arg'], valid=action['valid'], icon='cask.png')

    WF.send_feedback()

    # refresh cache
    cmd = ['/usr/bin/python', WF.workflowfile('cask_refresh.py')]
    run_in_background('cask_refresh', cmd)

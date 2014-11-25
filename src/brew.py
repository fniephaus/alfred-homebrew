#!/usr/bin/python
# encoding: utf-8

import sys
import os
import subprocess

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

import brew_refresh

WF = Workflow(update_settings={
    'github_slug': 'fniephaus/alfred-homebrew',
    'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
})

FORMULA_URL = 'https://github.com/Homebrew/homebrew/tree/master/Library/Formula'


# name and description are search keys
def search_key_for_action(action):
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)


def get_all_packages(query):
    formulas = WF.cached_data(
        'brew_all_formulas', brew_refresh.get_all_packages, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_installed_packages(query):
    formulas = WF.cached_data(
        'brew_installed_formulas', brew_refresh.get_installed_packages, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_open_link_command(formula):
    return 'open %s/%s.rb && exit' % (FORMULA_URL, name)


def brew_not_installed():
    _, err = subprocess.Popen(
        ['command', '/usr/local/bin/brew'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return err != ''


if __name__ == '__main__':
    from brew_actions import ACTIONS

    if WF.update_available:
        WF.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)

    if WF.cached_data('brew_not_installed', brew_not_installed, max_age=0):
        WF.add_item('Brew does not seem to be installed!',
                    'Hit enter to see what you need to do...', arg='open http://brew.sh/#install && exit', valid=True)
        WF.add_item('I trust this workflow',
                    'Hit enter to install brew...', arg='ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', valid=True)
        # delete cached file
        WF.cache_data('brew_not_installed', None)
    else:
        # extract query
        query = WF.args[0] if len(WF.args) else None

        if query and query.startswith('install'):
            for formula in get_all_packages(query):
                WF.add_item(formula, "Install", arg='brew install %s' %
                            formula, valid=True)
        elif query and query.startswith('search'):
            for formula in get_all_packages(query):
                WF.add_item(
                    formula, "Open on GitHub", arg=get_open_link_command(formula), valid=True)
        elif query and query.startswith('uninstall'):
            for formula in get_installed_packages(query):
                name = formula.rsplit()[0]
                WF.logger.debug(formula)
                WF.logger.debug(name)
                WF.add_item(formula, "Uninstall", arg='brew uninstall %s' %
                            name, valid=True)
        elif query and query.startswith('list'):
            for formula in get_installed_packages(query):
                name = formula.rsplit()[0]
                WF.add_item(
                    formula, "Open on GitHub", arg=get_open_link_command(name), valid=True)
        elif query and query.startswith('info'):
            info = WF.cached_data(
                'brew_info', brew_refresh.get_info, max_age=3600)
            WF.add_item(info, autocomplete='')
        else:
            # filter actions by query
            if query:
                ACTIONS = WF.filter(
                    query, ACTIONS, key=search_key_for_action, match_on=MATCH_SUBSTRING)

            for action in ACTIONS:
                WF.add_item(action['name'], action['description'], uid=action[
                            'name'], autocomplete=action['autocomplete'], arg=action['arg'], valid=action['valid'])

    WF.send_feedback()

    # refresh cache
    cmd = ['/usr/bin/python', WF.workflowfile('brew_refresh.py')]
    run_in_background('brew_refresh', cmd)

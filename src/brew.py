#!/usr/bin/python
# encoding: utf-8

import sys
import os

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
    formulas = WF.cached_data('brew_all', brew_refresh.get_all_packages, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_installed_packages(query):
    formulas = WF.cached_data('brew_installed', brew_refresh.get_installed_packages, max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1],
                         formulas, match_on=MATCH_SUBSTRING)
    return formulas


if __name__ == '__main__':
    from brew_actions import ACTIONS

    if WF.update_available:
        WF.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)

    # extract query
    query = WF.args[0] if len(WF.args) else None

    if query and query.startswith('install'):
        for formula in get_all_packages(query):
            WF.add_item(formula, "Install", arg='brew install %s' %
                        formula, valid=True)
    elif query and query.startswith('search'):
        for formula in get_all_packages(query):
            WF.add_item(formula, "Open on GitHub", arg='open %s/%s.rb' %
                        (FORMULA_URL, formula), valid=True)
    elif query and query.startswith('uninstall'):
        for formula in get_install_packages(query):
            WF.add_item(formula, "Uninstall", arg='brew uninstall %s' %
                        name, valid=True)
        filter_installed_packages(query)
    elif query and query.startswith('list'):
        for formula in get_install_packages(query):
            WF.add_item(
                formula, "Open on GitHub", arg='open %s/%s.rb' % (FORMULA_URL, name), valid=True)
    elif query and query.startswith('info'):
        info = WF.cached_data('brew_info', brew_refresh.get_info, max_age=3600)
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

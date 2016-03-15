#!/usr/bin/python
# encoding: utf-8

import os

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

from brew_actions import ACTIONS
import brew_refresh
import helpers as h

WF = Workflow(update_settings={
    'github_slug': 'fniephaus/alfred-homebrew',
    'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
})

FORMULA_URL = 'https://github.com/Homebrew/homebrew/tree/master/Library/' \
              'Formula'
BREW_INSTALL_URL = 'https://raw.githubusercontent.com/Homebrew/install/' \
                   'master/install'


def get_all_packages(query):
    formulas = WF.cached_data('brew_all_formulas',
                              brew_refresh.get_all_packages,
                              max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_installed_packages(query):
    formulas = WF.cached_data('brew_installed_formulas',
                              brew_refresh.get_installed_packages,
                              max_age=3600)

    query_filter = query.split()
    if len(query_filter) > 1:
        return WF.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def get_open_link_command(formula):
    return 'open %s/%s.rb && exit' % (FORMULA_URL, formula)


def brew_installed():
    return os.path.isfile('/usr/local/bin/brew')


if __name__ == '__main__':
    if WF.update_available:
        WF.add_item('An update is available!',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=h.get_icon(WF, 'cloud-download'))

    if not brew_installed():
        WF.add_item('Brew does not seem to be installed!',
                    'Hit enter to see what you need to do...',
                    arg='open http://brew.sh/#install && exit',
                    valid=True)
        WF.add_item('I trust this workflow',
                    'Hit enter to install brew...',
                    arg='ruby -e "$(curl -fsSL %s)"' % BREW_INSTALL_URL,
                    valid=True)
    else:
        # extract query
        query = WF.args[0] if len(WF.args) else None

        if query and query.startswith('install'):
            for formula in get_all_packages(query):
                WF.add_item(formula, 'Install formula',
                            arg='brew install %s' % formula,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('search'):
            for formula in get_all_packages(query):
                WF.add_item(formula, 'Open formula on GitHub',
                            arg=get_open_link_command(formula),
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('uninstall'):
            for formula in get_installed_packages(query):
                name = formula.rsplit()[0]
                WF.add_item(formula, 'Uninstall formula',
                            arg='brew uninstall %s' % name,
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('list'):
            for formula in get_installed_packages(query):
                name = formula.rsplit()[0]
                WF.add_item(formula, 'Open formula on GitHub',
                            arg=get_open_link_command(name),
                            valid=True,
                            icon=h.get_icon(WF, 'package'))
        elif query and query.startswith('info'):
            info = WF.cached_data('brew_info', brew_refresh.get_info,
                                  max_age=3600)
            WF.add_item(info, autocomplete='', icon=h.get_icon(WF, 'info'))
        else:
            # filter actions by query
            if query:
                ACTIONS = WF.filter(query, ACTIONS,
                                    key=h.search_key_for_action,
                                    match_on=MATCH_SUBSTRING)

            if len(ACTIONS) > 0:
                for action in ACTIONS:
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
    cmd = ['/usr/bin/python', WF.workflowfile('brew_refresh.py')]
    run_in_background('brew_refresh', cmd)

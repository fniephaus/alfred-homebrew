#!/usr/bin/env python3
# encoding: utf-8

import os
import subprocess
import sys

import cask_actions
import helpers
from workflow import MATCH_SUBSTRING, Workflow
from workflow.background import run_in_background

GITHUB_SLUG = 'fniephaus/alfred-homebrew'
OPEN_HELP = 'open https://github.com/fniephaus/alfred-homebrew && exit'


def execute(wf, cmd_list):
    opts = wf.settings.get('HOMEBREW_CASK_OPTS', None)
    if opts:
        if all(k in opts for k in ('appdir')):
            cmd_list += ['--appdir=%s' % opts['appdir']]

    brew_arch = helpers.get_brew_arch(wf)

    new_env = helpers.initialise_path(brew_arch)
    result, err = subprocess.Popen(cmd_list,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   env=new_env).communicate()
    if err:
        return 'Error: %s' % str(err, 'utf-8')
    return str(result, 'utf-8')


def get_all_casks():
    return execute(wf, ['brew', 'casks']).splitlines()


def get_installed_casks():
    return execute(wf, ['brew', 'list', '--cask']).splitlines()


def get_outdated_casks():
    return execute(wf, ['brew', 'outdated', '--cask']).splitlines()


def filter_all_casks(wf, query):
    formulas = wf.cached_data('cask_all_casks',
                              get_all_casks,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def filter_installed_casks(wf, query):
    formulas = wf.cached_data('cask_installed_casks',
                              get_installed_casks,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def filter_outdated_casks(wf, query):
    formulas = wf.cached_data('cask_outdated_casks',
                              get_outdated_casks,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def main(wf):
    if wf.update_available:
        wf.add_item('An update is available!',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=helpers.get_icon(wf, 'cloud-download'))

    find_brew = helpers.brew_installed()

    if not (find_brew['INTEL'] or find_brew['ARM']):
        helpers.brew_installation_instructions(wf)
    else:
        # extract query
        query = wf.args[0] if len(wf.args) else None

        if (not query and
                len(wf.cached_data('cask_outdated_casks',
                                   get_outdated_casks,
                                   max_age=3600)) > 0):
            wf.add_item('Some of your casks are outdated!',
                        autocomplete='outdated ',
                        valid=False,
                        icon=helpers.get_icon(wf, 'cloud-download'))

        if query and query.startswith('install'):
            for formula in filter_all_casks(wf, query):
                wf.add_item(formula, 'Install cask',
                            arg='brew install --cask %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and any(query.startswith(x) for x in ['search', 'home']):
            for formula in filter_all_casks(wf, query):
                wf.add_item(formula, 'Open homepage',
                            arg='brew home %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('uninstall'):
            for formula in filter_installed_casks(wf, query):
                name = formula.split(' ')[0]
                item = wf.add_item(formula, 'Uninstall cask',
                                   arg='brew uninstall --cask %s' % name,
                                   valid=True,
                                   icon=helpers.get_icon(wf, 'package'))
                item.add_modifier('alt', 'Uninstall and zap cask',
                                  arg='brew uninstall --cask --zap %s' % name,
                                  valid=True,
                                  icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('list'):
            for formula in filter_installed_casks(wf, query):
                wf.add_item(formula, 'Open homepage',
                            arg='brew home %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('outdated'):
            for formula in filter_outdated_casks(wf, query):
                name = formula.split(' ')[0]
                wf.add_item(formula, 'Upgrade cask',
                            arg='brew upgrade --cask %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('config'):
            helpers.edit_settings(wf)
            wf.add_item('`settings.json` has been opened.',
                        autocomplete='',
                        icon=helpers.get_icon(wf, 'info'))
        else:
            actions = cask_actions.ACTIONS
            # filter actions by query
            if query:
                actions = wf.filter(query, actions,
                                    key=helpers.search_key_for_action,
                                    match_on=MATCH_SUBSTRING)

            if len(actions) > 0:
                for action in actions:
                    wf.add_item(action['name'], action['description'],
                                uid=action['name'],
                                autocomplete=action['autocomplete'],
                                arg=action['arg'],
                                valid=action['valid'],
                                icon=helpers.get_icon(wf, 'chevron-right'))
            else:
                wf.add_item('No action found for "%s"' % query,
                            autocomplete='',
                            icon=helpers.get_icon(wf, 'info'))

        if len(wf._items) == 0:
            query_name = query[query.find(' ') + 1:]
            wf.add_item('No formula found for "%s"' % query_name,
                        autocomplete='%s ' % query[:query.find(' ')],
                        icon=helpers.get_icon(wf, 'info'))

    wf.send_feedback()

    # refresh cache
    cmd = ['/usr/bin/env', 'python3', wf.workflowfile('cask_refresh.py')]
    run_in_background('cask_refresh', cmd)


if __name__ == '__main__':
    wf = Workflow(update_settings={'github_slug': GITHUB_SLUG})
    sys.exit(wf.run(main))

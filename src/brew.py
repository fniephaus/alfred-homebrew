# encoding: utf-8

import os
import subprocess
import sys

from workflow import Workflow, MATCH_SUBSTRING
from workflow.background import run_in_background

import brew_actions
import helpers


GITHUB_SLUG = 'fniephaus/alfred-homebrew'
FORMULA_URL = 'https://github.com/Homebrew/homebrew/tree/master/Library/' \
              'Formula'
BREW_INSTALL_URL = 'https://raw.githubusercontent.com/Homebrew/install/' \
                   'master/install'


def execute(cmd_list):
    new_env = os.environ.copy()
    new_env['PATH'] = '/usr/local/bin:%s' % new_env['PATH']
    cmd, err = subprocess.Popen(cmd_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=new_env).communicate()
    if err:
        return err
    return cmd


def get_all_packages(wf, query):
    return execute(['brew', 'search']).splitlines()


def get_installed_packages():
    return execute(['brew', 'list', '--versions']).splitlines()


def get_info():
    return execute(['brew', 'info'])


def get_open_link_command(formula):
    return 'open %s/%s.rb && exit' % (FORMULA_URL, formula)


def filter_all_packages(wf, query):
    formulas = wf.cached_data('brew_all_formulas',
                              get_all_packages,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def filter_installed_packages(wf, query):
    formulas = wf.cached_data('brew_installed_formulas',
                              get_installed_packages,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulas, match_on=MATCH_SUBSTRING)
    return formulas


def brew_installed():
    return os.path.isfile('/usr/local/bin/brew')


def main(wf):
    if wf.update_available:
        wf.add_item('An update is available!',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=helpers.get_icon(wf, 'cloud-download'))

    if not brew_installed():
        wf.add_item('Brew does not seem to be installed!',
                    'Hit enter to see what you need to do...',
                    arg='open http://brew.sh/#install && exit',
                    valid=True)
        wf.add_item('I trust this workflow',
                    'Hit enter to install brew...',
                    arg='ruby -e "$(curl -fsSL %s)"' % BREW_INSTALL_URL,
                    valid=True)
    else:
        # extract query
        query = wf.args[0] if len(wf.args) else None

        if query and query.startswith('install'):
            for formula in filter_all_packages(wf, query):
                wf.add_item(formula, 'Install formula',
                            arg='brew install %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('search'):
            for formula in filter_all_packages(wf, query):
                wf.add_item(formula, 'Open formula on GitHub',
                            arg=get_open_link_command(formula),
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('uninstall'):
            for formula in filter_installed_packages(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Uninstall formula',
                            arg='brew uninstall %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('list'):
            for formula in filter_installed_packages(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Open formula on GitHub',
                            arg=get_open_link_command(name),
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('info'):
            wf.add_item(get_info(),
                        autocomplete='',
                        icon=helpers.get_icon(wf, 'info'))
        else:
            actions = brew_actions.ACTIONS
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
    cmd = ['/usr/bin/python', wf.workflowfile('brew_refresh.py')]
    run_in_background('brew_refresh', cmd)


if __name__ == '__main__':
    wf = Workflow(update_settings={'github_slug': GITHUB_SLUG})
    sys.exit(wf.run(main))

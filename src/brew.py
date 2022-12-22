#!/usr/bin/env python3
# encoding: utf-8

import os
import subprocess
import sys

import brew_actions
import helpers
from workflow import MATCH_SUBSTRING, Workflow
from workflow.background import run_in_background

GITHUB_SLUG = 'fniephaus/alfred-homebrew'


def execute(wf, cmd_list):
    brew_arch = helpers.get_brew_arch(wf)
    new_env = helpers.initialise_path(brew_arch)
    result, err = subprocess.Popen(cmd_list,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=new_env).communicate()
    if err:
        return 'Error: %s' % str(err, 'utf-8')
    return str(result, 'utf-8')


def get_all_formulae():
    return execute(wf, ['brew', 'formulae']).splitlines()


def get_installed_formulae():
    return execute(wf, ['brew', 'list', '--versions']).splitlines()


def get_pinned_formulae():
    return execute(wf, ['brew', 'list', '--pinned', '--versions']).splitlines()


def get_outdated_formulae():
    return execute(wf, ['brew', 'outdated', '--formula']).splitlines()


def get_info():
    return execute(wf, ['brew', 'info'])


def get_commands(wf, query):
    result = execute(wf, ['brew', 'commands']).splitlines()
    commands = [x for x in result if ' ' not in x]
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], commands, match_on=MATCH_SUBSTRING)
    return commands


def get_all_services():
    services_response = execute(wf, ['brew', 'services', 'list']).splitlines()
    services_response.pop(0)
    services = []
    for serviceLine in services_response:
        services.append({'name': serviceLine.split()[0], 'status': serviceLine.split()[1]})
    return services


def filter_all_formulae(wf, query):
    formulae = wf.cached_data('brew_all_formulae',
                              get_all_formulae,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulae, match_on=MATCH_SUBSTRING)
    return formulae


def filter_installed_formulae(wf, query):
    formulae = wf.cached_data('brew_installed_formulae',
                              get_installed_formulae,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulae, match_on=MATCH_SUBSTRING)
    return formulae


def filter_pinned_formulae(wf, query):
    formulae = wf.cached_data('brew_pinned_formulae',
                              get_pinned_formulae,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulae, match_on=MATCH_SUBSTRING)
    return formulae


def filter_outdated_formulae(wf, query):
    formulae = wf.cached_data('brew_outdated_formulae',
                              get_outdated_formulae,
                              max_age=3600)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], formulae, match_on=MATCH_SUBSTRING)
    return formulae


def filter_all_services(wf, query):
    services = wf.cached_data('brew_all_services',
                              get_all_services,
                              session=True)
    query_filter = query.split()
    if len(query_filter) > 1:
        return wf.filter(query_filter[1], services, key=lambda x: x['name'], match_on=MATCH_SUBSTRING)
    return services


def add_service_actions(wf, service_name):
    wf.add_item('Run Service',
                'Run the service formula without registering to launch at login (or boot).',
                autocomplete='services %s run' % service_name,
                arg='brew services run %s' % service_name,
                valid=True,
                icon=helpers.get_icon(wf, 'chevron-right'))
    wf.add_item('Stop Service',
                'Stop the service formula immediately and unregister it from launching at login (or boot).',
                autocomplete='services %s stop' % service_name,
                arg='brew services stop %s' % service_name,
                valid=True,
                icon=helpers.get_icon(wf, 'chevron-right'))
    wf.add_item('Start Service',
                'Start the service formula immediately and register it to launch at login (or boot).',
                autocomplete='services %s start' % service_name,
                arg='brew services start %s' % service_name,
                valid=True,
                icon=helpers.get_icon(wf, 'chevron-right'))
    wf.add_item('Restart Service',
                'Stop (if necessary) and start the service formula immediately and register it to launch '
                'at login (or boot).',
                autocomplete='services %s restart' % service_name,
                arg='brew services restart %s' % service_name,
                valid=True,
                icon=helpers.get_icon(wf, 'chevron-right'))

def main(wf):
    if wf.update_available:
        wf.add_item('An update is available!',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=helpers.get_icon(wf, 'cloud-download'))

    # Check for brew installation
    find_brew = helpers.brew_installed()

    if not (find_brew['INTEL'] or find_brew['ARM']):
        helpers.brew_installation_instructions(wf)
    else:
        # extract query
        query = wf.args[0] if len(wf.args) else None

        if (not query and
                len(wf.cached_data('brew_outdated_formulae',
                                   get_outdated_formulae,
                                   max_age=3600)) > 0):
            wf.add_item('Some of your formulae are outdated!',
                        autocomplete='outdated ',
                        valid=False,
                        icon=helpers.get_icon(wf, 'cloud-download'))

        if query and query.startswith('install'):
            for formula in filter_all_formulae(wf, query):
                wf.add_item(formula, 'Install formula.',
                            arg='brew install %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('services'):
            query_filter = query.split()
            if len(query_filter) == 2 and query.endswith(' '):
                service_name = query_filter[1]
                add_service_actions(wf, service_name)
            else:
                services = filter_all_services(wf, query)
                for service in services:
                    wf.add_item(service['name'], 'Select for action. Status: %s' % service['status'],
                                autocomplete='services %s ' % service['name'],
                                arg='',
                                valid=False,
                                icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('search'):
            for formula in filter_all_formulae(wf, query):
                wf.add_item(formula, 'Open formula on GitHub.',
                            arg='brew info --github %s' % formula,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('uninstall'):
            for formula in filter_installed_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Uninstall formula.',
                            arg='brew uninstall %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('list'):
            for formula in filter_installed_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Open formula on GitHub.',
                            arg='brew info --github %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('pin'):
            for formula in filter_installed_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Pin formula.',
                            arg='brew pin %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
                # delete cached file
                wf.cache_data('brew_pinned_formulae', None)
        elif query and query.startswith('unpin'):
            for formula in filter_pinned_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Unpin formula.',
                            arg='brew unpin %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
                # delete cached file
                wf.cache_data('brew_pinned_formulae', None)
        elif query and query.startswith('cat'):
            for formula in filter_all_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Display the source to this formula.',
                            arg='brew cat %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('outdated'):
            for formula in filter_outdated_formulae(wf, query):
                name = formula.rsplit()[0]
                wf.add_item(formula, 'Upgrade formula.',
                            arg='brew upgrade %s' % name,
                            valid=True,
                            icon=helpers.get_icon(wf, 'package'))
        elif query and query.startswith('info'):
            wf.add_item(get_info(),
                        autocomplete='',
                        icon=helpers.get_icon(wf, 'info'))
        elif query and query.startswith('commands'):
            for command in get_commands(wf, query):
                wf.add_item(command, 'Run this command.',
                            arg='brew %s' % command,
                            valid=True,
                            icon=helpers.get_icon(wf, 'chevron-right'))
        elif query and query.startswith('config'):
            helpers.edit_settings(wf)
            wf.add_item('`settings.json` has been opened.',
                        autocomplete='',
                        icon=helpers.get_icon(wf, 'info'))
        else:
            actions = brew_actions.ACTIONS
            if len(wf.cached_data('brew_pinned_formulae',
                                  get_pinned_formulae,
                                  max_age=3600)) > 0:
                actions.append({
                    'name': 'Unpin',
                    'description': 'Unpin formula.',
                    'autocomplete': 'unpin ',
                    'arg': '',
                    'valid': False,
                })
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
    cmd = ['/usr/bin/env', 'python3', wf.workflowfile('brew_refresh.py')]
    run_in_background('brew_refresh', cmd)


if __name__ == '__main__':
    wf = Workflow(update_settings={'github_slug': GITHUB_SLUG})
    sys.exit(wf.run(main))

#!/usr/bin/env python3
# encoding: utf-8

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
        'name': 'upgrade',
        'description': 'Upgrade casks',
        'autocomplete': '',
        'arg': 'brew upgrade --cask',
        'valid': True
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew doctor',
        'valid': True
    },
    {
        'name': 'home',
        'description': 'Open the homepage of a cask',
        'autocomplete': 'home',
        'arg': '',
        'valid': False
    },
    {
        'name': 'config',
        'description': 'Open `settings.json` in your default editor.',
        'autocomplete': 'config',
        'arg': '',
        'valid': False
    },
    {
        'name': 'Clear workflow cache',
        'description': '',
        'autocomplete': 'workflow:delcache',
        'arg': '',
        'valid': False
    }
]

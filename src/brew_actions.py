#!/usr/bin/env python3
# encoding: utf-8

ACTIONS = [
    {
        'name': 'install',
        'description': 'Install formula.',
        'autocomplete': 'install ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'uninstall',
        'description': 'Uninstall formula.',
        'autocomplete': 'uninstall ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'search',
        'description': 'Perform a substring search of formula names.',
        'autocomplete': 'search ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'list',
        'description': 'List all installed formulae.',
        'autocomplete': 'list ',
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
        'name': 'update',
        'description': 'Update brew packages',
        'autocomplete': '',
        'arg': 'brew update',
        'valid': True
    },
    {
        'name': 'upgrade',
        'description': 'Upgrade brew packages',
        'autocomplete': '',
        'arg': 'brew upgrade --formula',
        'valid': True
    },
    {
        'name': 'services',
        'description': 'Control installed services',
        'autocomplete': 'services ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew doctor',
        'valid': True
    },
    {
        'name': 'info',
        'description': 'Show info',
        'autocomplete': 'info',
        'arg': '',
        'valid': False
    },
    {
        'name': 'cat',
        'description': 'Display the source to formula.',
        'autocomplete': 'cat ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'cleanup',
        'description': 'Remove any older versions from the cellar.',
        'autocomplete': '',
        'arg': 'brew cleanup',
        'valid': True
    },
    {
        'name': 'commands',
        'description': 'Show a list of built-in and external commands.',
        'autocomplete': 'commands ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'pin',
        'description': 'Pin the specified formulae.',
        'autocomplete': 'pin ',
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

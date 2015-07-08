ACTIONS = [
    {
        'name': 'install',
        'description': 'Install new packages',
        'autocomplete': 'install ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'uninstall',
        'description': 'Uninstall packages',
        'autocomplete': 'uninstall ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'search',
        'description': 'Search packages',
        'autocomplete': 'search ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'list',
        'description': 'List installed packages',
        'autocomplete': 'list ',
        'arg': '',
        'valid': False
    },
    {
        'name': 'update',
        'description': 'Update brew packages',
        'autocomplete': '',
        'arg': 'brew update',
        'valid':  True
    },
    {
        'name': 'upgrade',
        'description': 'Upgrade brew packages',
        'autocomplete': '',
        'arg': 'brew upgrade',
        'valid':  True
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew doctor',
        'valid':  True
    },
    {
        'name': 'info',
        'description': 'Show info',
        'autocomplete': 'info',
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

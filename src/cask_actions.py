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
        'name': 'update',
        'description': 'Update brew casks',
        'autocomplete': '',
        'arg': 'brew cask update',
        'valid':  True
    },
    {
        'name': 'doctor',
        'description': 'Run brew doctor',
        'autocomplete': '',
        'arg': 'brew cask doctor',
        'valid':  True
    },
    {
        'name': 'home',
        'description': 'Open the homepage of a cask',
        'autocomplete': 'home',
        'arg': '',
        'valid': False
    },
    {
        'name': 'alfred',
        'description': 'Modify Alfred\'s scope to include the Caskroom',
        'autocomplete': 'alfred',
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

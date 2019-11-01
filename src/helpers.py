import os

BREW_INSTALL_URL = 'https://raw.githubusercontent.com/Homebrew/install/' \
                   'master/install'


def brew_installed():
    return os.path.isfile('/usr/local/bin/brew')


def brew_installation_instructions(wf):
    wf.add_item('Brew does not seem to be installed!',
                'Hit enter to see what you need to do...',
                arg='open https://brew.sh/#install && exit',
                valid=True)
    wf.add_item('I trust this workflow',
                'Hit enter to install brew...',
                arg='ruby -e "$(curl -fsSL %s)"' % BREW_INSTALL_URL,
                valid=True)


def is_dark(wf):
    if not wf.alfred_env.get('theme_background'):
        return True
    rgb = [int(x) for x in wf.alfred_env['theme_background'][5:-6].split(',')]
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 < 0.5


def get_icon(wf, name):
    name = '%s-dark' % name if is_dark(wf) else name
    return "icons/%s.png" % name


def search_key_for_action(action):
    """ Name and description are search keys. """
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)

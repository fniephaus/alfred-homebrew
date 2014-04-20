import sys
import os
from workflow import Workflow

FORMULA_URL = 'https://github.com/Homebrew/homebrew/tree/master/Library/Formula'


def complete(wf):
    query = ' '.join(wf.args).split()

    if len(query) > 0 and query[0] == 'install':
        for item in list_all_packages():
            name = item.rsplit()[0]
            if len(query) == 1 or query[1] in name:
                wf.add_item(name, arg='brew install %s' % name, valid=True)
    elif len(query) > 0 and query[0] == 'uninstall':
        for item in list_packages():
            name = item.rsplit()[0]
            if len(query) == 1 or query[1] in name:
                wf.add_item(name, arg='brew uninstall %s' % name, valid=True)
    elif len(query) > 0 and query[0] == 'list':
        for item in list_packages(True):
            name = item.rsplit()
            name = '%s %s' % (name[0], name[1])
            if len(query) == 1 or query[1] in name:
                wf.add_item(name, 'Open formula on GitHub', arg='open %s/%s.rb' % (FORMULA_URL, name), valid=True)
    elif len(query) > 0 and query[0] == 'search':
        for item in list_all_packages():
            name = item.rsplit()[0]
            if len(query) == 1 or query[1] in name:
                wf.add_item(name, 'Open formula on GitHub', arg='open %s/%s.rb' % (FORMULA_URL, name), valid=True)
    elif len(query) > 0 and query[0] == 'info':
        info = os.popen('/usr/local/bin/brew info').readlines()[0]
        wf.add_item(info, autocomplete='')
    else:
        wf.add_item('install', 'Install new packages', uid="install", autocomplete='install ')
        wf.add_item('uninstall', 'Uninstall packages', uid="uninstall", autocomplete='uninstall ')
        wf.add_item('search', 'Search available packages', uid="search", autocomplete='search ')
        wf.add_item('list', 'List installed packages', uid="list", autocomplete='list ')
        wf.add_item('update', 'Update brew packages', uid="update", arg='brew update', valid=True)
        wf.add_item('upgrade', 'Upgrade brew packages', uid="upgrade", arg='brew upgrade', valid=True)
        wf.add_item('doctor', 'Run brew doctor', uid="doctor", arg='brew doctor', valid=True)
        wf.add_item('info', 'Show info', uid="info", autocomplete='info')

    wf.send_feedback()

def list_packages(versions=False):
    options = '--versions' if versions else ''
    return os.popen('/usr/local/bin/brew list %s' % options).readlines()

def list_all_packages():
    return os.popen('/usr/local/bin/brew search').readlines()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(complete))

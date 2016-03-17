import brew

from workflow import Workflow


if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('brew_all_formulae', brew.get_all_formulae())
    wf.cache_data('brew_installed_formulae', brew.get_installed_formulae())
    wf.cache_data('brew_pinned_formulae', brew.get_pinned_formulae())
    wf.cache_data('brew_outdated_formulae', brew.get_outdated_formulae())

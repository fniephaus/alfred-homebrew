import brew

from workflow import Workflow


if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('brew_all_formulas', brew.get_all_packages())
    wf.cache_data('brew_installed_formulas', brew.get_installed_packages())

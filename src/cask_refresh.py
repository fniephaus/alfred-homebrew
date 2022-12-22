#!/usr/bin/env python3
# encoding: utf-8

import cask
from workflow import Workflow

if __name__ == '__main__':
    wf = Workflow()
    wf.cache_data('cask_all_casks', cask.get_all_casks())
    wf.cache_data('cask_installed_casks', cask.get_installed_casks())
    wf.cache_data('cask_outdated_casks', cask.get_outdated_casks())

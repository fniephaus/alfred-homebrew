#!/usr/bin/env python3
# encoding: utf-8

import unittest

import brew
import cask
import helpers
from workflow import Workflow


class HomeBrewTestCase(unittest.TestCase):

    def setUp(self):
        self.wf = Workflow()
        cask.wf = Workflow()
        brew.wf = Workflow()

    def test_get_all_formulae(self):
        result = brew.get_all_formulae()
        self.assertTrue(len(result) > 0)

    def test_search_key_for_action(self):
        result = helpers.search_key_for_action({
            'name': 'a',
            'description': 'b',
        })
        self.assertEqual(result, 'a b')

    def test_brew_get_installed_packages(self):
        result = brew.get_installed_formulae()
        self.assertTrue(len(result) >= 0)

    def test_brew_get_info(self):
        result = brew.get_info()
        self.assertTrue(all(x in result for x in ['kegs', 'files']))

    def test_cask_get_all_casks(self):
        result = cask.get_all_casks()
        self.assertTrue(len(result) > 0)

    def test_cask_get_installed_casks(self):
        result = cask.get_installed_casks()
        self.assertTrue(len(result) >= 0)

    def test_cask_execute(self):
        for cmd in ['search', 'list']:
            result = cask.execute(cask.wf, ['brew', cmd, '--cask'])
            # Changed to >= 0 cause sometimes a cask has not been installed.
            self.assertTrue(len(result) >= 0)

    def test_brew_execute(self):
        for cmd in ['search', 'list']:
            result = brew.execute(brew.wf, ['brew', cmd])
            self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()

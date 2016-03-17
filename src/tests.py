import unittest
import brew
import cask
import helpers
from workflow import Workflow


class HomeBrewTestCase(unittest.TestCase):

    def setUp(self):
        self.wf = Workflow()

    def test_get_all_packages(self):
        result = brew.get_all_packages(self.wf, '')
        self.assertTrue(len(result) > 0)
        result = brew.get_all_packages(self.wf, '------ ------')
        self.assertTrue(len(result) == 0)

    def test_search_key_for_action(self):
        result = helpers.search_key_for_action({
            'name': 'a',
            'description': 'b',
        })
        self.assertEquals(result, u'a b')

    def test_brew_get_all_packages(self):
        result = brew.get_all_packages(self.wf, '')
        self.assertTrue(len(result) > 0)

    def test_brew_get_installed_packages(self):
        result = brew.get_installed_packages(self.wf, '')
        self.assertTrue(len(result) >= 0)

    def test_brew_get_info(self):
        result = brew.get_info()
        self.assertTrue(all(x in result for x in ['kegs', 'files']))

    def test_cask_get_all_casks(self):
        result = cask.get_all_casks(self.wf, '')
        self.assertTrue(len(result) > 0)

    def test_cask_get_installed_casks(self):
        result = cask.get_installed_casks(self.wf, '')
        self.assertTrue(len(result) >= 0)

    def test_cask_execute(self):
        result = cask.execute(self.wf, 'notimplemented')
        self.assertIsNone(result)
        for cmd in ['search', 'list', 'alfred status']:
            result = cask.execute(self.wf, cmd)
            self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()

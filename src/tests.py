import unittest
import brew
import brew_refresh
import cask_refresh


class HomeBrewTestCase(unittest.TestCase):

    def test_get_all_packages(self):
        result = brew.get_all_packages("")
        self.assertTrue(len(result) > 0)
        result = brew.get_all_packages("------ ------")
        self.assertTrue(len(result) == 0)

    def test_search_key_for_action(self):
        result = brew.search_key_for_action({
            'name': 'a',
            'description': 'b',
        })
        self.assertEquals(result, u'a b')

    def test_refresh_get_all_packages(self):   
        result = brew_refresh.get_all_packages()
        self.assertTrue(len(result) > 0)

    def test_refresh_get_installed_packages(self):
        result = brew_refresh.get_installed_packages()
        self.assertTrue(len(result) >= 0)

    def test_refresh_get_info(self):
        result = brew_refresh.get_info()
        self.assertTrue(all(x in result for x in ['kegs', 'files']))

    def test_refresh_get_all_casks(self):
        result = cask_refresh.get_all_casks()
        self.assertTrue(len(result) > 0)

    def test_refresh_get_installed_casks(self):
        result = cask_refresh.get_installed_casks()
        self.assertTrue(len(result) >= 0)

    def test_refresh_execute_cask_command(self):
        result = cask_refresh.execute_cask_command('notimplemented')
        self.assertIsNone(result)
        for cmd in ['search', 'list', 'alfred status']:
            result = cask_refresh.execute_cask_command(cmd)
            self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()

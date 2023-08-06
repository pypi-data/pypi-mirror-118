import unittest
import pandas as pd

from project.scraper import Scraper


class ScraperTest(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    @unittest
    def test_get_links(self):
        expected_value = None
        actual_value = self.scraper.get_links()
        self.assertEqual(expected_value, actual_value)

    @unittest
    def test_get_csv_from_dict(self, dict_attacks):
        test_dict = {'Title': [], 'Date': [], 'Affiliation': [], 'Description': [], 'Suspected Victims':[], 'Suspected State Sponsor':[], 'Type Of Incident': [], 'Target Category':[], 'Victim Government Reaction': [] }
        test_df = pd.DataFrame.from_dict(test_dict)
        expected_value = test_df
        actual_value = Scraper.get_csv_from_dict(test_dict, 'test')
        self.assertTrue(expected_value.equals(actual_value))

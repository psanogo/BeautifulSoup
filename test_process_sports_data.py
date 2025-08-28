#!/usr/bin/env python3

import unittest
import os
import csv
from unittest.mock import patch

# Import the functions from the script to be tested
from process_sports_data import scrape_and_process_data, save_to_csv, main

class TestProcessSportsData(unittest.TestCase):
    """Unit tests for the process_sports_data.py script."""

    def test_scrape_and_process_data(self):
        """
        Test that scrape_and_process_data returns a list of lists with the correct structure.
        """
        result = scrape_and_process_data()
        self.assertIsInstance(result, list, "Function should return a list.")
        self.assertTrue(all(isinstance(row, list) for row in result), "All items in the list should be lists.")
        if result:
            self.assertEqual(len(result[0]), 7, "Each row should have 7 elements.")

    def test_save_to_csv(self):
        """
        Test that save_to_csv writes the correct header and data to a file.
        """
        test_filename = "test_output.csv"
        test_header = ['ID', 'Name']
        test_data = [
            [1, 'Alice'],
            [2, 'Bob']
        ]

        # Ensure the file doesn't exist before the test
        if os.path.exists(test_filename):
            os.remove(test_filename)

        # Call the function to be tested
        save_to_csv(test_data, test_filename, test_header)

        # Verify the file was created and has the correct content
        self.assertTrue(os.path.exists(test_filename), "CSV file was not created.")

        with open(test_filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Read header and check
            header_from_file = next(reader)
            self.assertEqual(header_from_file, test_header, "CSV header does not match.")
            # Read data and check
            data_from_file = list(reader)
            # The csv reader reads all fields as strings, so we convert for comparison
            expected_data_as_str = [[str(item) for item in row] for row in test_data]
            self.assertEqual(data_from_file, expected_data_as_str, "CSV data does not match.")

        # Clean up the temporary file
        os.remove(test_filename)

    @patch('process_sports_data.save_to_csv')
    @patch('process_sports_data.scrape_and_process_data')
    def test_main(self, mock_scrape, mock_save):
        """
        Test the main function to ensure it calls its helper functions correctly.
        """
        mock_data = [[1, 'TeamA', 'TeamB', 1.0, 2.0, 3.0, 'TeamA']]
        mock_scrape.return_value = mock_data

        main()

        mock_scrape.assert_called_once()
        expected_header = ['GameID', 'Team 1', 'Team 2', 'Expected Runs (Team 1)', 'Expected Runs (Team 2)', 'Over/Under', 'Moneyline Favorite']
        mock_save.assert_called_once_with(mock_data, 'sports_statistics.csv', expected_header)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
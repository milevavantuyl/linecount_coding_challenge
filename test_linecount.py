""" This file contains the tests for the linecount module. """

import os
import unittest
from unittest import mock
import csv
import numpy as np
from linecount import dir_line_count, file_line_count


class TestLineCount(unittest.TestCase):
    """ This class contains unit tests for the linecount program.

    Sample files (e.g. txt and csv) files are created within directories for testing
    purposes. They are created before any of the tests are executed and removed
    after all tests have been completed.

    This class contains the following functions:

        * setUpClass - creates the sample files and directories used for testing
        * tearDownClass - removes the sample files and directories created for testing
        * test_file_line_count - tests the file_line_count function
        * test_dir_line_counts - tests the dir_line_count function

    """
    @classmethod
    def setUpClass(cls):

        # Create an empty directory
        cls.directory_path_empty = './unit_test_files_empty'
        os.mkdir(cls.directory_path_empty)

        # Create a nested directory structure to store testing files with different extenions
        cls.directory_path = './unit_test_files'
        cls.subdirectory_path = os.path.join(cls.directory_path, 'some_other_files')
        os.mkdir(cls.directory_path)
        os.mkdir(cls.subdirectory_path)

        # Populate the nested directory with .txt testing files
        file_1_contents = ["5_lines.txt\n", "Regular txt file\n", "Line 1, \n",
                             "... \n", "5 Lines in total!"]
        file_2_contents = []
        file_3_contents = ["\n", "\n", "\n"]

        with open(os.path.join(cls.directory_path, "5_lines.txt"), "a", encoding='utf-8') as out:
            out.writelines(file_1_contents)

        with open(os.path.join(cls.directory_path, "empty_file.txt"), "a", encoding='utf-8') as out:
            out.writelines(file_2_contents)

        with open(os.path.join(cls.subdirectory_path, "3_empty_lines.txt"),
                    "a", encoding='utf-8') as out:
            out.writelines(file_3_contents)

        # Populate the nested directory with .csv testing files
        file_4_contents = np.arange(0, 20).reshape(4,5)
        file_5_contents = np.arange(0, 100).reshape(20,5)
        file_6_contents = np.arange(0, 100).reshape(100,1)

        with open(os.path.join(cls.directory_path, '4_lines.csv'), 'w', encoding='utf-8') as out:
            writer = csv.writer(out)
            writer.writerows(file_4_contents)

        with open(os.path.join(cls.subdirectory_path, '20_lines.csv'),'w', encoding='utf-8') as out:
            writer = csv.writer(out)
            writer.writerows(file_5_contents)

        with open(os.path.join(cls.subdirectory_path, '100_lines.csv'),'w',encoding='utf-8') as out:
            writer = csv.writer(out)
            writer.writerows(file_6_contents)

    @classmethod
    def tearDownClass(cls):
        # Remove all files created during setup
        for dirpath, _, filenames in os.walk(cls.directory_path):
            for filename in filenames:
                os.remove(os.path.join(dirpath, filename))

        # Remove all directories created during setup
        os.rmdir(cls.directory_path_empty)
        os.rmdir(cls.subdirectory_path)
        os.rmdir(cls.directory_path)


    def test_file_line_count(self):
        """ Test the function linecount.file_line_count. """

        # Paths to the directories defined in set up
        directory_path = './unit_test_files'
        subdirectory_path = os.path.join(directory_path, 'some_other_files')

        # Test 1 - An invalid file path: Triggers a file not found error
        self.assertRaises(FileNotFoundError, file_line_count,
                        os.path.join(directory_path, "nonexistent_file.txt"))

        # Test 2 - A normal txt file with 5 lines
        self.assertEqual(file_line_count(os.path.join(directory_path, "5_lines.txt")), 5)

        # Test 3 - An empty text file with 0 lines
        self.assertEqual(file_line_count(os.path.join(directory_path, "empty_file.txt")), 0)

        # Test 4 - A txt file containing 3 empty lines
        self.assertEqual(file_line_count(os.path.join(subdirectory_path, "3_empty_lines.txt")), 3)

        # Test 5 - A csv file with 100 lines
        self.assertEqual(file_line_count(os.path.join(subdirectory_path, "100_lines.csv")), 100)

    def test_dir_line_count(self):
        """ Test the function linecount.dir_line_count. """

        # Paths to the directories defined in set up
        directory_path_empty = './unit_test_files_empty'
        directory_path = './unit_test_files'
        subdirectory_path = os.path.join(directory_path, 'some_other_files')

        # Expected output for scenarios where no files are found
        no_files_expected_stdout = [
            mock.call.write("==============="),
            mock.call.write("\n"),
            mock.call.write("Number of files found: \t 0"),
            mock.call.write("\n"),
            mock.call.write("Total number of lines: \t 0"),
            mock.call.write("\n"),
            mock.call.write("Average lines per file: \t 0 files found."),
            mock.call.write("\n")
        ]

        # Test 1 - An invalid directory path: Finds 0 files and returns no errors
        self.assertListEqual(dir_line_count('./invalid_directory_path'), [])
        with mock.patch('sys.stdout') as mocked_stdout:
            dir_line_count('./invalid_directory_path')
        mocked_stdout.assert_has_calls(no_files_expected_stdout)

        # Test 2 - A path to an empty directory: Finds 0 files and returns no errors
        self.assertListEqual(dir_line_count(directory_path_empty), [])
        with mock.patch('sys.stdout') as mocked_stdout:
            dir_line_count(directory_path_empty)
        mocked_stdout.assert_has_calls(no_files_expected_stdout)

        # Test 3 - No extension provided: Finds .txt files and computes the number of lines
        self.assertListEqual(dir_line_count(directory_path),
            [(os.path.join(directory_path, "empty_file.txt"), 0),
            (os.path.join(directory_path, "5_lines.txt"), 5),
            (os.path.join(subdirectory_path, "3_empty_lines.txt"), 3)])

        with mock.patch('sys.stdout') as mocked_stdout:
            dir_line_count(directory_path)

        mocked_stdout.assert_has_calls([
            mock.call.write(f"{os.path.join(directory_path, 'empty_file.txt')} \t 0"),
            mock.call.write("\n"),
            mock.call.write(f"{os.path.join(directory_path, '5_lines.txt')} \t 5"),
            mock.call.write("\n"),
            mock.call.write(f"{os.path.join(subdirectory_path, '3_empty_lines.txt')} \t 3"),
            mock.call.write("\n"),
            mock.call.write("==============="),
            mock.call.write("\n"),
            mock.call.write("Number of files found: \t 3"),
            mock.call.write("\n"),
            mock.call.write("Total number of lines: \t 8"),
            mock.call.write("\n"),
            mock.call.write("Average lines per file: \t 2.67"),
            mock.call.write("\n")
        ])

        # Test 4 - Extension that isn't txt (e.g. csv):
        # Finds the csv files and computes the number of lines
        self.assertListEqual(dir_line_count(directory_path, '.csv'),
            [(os.path.join(directory_path, '4_lines.csv'), 4),
            (os.path.join(subdirectory_path, '100_lines.csv'), 100),
            (os.path.join(subdirectory_path, '20_lines.csv'), 20)])

        with mock.patch('sys.stdout') as mocked_stdout:
            dir_line_count(directory_path, '.csv')

        mocked_stdout.assert_has_calls([
            mock.call.write(f"{os.path.join(directory_path, '4_lines.csv')} \t 4"),
            mock.call.write("\n"),
            mock.call.write(f"{os.path.join(subdirectory_path, '100_lines.csv')} \t 100"),
            mock.call.write("\n"),
            mock.call.write(f"{os.path.join(subdirectory_path, '20_lines.csv')} \t 20"),
            mock.call.write("\n"),
            mock.call.write("==============="),
            mock.call.write("\n"),
            mock.call.write("Number of files found: \t 3"),
            mock.call.write("\n"),
            mock.call.write("Total number of lines: \t 124"),
            mock.call.write("\n"),
            mock.call.write("Average lines per file: \t 41.33"),
            mock.call.write("\n")
        ])

if __name__ == "__main__":
    unittest.main()

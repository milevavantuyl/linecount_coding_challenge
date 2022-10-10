""" File and Directory Line Counter

This program allows the user to compute the number of lines in files
with a given extension and stored in a given directory. It outputs the
number of corresponding files, the total number of lines,
and the average number of lines per file.

The program has been tested for files with .txt, .csv, and .pdf extensions.
In the case of file extensions like .pdf files that have specific encodings,
the line counts may be unexpected as they are based on the internal encodings
of the files rather than the high-level text viewed when the pdf is opened.

'Numpy' must be installed to run the program.

This file contains the following functions:

    * file_line_count - returns the number of lines in a given file
    * dir_line_count - returns a list of all files with the extension and their line counts
    * main - allows for quick testing via the command line

"""

import os
import sys
import numpy as np

def file_line_count(filepath):
    """Return the number of lines within the file. An error is raised if the filepath is invalid."""
    with open(filepath, encoding='utf-8', errors="replace") as file:
        num_lines = sum(1 for line in file)
    return num_lines

def dir_line_count(directory, extension = ".txt"):
    """Count the number of lines in each file with the given extension within the directory."""

    # Get the files within the given directory and its subdirectories
    all_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))

    # Get line counts of files with the gien extension
    files_with_extension = []
    line_counts = []
    for file in all_files:
        if file.endswith(extension):
            files_with_extension.append(file)
            line_counts.append(file_line_count(file))

    files_and_counts = list(zip(files_with_extension, line_counts))

    # Report the results
    for file, length in files_and_counts:
        print(f"{file} \t {length}")
    print("===============")
    print(f"Number of files found: \t {len(files_with_extension)}")
    print(f"Total number of lines: \t {int(np.sum(line_counts))}")
    if len(files_with_extension) > 0:
        print(f"Average lines per file: \t {round(np.mean(line_counts),2)}")
    else:
        print("Average lines per file: \t 0 files found.")

    return files_and_counts

if __name__ == "__main__":

    user_args = sys.argv
    print("User provided arguments:", user_args[1:])

    # Directory is provided
    if len(user_args) == 2:
        dir_line_count(sys.argv[1])

    # Directory and filename extension are provided
    elif len(user_args) == 3:
        if sys.argv[2][0] != '.':
            print('''The filename extension is incorrectly. Examples of proper formatting:
            \'.txt\' or \'.csv\'''')
        else:
            dir_line_count(sys.argv[1], sys.argv[2])

    # Provided an incorrect number of arguments
    else:
        print('''This program expects one or two arguments:
        Arg1: string, directory path,
        Arg2 (optional): string, filename extension''')

    # # User testing with txt and csv files
    # print("# Lines in txt file (5):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', '5_lines.txt')))
    # print("# Lines in csv file (4):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', '4_lines.csv')))

    # # User testing with pdf, doc, docx, and xlsx files
    # print("# Lines in pdf file (162):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', 'sample_1.pdf')))
    # print("# Lines in doc file (52):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', 'sample_1.doc')))
    # print("# Lines in docx file (71):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', 'sample_1.docx')))
    # print("# Lines in xlsx file (48):",
    #     file_line_count(os.path.join('./sample_dir_for_testing', 'sample_1.xlsx')))

    # # User testing of the full program
    # print(dir_line_count('./sample_dir_for_testing'))

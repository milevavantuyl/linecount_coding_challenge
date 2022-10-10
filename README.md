# File and Directory Line Counter

## Introduction 
The File and Directory Line Counter for Python takes a directory and an optional filename extension. The program then counts and reports statistics about the number of lines in all files that have the extension within the directory. 

At this time, the program has been tested for txt, csv, pdf, xlsx, doc, and docx files. Note that files including pdf, xlsx, doc, and docx file types may produce unexpected results. This is because the program counts the lines of the files based on the internal encodings and file format rather than the high-level text that is viewed when the file is opened by a user. Future development will focus on further addressing this challenge. 

## Installation and Usage
To run this program: 

1. Clone this repository from GitHub.
2. (Optional) Create a virtual environment with a Python environemnt manager like Conda.  
`conda create -n linecount python numpy pylint`  
`conda activate linecount`   
3. Navigate to the repository in your terminal.
4. Run the program from the command line as desired:   
`python linecount.py sample_dir_for_testing`     
`python linecount.py sample_dir_for_testing .csv`

## Contents
For reference, the repository contains the following components:
* linecount.py – Contains the program that computes the number of lines in the directory as defined by the problem formulation.  
* test_linecount.py – Contains the unit tests for linecount.py
*	sample_dir_for_testing – A directory for quick testing by the user. This directory is similar to the directory that is programmatically created and deleted during unit tests. 

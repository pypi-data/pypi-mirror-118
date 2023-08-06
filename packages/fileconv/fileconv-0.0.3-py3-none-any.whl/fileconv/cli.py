"""
This script will convert .txt , .docx or .doc & .xlsx or .xls / .csv to .pdf
It uses 'fpdf', 'docx2pdf' & 'win32' to execute this task.

The programm crawls over one directory with (possible multiple) subdirectories and identifies files, by their extension and converts them to pdf, while leaving the old ones 


@Author: ovanov
@Date: 26.03.21
"""

import argparse
from typing import Dict

from .crawlers import Crawler


def argument_parser() -> Dict:
    parser = argparse.ArgumentParser('fileconv',description='Command line tool for file conversion to PDF. Supports MS Word, Excel and txt files.')

    parser.add_argument('--pdf',
    help='(required) filepath to the directory, in which the files should be converted to PDF',
    nargs='?',
    type=str,
    default=False)

    parser.add_argument('--txt',
    help='(required) filepath to the directory, in which the files should be converted to TXT',
    nargs='?',
    type=str,
    default=False)

    parser.add_argument('--output', '-o',
    help='(required) Give the path and the name of the output directory.',
    nargs='?',
    type=str,
    default=False)

    return parser


def main():
    """
    Change the "path" variable, in order to pass the directory
    """
    # get argument parser
    parser = argument_parser()
    args = parser.parse_args()
    args_dict = {
        arg: value for arg, value in vars(args).items()
        if value is not None
    }

    if args_dict['pdf'] == False and args_dict['txt'] == False: 
        raise KeyError('Please give a path to a file or a dirctory path.')
    if args_dict['pdf'] != False and args_dict['txt'] != False: 
        raise KeyError("Please give only one task. fileconv can't parse in both ways at once.")

    if args_dict['pdf'] != False:
        path = args_dict['pdf']
        output = args_dict['output']
        Crawler.crawl(path, output)

    else:
        path = args_dict['txt']
        output = args_dict['output']
        Crawler.pdf_crawl(path, output)

    return

if __name__ == "__main__":
    main()

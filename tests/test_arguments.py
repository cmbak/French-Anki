import os
import sys
from main import validate_file_format

def test_no_file_args():
    assert validate_file_format([]) == (False, 'Please enter a path to the text file')

def test_too_many_file_args():
    assert validate_file_format(['file1.txt', 'file2.txt']) == (False, 'Please enter a path to the text file')

def test_invalid_path():
    assert validate_file_format(['file1.txt']) == (False, 'Please enter a valid file path!')

def test_not_text_file():
    assert validate_file_format([os.path.dirname(__file__)]) == (False, 'Please enter a valid file format (.txt)!')

def test_valid_path():
    if sys.platform == 'win32':
        path_to_sample = 'sample_texts\\art_de_la_traduction.txt'
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        path_to_sample = 'sample_texts/art_de_la_traduction.txt'
    path_to_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', path_to_sample)) # Need to go up one dir
    assert validate_file_format([path_to_file]) == (True, f'{path_to_file} has been found!')
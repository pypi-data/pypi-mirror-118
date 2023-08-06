#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides main utilities that are related to the Polymatheia package."""

import glob
import json
import os
import shutil
import sys

from loguru import logger
from progress.bar import Bar

from polymatheia_tools.config import LOGGING_FILENAME, LOGGING_FORMAT


class PolymatheiaUtils:
    """The :class:`~polymatheia_tools.utils.PolymatheiaUtils` provides utilities
    related to the Polymatheia package.
    """

    INPUT_FOLDER = "polymatheia_files"
    OUTPUT_FOLDER = "polymatheia_files_extracted"
    FILE_EXT = "xml"

    @staticmethod
    def extract(i, o, e):
        """Extract files from the Polymatheia folder structure to a flat structure in a single folder.

        :param i: Path to input folder
        :type i: ``str``
        :param o: Path to output folder
        :type o: ``str``
        :param e: File extension of Polymatheia files
        :type e: ``str``
        """
        if not os.path.exists(o):
            os.makedirs(o)

        nr_of_files = sum([len(files) for r, d, files in os.walk(i)])
        with Bar("Progress: ", max=nr_of_files) as progressbar:
            for file_path in glob.glob(os.path.join(i, '**', '*.' + e), recursive=True):
                new_path = os.path.join(o, os.path.basename(file_path))
                shutil.copy(file_path, new_path)
                progressbar.next()


class MainUtils:
    """The :class:`~polymatheia_tools.utils.MainUtils` provides generic utilities."""

    @staticmethod
    def convert_to_list(elem):
        """Convert an element to a list, if necessary.

        :param elem: An object
        :type elem: ``object``
        :return: List containing elem if elem is not already a list, elem otherwise
        :rtype: ``list``
        """
        return [elem] if not type(elem) == list else elem


class DictUtils:
    """The :class:`~polymatheia_tools.utils.DictUtils` provides generic utilities."""

    # Default values
    INFILE = "input_dict.json"
    OUTFILE = "input_dict_keys_removed.json"
    _ENCODING = "utf-8"

    @staticmethod
    def remove_keys(i, o, k):
        """Remove all keys from a given dict i (in a JSON file) if not in k and save the remaining dict as JSON in o.

        :param i: Path to input JSON file
        :type i: ``str``
        :param o: Path to output JSON file
        :type o: ``str``
        :param k: List of keys to be removed
        :type k: ``list``
        """
        # Set up logging
        logger.remove()
        logger.add(LOGGING_FILENAME, format=LOGGING_FORMAT, level="DEBUG")
        logger.add(sys.stderr, level="INFO")

        with open(i, "r", encoding=DictUtils._ENCODING) as f:
            in_data = json.load(f)

        out_data = dict()
        for key in in_data.keys():
            if key in list(k):
                out_data[key] = in_data[key]

        if not os.path.exists(os.path.dirname(o)):
            os.makedirs(os.path.dirname(o))
        with open(o, 'w', encoding=DictUtils._ENCODING) as f:
            json.dump(out_data, f, indent=4)
            logger.info(f"Keys from {i} were removed (except keys in {k}). New dictionary was written to {o}.")

    @staticmethod
    def remove_empty_entries(d):
        """Remove keys from dict d that have no values.

        :param d: A dictionary
        :type d: ``dict``
        :return: Input dictionary without empty entries.
        :rtype: ``dict``
        """
        if isinstance(d, dict):
            return {
                k: v
                for k, v in ((k, DictUtils.remove_empty_entries(v)) for k, v in d.items())
                if v
            }
        if isinstance(d, list):
            return [v for v in map(DictUtils.remove_empty_entries, d) if v]
        return d

    @staticmethod
    def merge(a, b):
        """Merge two dictionaries.

        :param a: A dictionary
        :type a: ``dict``
        :param b: Another dictionary
        :type b: ``dict``
        :raise: KeyError if a key is found in both dictionaries
        :return: Dictionary a merged with b
        :rtype: ``dict``
        """
        intersection = set(a.keys()).intersection(set(b.keys()))
        if len(intersection) > 0:
            raise KeyError(f"Duplicate key found: {intersection}.")
        else:
            a.update(b)
            return a

    @staticmethod
    def get_top_keys(d, k):
        """Get keys with highest values from a dictionary.

        :param d: A dictionary
        :type d: ``dict``
        :param k: Top k elements that will be returned
        :type k: ``int``
        :return: List of tuples (value, key) for top k keys
        :rtype: ``list``
        """
        items = sorted(d.items(), reverse=True, key=lambda x: x[1])
        return map(lambda x: x[0], items[:k])

    @staticmethod
    def sort_by_key(d):
        """Sort a dictionary alphabetically by its keys.

        :param d: A dictionary
        :type d: ``dict``
        :return: The sorted dictionary
        :rtype: ``dict``
        """
        return dict(sorted(d.items(), key=lambda x: str(x[0])))

    @staticmethod
    def save_to_json(d, f):
        """Save a dictionary to a JSON file.

        :param d: A dictionary
        :type d: ``dict``
        :param f: Path to file
        :type f: ``str``
        """
        if not os.path.exists(os.path.dirname(f)):
            os.makedirs(os.path.dirname(f))
        with open(f, 'w', encoding=DictUtils._ENCODING) as file:
            json.dump(d, file, indent=4)

    @staticmethod
    def read_from_json(f):
        """Read a dictionary from a JSON file.

        :param f: Path to file
        :type f: ``str``
        :return: Dictionary loaded from JSON file
        :rtype: ``dict``
        """
        with open(f, "r", encoding=DictUtils._ENCODING) as file:
            return json.load(file)

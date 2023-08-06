#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides a class for analyzing the number and type of all PICA fields used in a corpus."""

import os
import sys

from loguru import logger
from polymatheia.data.reader import XMLReader
from polymatheia.filter import RecordsFilter
from progress.bar import Bar

from polymatheia_tools.config import LOGGING_FILENAME, LOGGING_FORMAT
from polymatheia_tools.parsing import DatafieldParser
from polymatheia_tools.utils import DictUtils, MainUtils


class PICAAnalysis:
    """The :class:`~polymatheia_tools.analysis.PICAAnalysis` provides a PICA fields analysis.

    After creating a new :class:`~polymatheia_tools.analysis.PICAAnalysis` the analysis can be started
    by calling the ``start`` function.
    """

    INFOLDER = "input_files"
    OUTFILE = "field_analysis.json"

    # Keys for JSON fields in the output file
    _COUNT = "total"
    _UNIQUE_COUNT = "in_X_records"
    _SUBFIELDS = "subfields"
    _CODE_TOTAL = "total"
    _UNIQUE_INSIDE_DATAFIELD = "in_X_datafields"
    _UNIQUE_INSIDE_RECORD = "in_X_records"

    def __init__(self, i=INFOLDER, o=OUTFILE):
        """Construct a new :class:`~polymatheia_tools.analysis.PICAAnalysis`.

        Parameters are optional. If a parameter is missing, the default class values
        from :class:`~polymatheia_tools.analysis.PICAAnalysis` are used.

        :param i: Path to folder that contains data sets as files in XML format
        :type i: ``str``
        :param o: Path to output file where field analysis will be saved
        :type o: ``str``
        """
        reader = XMLReader(i)
        fltr = ('true',)
        self._all_records = RecordsFilter(reader, fltr)
        # self._nr_records = 100
        self._nr_records = len(next(os.walk(i))[2])
        self._json_output_file = o
        self._result_dict = {}

    def start(self):
        """Start the analysis."""
        # Set up logging
        logger.remove()
        logger.add(LOGGING_FILENAME, format=LOGGING_FORMAT, level="DEBUG")
        logger.add(sys.stderr, level="INFO")

        logger.info("PICAAnalysis started.")
        with Bar("Progress: ", max=self._nr_records) as progressbar:
            for record in self._all_records:
                try:
                    datafields = record.zs_recordData['infosrwschema5picaXML-v1.0record'].datafield
                    self._parse_record(datafields)
                except Exception as e:
                    logger.debug(f"Record can not be processed: {e}")
                progressbar.next()

        # Remove empty keys and sort dict
        self._result_dict = DictUtils.remove_empty_entries(self._result_dict)
        self._sort_fields(sub=True)
        self._sort_fields()

        logger.debug(f"Keys from result dictionary: {self._result_dict.keys()}")

        DictUtils.save_to_json(self._result_dict, self._json_output_file)
        logger.info(f"Analysis results saved to {self._json_output_file}.")

    def _parse_record(self, fields):
        """Parse a single record from an XML file.

        :param fields: Datafields in a single record
        :type fields: ``object``
        """
        datafields = MainUtils.convert_to_list(fields)

        tags_in_this_record = []
        codes_in_this_record = []

        for field in datafields:
            tag, codes = DatafieldParser.parse(field, code_only=True)
            tags_in_this_record, codes_in_this_record = self._add_to_dict(
                tag, codes, tags_in_this_record, codes_in_this_record
            )

    def _add_to_dict(self, tag, codes, tags_in_this_record, codes_in_this_record):
        """Add collected elements to the result dictionary.

        :param tag: The tag for a single datafield
        :type tag: ``str``
        :param codes: Subfield codes in a single datafield
        :type codes: ``list``
        :param tags_in_this_record: All tags found in a record
        :type tags_in_this_record: ``list``
        :param codes_in_this_record: All codes found in a record
        :type codes_in_this_record: ``list``
        :return: List of tags and list of codes in a record
        :rtype: ``list``, ``list``
        """
        # Add tag to result dict, if not yet existent
        if tag not in self._result_dict.keys():
            self._result_dict[tag] = {}
            self._result_dict[tag][PICAAnalysis._COUNT] = 1
            self._result_dict[tag][PICAAnalysis._UNIQUE_COUNT] = 1
            self._result_dict[tag][PICAAnalysis._SUBFIELDS] = {}
        # If tag is existent, increase counter
        else:
            self._result_dict[tag][PICAAnalysis._COUNT] += 1
            if tag not in tags_in_this_record:
                self._result_dict[tag][PICAAnalysis._UNIQUE_COUNT] += 1
        # Remember that tag was already encountered
        tags_in_this_record.append(tag)

        # Count occurrence of subfield codes
        codes_in_this_datafield = []
        for code in codes:
            if code:
                # Subfield code not yet in result dict
                if code not in self._result_dict[tag][PICAAnalysis._SUBFIELDS].keys():
                    self._result_dict[tag][PICAAnalysis._SUBFIELDS][code] = {}
                    self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][PICAAnalysis._CODE_TOTAL] = 1
                    self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][PICAAnalysis._UNIQUE_INSIDE_RECORD] = 1
                    self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][PICAAnalysis._UNIQUE_INSIDE_DATAFIELD] = 1
                # Subfield code already in result dict
                else:
                    self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][PICAAnalysis._CODE_TOTAL] += 1
                    if tag + "--" + code not in codes_in_this_record:
                        self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][PICAAnalysis._UNIQUE_INSIDE_RECORD] += 1
                    # Count uniqueness of code in datafield
                    if code not in codes_in_this_datafield:
                        self._result_dict[tag][PICAAnalysis._SUBFIELDS][code][
                            PICAAnalysis._UNIQUE_INSIDE_DATAFIELD
                        ] += 1
                # Remember occurrence of code in record and datafield
                codes_in_this_record.append(tag + "--" + code)
                codes_in_this_datafield.append(code)

        return tags_in_this_record, codes_in_this_record

    def _sort_fields(self, sub=False):
        """Sort fields in the result dict.

        :param sub: Whether subfields should be sorted. If ``False``, keys on the main level will be sorted only.
        :type sub: ``bool``
        """
        if sub:
            for key in self._result_dict.keys():
                subfield_dict = self._result_dict[key][PICAAnalysis._SUBFIELDS]
                self._result_dict[key][PICAAnalysis._SUBFIELDS] = DictUtils.sort_by_key(subfield_dict)
                for key2 in subfield_dict.keys():
                    subfield_dict[key2] = DictUtils.sort_by_key(subfield_dict[key2])
        else:
            self._result_dict = DictUtils.sort_by_key(self._result_dict)

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides a class for extracting values from XML files and converting them to a JSON file."""

import os

from polymatheia.data.reader import XMLReader
from polymatheia.filter import RecordsFilter
from progress.bar import Bar

from polymatheia_tools.parsing import DatafieldParser
from polymatheia_tools.utils import DictUtils, MainUtils


class ValueExtraction:
    """The :class:`~polymatheia_tools.extraction.ValueExtraction` provides an XML value extraction.

    After creating a new :class:`~polymatheia_tools.extraction.ValueExtraction` the extraction can be started
    by calling the ``start`` function.
    """

    INFOLDER = "polymatheia_files_extracted"
    OUTFILE = "extracted_values.json"
    MERGE_FILE_NAME = "data_corpus.json"
    _BATCH_SIZE = 5000
    _ENCODING = "utf-8"

    def __init__(self, i=INFOLDER, o=OUTFILE, fields=None, subfields=None, ppn_field="003@"):
        """Construct a new :class:`~polymatheia_tools.extraction.ValueExtraction`.

        Parameters are optional. If a parameter is missing, the default class values
        from :class:`~polymatheia_tools.extraction.ValueExtraction` are used.

        Examples for `fields` and `subfields` parameters:

        FIELDS = {
            "044A": ["a"],
            "044K": ["a"]
        }

        SUBFIELDS = {
            "003@": ["0"],
            "044A": ["A", "B", "N", "S", "a", "b", "c", "d", "e", "f", "g", "h", "k", "l", "n", "p", "q", "s", "t", "v",
                     "x", "y", "z"],
            "044K": ["2", "3", "6", "7", "9", "A", "C", "D", "E", "F", "G", "L", "M", "N", "P", "V", "W", "Y", "Z", "a",
                     "c", "f", "g", "n", "p", "w", "x", "z"]
        }

        :param i: Path to input folder that contains XML files
        :type i: ``str``
        :param o: Path to output JSON file
        :type o: ``str``
        :param fields: Fields to extract
        :type fields: ``dict``
        :param subfields: Subfields to extract
        :type subfields: ``dict``
        :param ppn_field: Field with PPN identifier
        :type ppn_field: ``str``
        """
        reader = XMLReader(i)
        fltr = ('true',)
        self._all_records = RecordsFilter(reader, fltr)
        self._nr_records = len(next(os.walk(i))[2])
        self._output_file = o
        self._result_dict = {}
        self._fields = fields
        self._subfields = subfields
        self._ppn_field = ppn_field

    def start(self):
        """Start the extraction process."""
        with Bar("Progress: ", max=self._nr_records) as progressbar:
            for i, record in enumerate(self._all_records):
                if i % ValueExtraction._BATCH_SIZE == 0 and i != 0:
                    DictUtils.save_to_json(self._result_dict, self._output_file + "_" + str(i) + ".json")
                    self._result_dict = {}

                datafields = record.zs_recordData['infosrwschema5picaXML-v1.0record'].datafield
                self._parse_record(datafields, self._fields, self._subfields)
                progressbar.next()

        DictUtils.save_to_json(self._result_dict, self._output_file + "_" + str(self._nr_records) + ".json")

    def _parse_record(self, datafields, fields, subfields):
        """Parse a single record from an XML file.

        :param datafields: Datafields in a single record
        :type datafields: ``object``
        :param fields: Fields
        :type fields: ``dict``
        :param subfields: Subfields for each field
        :type subfields: ``dict``
        """
        data = MainUtils.convert_to_list(datafields)

        # Get record identifier and add as key to result dictionary
        ppn = ValueExtraction._get_ppn(data, subfields, self._ppn_field)
        self._result_dict[ppn] = {}

        # Fill result dictionary with selected values from parsed XML file
        for field in data:
            tag, values = DatafieldParser.parse(field)
            if tag in fields.keys():
                if tag not in self._result_dict[ppn].keys():
                    self._result_dict[ppn][tag] = {}
                for i in values:
                    if i[0] in fields[tag]:
                        if i[0] not in self._result_dict[ppn][tag].keys():
                            self._result_dict[ppn][tag][i[0]] = [i[1]]
                        else:
                            self._result_dict[ppn][tag][i[0]].append(i[1])

        self._result_dict = DictUtils.remove_empty_entries(self._result_dict)

    @staticmethod
    def merge(p, o=MERGE_FILE_NAME):
        """Merge dictionaries in a folder into a single file.

        :param p: Path to folder with dictionaries
        :type p: ``str``
        :param o: Name of result file with merges dictionaries.
        :type o: ``str``
        """
        merge_file = os.path.join(p, o)
        previous_file = None

        if os.path.exists(merge_file):
            os.remove(merge_file)

        for file in os.listdir(p):
            if previous_file:
                d1 = DictUtils.read_from_json(os.path.join(p, previous_file))
                d2 = DictUtils.read_from_json(os.path.join(p, file))
                merged = DictUtils.merge(d1, d2)
                DictUtils.save_to_json(merged, merge_file)
                previous_file = o
            else:
                d1 = DictUtils.read_from_json(os.path.join(p, file))
                merged = DictUtils.merge(d1, {})
                DictUtils.save_to_json(merged, merge_file)
                previous_file = file

    @staticmethod
    def _get_ppn(data, subfields, ppn_field):
        """Extract PPN identifier from a record.

        :param data: Datafields in this record
        :type data: ``list``
        :param subfields: Subfields from configuration file
        :type subfields: ``dict``
        :param ppn_field: Field with PPN identifier
        :type ppn_field: ``str``
        :return: PPN identifier, if available, else None
        :rtype: ``str``
        """
        for field in data:
            tag, values = DatafieldParser.parse(field)
            if tag == ppn_field:
                for i in values:
                    if i[0] in subfields[tag]:
                        return i[1]
                else:
                    continue
        return None

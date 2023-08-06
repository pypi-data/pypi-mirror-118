# !/usr/bin/python
# -*- coding: utf-8 -*-

"""This module provides a class for parsing data."""

from polymatheia.data import NavigableDict

from polymatheia_tools.utils import MainUtils


class DatafieldParser:
    """The :class:`~polymatheia_tools.parsing.DatafieldParser` provides a parsing function for datafields."""

    @staticmethod
    def parse(field, code_only=False):
        """Parse subfield codes and values from a given field.

        :param field: A datafield from a record
        :type field: ``dict``
        :param code_only: If only subfield codes should be returned
        :type code_only: ``bool``
        :return: Tag for this datafield and values/codes of subfields
        :rtype: ``str``, ``list``
        """
        # Type hints
        field: NavigableDict

        tag = field["_attrib"].tag["_text"]
        values = []

        try:
            subfields = MainUtils.convert_to_list(field.subfield)
            for subfield in subfields:
                if code_only:
                    v = subfield["_attrib"].code["_text"].strip()
                else:
                    v = (subfield["_attrib"].code["_text"].strip(), subfield["_text"]["_text"].strip())
                values.append(v)
        except KeyError:
            values.append(None)

        return tag, values

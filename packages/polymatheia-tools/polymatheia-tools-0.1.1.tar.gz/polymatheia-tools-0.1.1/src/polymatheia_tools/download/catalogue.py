#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Custom dictionary used for representing library catalogue keys."""

NAME = "name"
KEYS = "catalogue_keys"
NOTATIONS = "notations"


class CatalogueKeyDict(dict):
    """Class representing library catalogue keys."""

    def __init__(self, *args, **kwargs):
        """Create object of :class:`~polymatheia_tools.download.catalogue.CatalogueKeyDict`."""
        super(CatalogueKeyDict, self).__init__(*args, **kwargs)
        self.__dict__ = {
            KEYS: kwargs[KEYS],
            NOTATIONS: kwargs[NOTATIONS],
            NAME: kwargs[NAME]
        }

    def __str__(self):
        """Get string representation of instances."""
        return f"{self.__dict__[NAME]}: {self.__dict__[KEYS]} -- {self.__dict__[NOTATIONS]}"

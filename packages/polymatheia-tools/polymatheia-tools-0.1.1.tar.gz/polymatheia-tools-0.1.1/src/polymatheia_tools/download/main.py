#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Docstring."""

from loguru import logger

from polymatheia_tools.download.config import LOGGING_FILENAME, LOGGING_FORMAT, DEFAULT_OUTPUT_PATH, \
    DEFAULT_SCHEMA, DEFAULT_FILE_FORMAT
from polymatheia_tools.download.sru_call import SRUCall, PPNCall, CustomCall
from polymatheia_tools.download import common


def schemas(api):
    """Get available schemas for an API."""
    explain = SRUCall.explain(api)
    for s in explain["schemas"]:
        print(s[0], "-", s[1])


def keys(api):
    """Get available catalogue keys for an API."""
    print(SRUCall.keys(api))


def main(api, ppn=False, custom_query=False, i=None, f=DEFAULT_FILE_FORMAT, s=DEFAULT_SCHEMA, o=DEFAULT_OUTPUT_PATH,
         query=None):
    """Start exporting SRU data."""
    # set up logging
    logger.remove()
    logger.add(LOGGING_FILENAME, format=LOGGING_FORMAT, level="DEBUG")

    common.check_args_main(ppn, i)

    print(f"INFO: Output file format is set to {f}.")
    print(f"INFO: Schema is set to {s}.")
    print(f"INFO: Records will be saved to {o}.")
    print(f"INFO: API is {api}.")

    # set config dict
    config = {"api": api,
              "query": None,
              "max_records": 1,
              "schema": s,
              "export_path": o}

    if ppn:
        PPNCall.start(i, f, config, custom_query)
    else:
        CustomCall.start(api, f, query, config)

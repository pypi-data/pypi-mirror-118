#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Class for common utils."""


def check_args_main(ppn, ppn_file):
    """Check command line arguments for validity."""
    if ppn and not ppn_file:
        raise FileNotFoundError("No file name specified for PPN list!")
    elif ppn and ppn_file:
        print(f"INFO: File {ppn_file} will be used.")
    if not ppn and ppn_file:
        print("INFO: Argument --file will be ignored because the --ppn flag is set to False.")
    if not ppn:
        print("INFO: Use configuration from ./config/custom.py")

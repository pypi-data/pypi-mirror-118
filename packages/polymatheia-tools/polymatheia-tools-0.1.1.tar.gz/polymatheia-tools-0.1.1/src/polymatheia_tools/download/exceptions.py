#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Docstring."""

from loguru import logger


class EmptyError(Exception):
    """Data is empty and cannot be processed."""

    def __init__(self):
        """Docstring."""
        logger.error("Data is empty and cannot be processed.")

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Class for query utils."""

from loguru import logger

from polymatheia_tools.download.catalogue import KEYS, NOTATIONS
from polymatheia_tools.download.config import BOOLEAN_AND
from polymatheia_tools.download.exceptions import EmptyError


def create(api, catalogue_keys, boolean=BOOLEAN_AND):
    """Create a CQL query from a list of classification dicts.

    :param api: SRU endpoint
    :type api: ``str``
    :param catalogue_keys: List of :class:`~polymatheia_tools.download.catalogue.CatalogueKeyDict`
    :type catalogue_keys: ``list``
    :param boolean: Boolean operator
    :type boolean: ``str``
    """
    q = []

    for c in catalogue_keys:
        for k in c[KEYS]:
            # if not k.split(".")[1].upper() in SRUCall.explain(api)["keys"]:
            #     raise ValueError(f"{k} is not a valid search key for this SRU endpoint!")
            for n in c[NOTATIONS]:
                q.append("=".join((k, n)))

    q = f" {boolean} ".join(q)
    logger.info(f"Query: {q}")

    return q if len(q) > 0 else EmptyError()


def create_custom(catalogue_keys, boolean=BOOLEAN_AND):
    """
    """
    q = []

    for c in catalogue_keys:
        for n in c[NOTATIONS]:
            query = "pica.1049=" + n
            q.append(query)
    q.append("pica.1045=rel-tt")
    q.append("pica.1001=b")

    q = f" {boolean} ".join(q)
    logger.info(f"Query: {q}")

    return q if len(q) > 0 else EmptyError()

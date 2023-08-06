#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Docstring."""

import os
import re

from hashlib import sha256
from loguru import logger
from lxml import etree
from polymatheia.data.reader import SRUExplainRecordReader, SRURecordReader
from polymatheia.data.writer import JSONWriter, CSVWriter, XMLWriter
from progress.bar import Bar

from polymatheia_tools.download.catalogue import CatalogueKeyDict
from polymatheia_tools.download.config import BOOLEAN_OR, DEFAULT_PPN_INPUT_PATH
from polymatheia_tools.download import query


class SRUCall:
    """A class for calling an SRU web service and handling the responses."""

    def __init__(self, config):
        """Initialize class object."""
        self.api = config["api"]
        self.query = config["query"]
        self.max_records = config["max_records"]
        self.schema = config["schema"]
        self.export_path = config["export_path"]
        self.reader = SRURecordReader(self.api,
                                      query=self.query,
                                      max_records=self.max_records,
                                      record_schema=self.schema
                                      )

    @staticmethod
    def explain(api):
        """Get explain record information."""
        reader = SRUExplainRecordReader(api)
        keys = []
        names = []
        for r in reader:
            try:
                for index in r.explain.indexInfo.index:
                    keys.append(index.title.split(" ", 1)[0].split("[")[1].split("]")[0])
                    names.append(index.title.split(" ", 1)[1])
            except Exception:
                pass
        return {"record": [r for r in reader],
                "echo": reader.echo,
                "schemas": reader.schemas,
                "keys": keys,
                "names": names}

    @staticmethod
    def keys(api):
        """Get a human-readable list of all keys that can be used with this SRU endpoint."""
        keys = []
        explain = SRUCall.explain(api)
        for i, k in enumerate(explain["keys"]):
            keys.append(k + " " + explain["names"][i])

        return "\n".join(keys)

    @staticmethod
    def get_total_number(config):
        """Get total number of results for a query."""
        return SRURecordReader.result_count(config["api"], query=config["query"])

    def show(self, max_nr):
        """Show sample of the SRU export."""
        count = 0
        for record in self.reader:
            if count < max_nr:
                print(record)
                count += 1
            else:
                break

    def save_custom(self, fileformat, total, ppn=None):
        """Save data to disk."""
        if fileformat.lower() == "xml":
            w = XMLWriter(self.export_path, "")
        elif fileformat.lower() == "json":
            w = JSONWriter(self.export_path, "")
        elif fileformat.lower() == "csv":
            w = CSVWriter(self.export_path, "")
        else:
            raise ValueError("Wrong fileformat parameter!")

        # TODO: only XML is supported at the moment
        with Bar("Progress: ", max=total) as progressbar:
            for identifier, record in enumerate(self.reader):
                try:
                    hash = sha256(str(identifier).encode('utf-8'))
                    hex = hash.hexdigest()
                    if not ppn:
                        ppn = str(identifier)
                    file_path = os.path.join(
                        self.export_path + ppn,
                        *[hex[idx:idx + 4] for idx in range(0, len(hex), 4)],
                        hex)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(f'{file_path}.xml', 'wb') as out_f:
                        root = etree.Element('record')
                        _build_xml_doc(root, record)
                        out_f.write(etree.tostring(root))

                    progressbar.next()
                except:
                    logger.debug(f"Datensatz {record} kann nicht verarbeitet werden.")

            progressbar.next()

    def save_ppn(self, ident, fileformat):
        """Save data to disk."""
        if fileformat.lower() == "xml":
            w = XMLWriter(self.export_path, "")
        elif fileformat.lower() == "json":
            w = JSONWriter(self.export_path, "")
        elif fileformat.lower() == "csv":
            w = CSVWriter(self.export_path, "")
        else:
            raise ValueError("Wrong fileformat parameter!")

        # TODO: only XML is supported at the moment
        try:
            for record in self.reader:
                if isinstance(ident, list):
                    identifier = record.get(ident)
                else:
                    identifier = ident
                if identifier:
                    hash = sha256(identifier.encode('utf-8'))
                    hex = hash.hexdigest()
                    file_path = os.path.join(
                        self.export_path,
                        *[hex[idx:idx + 4] for idx in range(0, len(hex), 4)],
                        hex)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(f'{file_path}.xml', 'wb') as out_f:
                        root = etree.Element('record')
                        _build_xml_doc(root, record)
                        out_f.write(etree.tostring(root))
        except:
            logger.debug(f"Datensatz {ident} kann nicht verarbeitet werden.")


def _build_xml_doc(parent, data):
    """Build the XML document tree.

    Tag names are generated from the keys in the ``data``, ensuring that they are valid XML tag names.

    Handles nested ``data`` trees by nesting elements and lists by generating the same tag repeatedly.

    :param parent: The parent node to attach elements to
    :type parent: :class:`~lxml.etree.Element`
    :param data: The data to build the tree from
    :type data: :class:`~polymatheia.data.NavigableDict`
    """
    for key, value in data.items():
        if isinstance(value, list):
            for sub_value in value:
                element = etree.Element(_valid_xml_tag(key))
                if isinstance(sub_value, dict):
                    _build_xml_doc(element, sub_value)
                else:
                    element.text = str(value)
                parent.append(element)
        elif isinstance(value, dict):
            element = etree.Element(_valid_xml_tag(key))
            _build_xml_doc(element, value)
            parent.append(element)
        else:
            element = etree.Element(_valid_xml_tag(key))
            element.text = str(value)
            parent.append(element)


def _valid_xml_tag(tag):
    """Generate a valid XML tag for the given ``tag``.

    :param tag: The tag to generate a valid XML tag for
    :type tag: ``str``
    :return: A valid XML tag
    :rtype: ``str``
    """
    tag = re.sub(r'\s+', '-', tag)
    tag = ''.join(re.findall(r'\w|\d|-|_|\.', tag))
    while not re.match(r'\w', tag) or re.match(r'\d', tag):
        tag = tag[1:]
    if tag.lower().startswith('xml'):
        tag = tag[3:]
    return tag


class PPNCall:
    """A class for PPN calls to an SRU endpoint."""

    @staticmethod
    def start(ppn_file, fileformat, config, custom_query, count_only=False):
        """Execute SRU retrieval with PPN list."""
        if "/" not in ppn_file:  # file name is not a path, set to default path
            ppn_file = os.path.join(DEFAULT_PPN_INPUT_PATH, ppn_file)

        # read PPN list
        with open(ppn_file, "r", encoding="utf-8") as f:
            _ppn_list = f.readlines()
        _ppn_list = [x.strip() for x in _ppn_list]

        # create CatalogueKeyDict object for each PPN
        catalogue_keys = [CatalogueKeyDict(name="PPN",
                                           catalogue_keys=["pica.ppn"],
                                           notations=[_nr]) for _nr in _ppn_list]

        # create query for each PPN
        if not custom_query:  # custom query
            queries = [query.create(config["api"], [_k]) for _k in catalogue_keys]
        else:
            queries = [query.create_custom([_k]) for _k in catalogue_keys]

        # call SRU
        amount = dict()
        with Bar("Progress: ", max=len(catalogue_keys)) as progressbar:
            for q in queries:
                config["query"] = q

                # get PPN
                record_id = q.split("=")[1]

                # get total number of retrieved records
                total = SRUCall.get_total_number(config)
                config["max_records"] = total
                if count_only:
                    _tmp = q.split("=")[1]
                    ppn = _tmp.split(" ")[0]
                    amount[ppn] = total
                    progressbar.next()
                    continue
                logger.info(f"Total number of records: {total}")
                # TODO: If total != 1, the PPN is probably invalid!

                # execute and save SRU
                sru = SRUCall(config)
                if not custom_query:
                    sru.save_ppn(record_id, fileformat=fileformat)
                else:
                    _tmp = q.split("=")[1]
                    ppn = _tmp.split(" ")[0]
                    if total > 0:
                        logger.info(f"Processing PPN {ppn}")
                        sru.save_custom(fileformat=fileformat, total=total, ppn=ppn)
                    else:
                        logger.info(f" {config['query']} has zero results")
                progressbar.next()
        if count_only:
            return amount


class CustomCall:
    """A class for SRU calls that are using catalogue keys."""

    @staticmethod
    def start(api, fileformat, q, config):
        """Execute SRU retrieval with catalogue keys."""
        # set query
        config["query"] = query.create(api, q, boolean=BOOLEAN_OR)

        # set total number of retrieved records
        total = SRUCall.get_total_number(config)
        config["max_records"] = total
        logger.info(f"Total number of records: {total}")

        # call SRU
        sru = SRUCall(config)
        # sru.show(1)
        sru.save_custom(fileformat=fileformat, total=total)

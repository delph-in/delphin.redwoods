# -*- coding: utf-8 -*-
"""
PyDelphin Plugin for Redwoods LinGO Treebank

- ``TreebankException``: ``PydelphinException`` occuring processing Treebank.

- ``TreebankResponce``: ``Response`` with metadata.

- ``Metadata``: list of metadata about ERG tagged release.

- ``Treebank``: Treebank wrapper.
  - ``description()``: metada about current testsuites and partitions
  - ``upload(testsuite: str)``: add testuite to current bundle
  - ``remove(testuite:str) ``: remove testuite from current bundle
  - ``get(testsuite: str)``: make ``TreebankResponce`` for given testsuite.
  - ``get_all(): make ``TreebankResponce`` for all included testsuites.
"""

import os
import csv
from typing import List, Dict
from pprint import pprint
from glob import glob

from svn.remote import RemoteClient

from delphin.interface import Response
from delphin.itsdb import TestSuite
from delphin.exceptions import PyDelphinException


class TreebankException(PyDelphinException):
    """Treebank Processing Exception"""


class TreebankResponse(Response):
    """ ``Response`` with metadata """

    def __init__(self):
        super()
        self["results"] = []
        self["metadata"] = []


class Metadata(List):
    """
    Redwoods metadata information. Supported ERG tagged versions:
    - 1214, 2018

    Parameters
    ----------
    tag: int, default ``1214``
        ERG tagged version of Redwoods
    """

    def __init__(self, tag=1214):
        super()
        TAGS = [1214, 2018]

        if tag not in TAGS:
            msg = '{} not in list of valid tags: {}'.format(tag, TAGS)
            raise TreebankException(msg)

        path = "./delphin/data/{}.csv".format(tag)

        with open(path) as f:
            reader = csv.reader(f, delimiter=',')
            for idx, row in enumerate(reader):
                if idx == 0:
                    schema = row
                else:
                    e = dict(zip(schema, row))
                    self.append(e)


class Treebank(object):
    """
    Treebank: a bundle for a Redwoods testsuite profiles

    Parameters
    ----------
    name: str
        name of the testsuite or partition to be uploaded
    path: str, default ``~/redwoods<TAG>``
        path to tsdb, by default retrieves to home directory
    use_logon: bool, default ``True``
        if ``True`` used testsuites from logon environment
    tag: int, default ``1214``
        version of ERG tagged version to use.
    """

    def __init__(self,
                 name: str,
                 path: str = None,
                 use_logon: bool = True,
                 tag: int = 1214):

        self.metatada = Metadata(tag)

        if path is None:

            logon_path = os.environ.get('LOGONROOT')
            default_path = os.path.expanduser("~") + "/redwoods"+str(tag)

            if use_logon and logon_path:
                self._path = logon_path + "/lingo/erg/tsdb/gold"

            elif os.path.exists(default_path):
                self._path = default_path

            else:
                self._path = default_path

                print("checking out Redwoods to {}".format(self._path))

                url = 'svn.delph-in.net/erg/tags/{}/tsdb/gold/'.format(tag)
                cli = RemoteClient(url)
                cli.checkout(self._path)
        else:
            if os.path.isdir(path):
                self._path = path
            else:
                raise TreebankException("{} does not exits".format(path))

        self._testsuites = {}

        self.upload(name)

    def __contains__(self, key):
        return key in self._testsuites

    def __getitem__(self, key):
        return self._testsuites[key]

    def __iter__(self):
        return iter(self._testsuites)

    def __len__(self):
        return len(self._testsuites)

    def description(self):
        """
        Metadata information about Testsuites in Treebankt
        """

        data = [e for e in self.metatada if e['name']
                in self._testsuites.keys()]

        pprint(data)

    def upload(self, name: str):
        """
        Upload testsuite or partition

        Parameters
        ----------
        name: str
            name of the testsuite or their bundle to be uploaded
        """

        testsuites = self._collect(name)

        for ts in testsuites:

            path = "{}/{}".format(self._path, ts)
            paths = glob(path + '*')
            paths = [p for p in paths if not os.path.exists(p+'/virtual')]
            if len(paths) != 0:
                self._testsuites[ts] = path

            else:
                raise TreebankException("No testsuite {} ".format(path))

    def remove(self, name: str):
        """
        Remove testsuite or partition

        Parameters
        ----------
        name: str
            name of the testsuite or partition to be removed
        """

        testsuites = self._collect(name)

        for ts in testsuites:
            del self._testsuites[ts]

    def _collect(self, name: str) -> List[str]:

        names = [e['name'] for e in self.metatada]
        partitions = set(["{}.{}".format(e['description'], e['split'])
                         for e in self.metatada])

        if name in names:

            return [name]

        elif name in partitions:

            d, s = name.split(".")

            testsuites = [e['name'] for e in self.metatada if
                          d == e['description'] and s == e['split']]

            return testsuites

        else:
            msg = "not a valid testsuite or partition"
            raise TreebankException(msg)

    def get(self, name: str) -> TreebankResponse:

        testsuites = self._collect(name)

        response = TreebankResponse()

        for ts in testsuites:

            response["results"].append(self._make_result(ts))
            response["metadata"].append(self._make_metadata(ts))

        return response

    def get_all(self) -> TreebankResponse:

        responses = []

        for ts in self._testsuites:

            responses.append(self.get(ts))

        response = TreebankResponse()

        for key in responses[0].keys():

            response[key] = [ress[key] for ress in responses]

        return response

    def _make_result(self, name: str) -> List[str]:

        # Get all testsuites matching the name path
        # Required for treating virtual testsuites

        paths = glob(self._testsuites[name] + "*")
        paths = [p for p in paths if not os.path.exists(p+'/virtual')]

        tables = [TestSuite(path)["result"] for path in paths]

        result = []

        for table in tables:

            for record in table:

                result.append({
                    'surface': record['surface'],
                    'mrs': record['mrs'],
                    'derivation': record['derivation'],
                    'tree': record['tree']})

        return result

    def _make_metadata(self, name: str) -> Dict:

        names = [e['name'] for e in self.metatada]

        if name in names:
            data = [e for e in self.metatada if name == e['name']]

            if len(data) == 1:
                return data[0]
            else:
                msg = "expected 1, but got {} instances".format(len(data))
                TreebankException(msg)

        else:
            TreebankException("{} not found in redwoods".format(name))

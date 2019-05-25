"""
PyDelphin Plugin as an interface tin LinGO Redwoods Treebank
"""
import os
from typing import List
from enum import Enum, auto
from svn.remote import RemoteClient as cli

from delphin.interface import Response
from delphin.itsdb import TestSuite
from delphin.exceptions import PyDelphinException

# Redwoods Portions by split.
# See http://svn.delph-in.net/erg/tags/1214/etc/redwoods.xls

TRAIN = [
    "csli", "esd", "fracas", "mrs", "trec", "ecoc", "ecos", "hike", "jh0",
    "jh1", "jh2", "jh3", "jh4", "tg1", "ps", "rtc000", "rtc001", "sc01",
    "sc02", "sc03", "vm6", "vm13", "vm31", "ws01", "ws02", "ws03", "ws04",
    "ws05", "ws06", "ws07", "ws08", "ws09", "ws10", "ws11", "peted", "wsj00a",
    "wsj00b", "wsj00c", "wsj00d", "wsj01a", "wsj01b", "wsj01c", "wsj01d",
    "wsj02a", "wsj02b", "wsj02c", "wsj02d", "wsj03a", "wsj03b", "wsj03c",
    "wsj04a", "wsj04b", "wsj04c", "wsj04d", "wsj04e", "wsj05a", "wsj05b",
    "wsj05c", "wsj05d", "wsj05e", "wsj06a", "wsj06b", "wsj06c", "wsj06d",
    "wsj07a", "wsj07b", "wsj07c", "wsj07d", "wsj07e", "wsj08a", "wsj09a",
    "wsj09b", "wsj09c", "wsj09d", "wsj09e", "wsj10a", "wsj10b", "wsj10c",
    "wsj10d", "wsj11a", "wsj11b", "wsj11c", "wsj11d", "wsj11e", "wsj12a",
    "wsj12b", "wsj12c", "wsj12d", "wsj12e", "wsj13a", "wsj13b", "wsj13c",
    "wsj13d", "wsj13e", "wsj14a", "wsj14b", "wsj14c", "wsj14d", "wsj14e",
    "wsj15a", "wsj15b", "wsj15c", "wsj15d", "wsj15e", "wsj16a", "wsj16b",
    "wsj16c", "wsj16d", "wsj16e", "wsj16f", "wsj17a", "wsj17b", "wsj17c",
    "wsj17d", "wsj18a", "wsj18b", "wsj18c", "wsj18d", "wsj18e", "wsj19a",
    "wsj19b", "wsj19c", "wsj19d",
]

DEV = [
    "ecpa", "jh5", "tg2", "ws12", "wsj20a",
    "wsj20b", "wsj20c", "wsj20d", "wsj20e",
]

TEST = [
    "ecpr", "jhk", "jhu", "tgk", "tgu", "psk", "psu", "rondane", "cf04",
    "cf06", "cf10", "cf21", "cg07", "cg11", "cg21", "cg25", "cg32", "cg35",
    "ck11", "ck17", "cl05", "cl14", "cm04", "cn03", "cn10", "cp15", "cp26",
    "cr09", "vm32", "ws13", "ws214", "petet", "wsj21a", "wsj21b", "wsj21c",
    "wsj21d",
]


class RedwoodsError(PyDelphinException):
    """Exception when processing Redwoods"""


class Partition(Enum):
    TRAIN = auto()
    DEV = auto()
    TEST = auto()


class RedwoodsResponse(Response):
    "Wrapper for extra fields include to Response"

    def __init__(self):
        super()
        self["results"] = []
        self["partitions"] = []
        self["ids"] = []

    def partitions(self) -> List[Partition]:

        return [partition for partition in self.get('partition', [])]

    def partition(self, i) -> Partition:

        return self.get('partition', [])[i]

    def ids(self) -> List[str]:

        return [id for id in self.get('id', [])]

    def id(self, i) -> str:

        return self.get('id', [])[i]


class Redwoods:

    def __init__(self, testsuite: str, path: str = None):

        if path is None:

            logon_path = os.environ.get('LOGONROOT')
            default_path = os.path.expanduser("~") + "/redwoods"

            if logon_path:
                self._path = logon_path + "/lingo/erg/tsdb/gold"

            elif os.path.exists(default_path):
                self._path = default_path

            else:
                print('No path found, checking out Redwoods to '+default_path)

                # TODO currrent  trunk does not have full Redwoods.
                # Use latest tagged version
                rep = cli("http://svn.delph-in.net/erg/tags/1214/tsdb/gold/")
                rep.checkout(default_path)

                self._path = default_path

        else:
            self._path = path

        self._testsuites = {}

        self.upload(testsuite)

    def __contains__(self, key):
        return key in self._testsuites

    def __getitem__(self, key):
        return TestSuite(self._testsuites[key])

    def __iter__(self):
        return iter(self._testsuites)

    def __len__(self):
        return len(self._testsuites)

    def upload(self, testsuite: str):

        testsuites = self._collect_testsuites(testsuite)

        for testsuite in testsuites:

            testsuite_path = "{}/{}".format(self._path, testsuite)

        if os.path.exists(testsuite_path):
            self._testsuites[testsuite] = testsuite_path

        else:
            raise RedwoodsError("No testsuite {} ".format(testsuite_path))

    def remove(self, testsuite: str):

        testsuites = self._collect_testsuites(testsuite)

        for testsuite in testsuites:
            del self._testsuites[testsuite]

    def reload(self, testsuite: str):

        self._testsuites = {}

        self.upload(testsuite)

    def _collect_testsuites(self, testsuite: str) -> List[str]:

        "support for special groups of testsuites"
        # TODO add all the standard named partitions

        if testsuite == "deepbank-train":
            return list(filter(lambda x: "wsj" in x, TRAIN))

        elif testsuite == "deepbank-dev":
            return list(filter(lambda x: "wsj" in x, DEV))

        elif testsuite == "deepbank-test":
            return list(filter(lambda x: "wsj" in x, TEST))

        elif testsuite == "deepbank":
            return list(filter(lambda x: "wsj" in x, TRAIN+DEV+TEST))

        elif testsuite == "redwoods":
            return TRAIN+DEV+TEST

        else:
            return [testsuite]

    def get(self, testsuite: str) -> RedwoodsResponse:

        testsuites = self._collect_testsuites(testsuite)

        response = RedwoodsResponse()

        for testsuite in testsuites:

            response["results"].append(self._make_result(testsuite))
            response["partitions"].append(self._make_partitions(testsuite))
            response["ids"].append(self._make_ids(testsuite))

        return response

    def get_all(self) -> RedwoodsResponse:

        responses = []

        for testsuite in self._testsuites:

            responses.append(self.get(testsuite))

        join_response = RedwoodsResponse()

        for key in responses[0].keys():

            join_response[key] = [response[key] for response in responses]

        return join_response

    def _make_result(self, testsuite: str) -> List[str]:

        table = TestSuite(self._testsuites[testsuite])["result"]
        result = []

        for record in table:

            result.append({
                'surface': record['surface'],
                'mrs': record['mrs'],
                'derivation': record['derivation'],
                'tree': record['tree']})

        return result

    def _make_partitions(self, testsuite: str) -> List[Partition]:

        size = len(TestSuite(self._testsuites[testsuite])["result"])

        if testsuite in TRAIN:
            return size*[Partition.TRAIN]

        elif testsuite in DEV:
            return size*[Partition.DEV]

        elif testsuite in TEST:
            return size*[Partition.TEST]

        else:
            redwoods = TRAIN+DEV+TEST
            msg = "Testsuite {} not in Redwoods:{}".format(testsuite, redwoods)
            raise RedwoodsError(msg)

    def _make_ids(self, testsuite: str) -> List[str]:

        table = TestSuite(self._testsuites[testsuite])["parse"]
        ids = []

        for record in table:

            ids.append(testsuite + ':' + record['i-id'])

        return ids

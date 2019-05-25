import os
from redwoods import Redwoods
from delphin.itsdb import TestSuite

default_path = os.path.expanduser("~") + "/redwoods"

def test_init_with_path():

    instance = Redwoods(["wsj00a"], default_path)
    assert str(instance["wsj00a"]._path) == default_path + "/wsj00a"

def test_init_without_path():

    instance = Redwoods(["wsj00a"])
    assert str(instance["wsj00a"]._path) == default_path + "/wsj00a"

def test_upload():
    
    instance = Redwoods(["wsj00a"], default_path)
    instance.upload("wsj00b")
    assert str(instance["wsj00a"]._path) == default_path + "/wsj00a"
    assert str(instance["wsj00b"]._path) == default_path + "/wsj00b"


def test_remove():

    instance = Redwoods(["wsj00a", "wsj00b"], default_path)
    instance.remove("wsj00b")

    assert str(instance["wsj00a"]._path) == default_path + "/wsj00a"
    assert not "wsj00b" in instance

def test_reload():

    instance = Redwoods(["wsj00a"], default_path)
    instance.reload(["wsj00b"])
    assert str(instance["wsj00b"]._path) == default_path + "/wsj00b"
    assert not "wsj00a" in instance

def test_get():

    instance = Redwoods(["wsj00a"], default_path)
    response = instance.get("wsj00a")

    assert "results" in response
    assert "partitions" in response
    assert "ids" in response

def test_get_all():

    instance = Redwoods(["wsj00a"], default_path)
    response = instance.get("wsj00a")

    assert "results" in response
    assert "partitions" in response
    assert "ids" in response



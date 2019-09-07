import os

from delphin.redwoods import Treebank

default_path = os.path.expanduser("~") + "/redwoods"

def test_init_with_path():

    instance = Treebank("wsj00", default_path)
    assert str(instance["wsj00"]) == default_path + "/wsj00"

def test_init_without_path():

    instance = Treebank("wsj00")
    assert str(instance["wsj00"]) == default_path + "/wsj00"

def test_upload():
    
    instance = Treebank("wsj00", default_path)
    instance.upload("wsj01")
    assert str(instance["wsj00"]) == default_path + "/wsj00"
    assert str(instance["wsj01"]) == default_path + "/wsj01"


def test_remove():

    instance = Treebank("wsj00", default_path)
    instance.upload("wsj01")
    instance.remove("wsj01")

    assert str(instance["wsj00"]) == default_path + "/wsj00"
    assert not "wsj00b" in instance

def test_get():

    instance = Treebank("wsj00", default_path)
    response = instance.get("wsj00")

    assert "results" in response
    assert "metadata" in response


def test_get_all():

    instance = Treebank("wsj00", default_path)
    response = instance.get("wsj00")

    assert "results" in response
    assert "metadata" in response

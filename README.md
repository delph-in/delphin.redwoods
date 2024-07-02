# delphin.redwoods

[Pydelphin](https://github.com/delph-in/pydelphin) plugin for the LinGO Redwoods Treebank

## Installation

```bash
pip install delphin.redwoods
```

requirements:
- ``pydelphin >= 1.0.0``
- ``svn >= 0.3.46``

## Usage 

``Treebank`` class that acts as a bundle, grouping testsuites of interest

```python
from delphin.redwoods import Treebank
```
Redwoods data can be retrieved from 3 sources:

- User specified path to gold parse

```python
profile = Treebank("wsj00a", "path/to/gold/")
```

- If environment ``$LOGONROOT`` is setup, use its remote copy of Redwoods

```python
profile = Treebank("wsj00a")
```

- retreave [svn repository](http://svn.delph-in.net/erg/tags/<TAG>/tsdb/gold) to ``~/redwoods<TAG>`` (default option)

```python
profile = Treebank("wsj00a")
```

When retreiving the data you can specified which ``tag`` version to use. Currently supported versions:
- 1214 (default)
- 2018 

User can edit the profiles stored in the bundle:

```python
profile = Treebank("wsj00") # access to profile wsj00
profile.upload("wsj01") # access to profiles wsj00 and wsj01
profile.remove("wsj00") # access to profiles wsj01
```

There exists support to create standard bundle sets of profiles:

```python
deepbank_train = Treebank("deepbank.train") # wsj section 0 - 19
deepbank_dev = Treebank("deepbank.dev") # wsj section 20
deepbank_test = ReTreebankdwoods("deepbank.test") # wsj section 21
```

``TreebankResponse`` can be retrieved for a single profile or all profiles specified in the bundle:

```python
profile.get("wsj00") # ``TreebankResponse`` for Profile wsj00
profile.get_all() # ``TreebankResponse`` for all profiles specified in ``profile``
```

Each ``TreebankResponse`` consists of the following information:
- `metadata` about the the partition, including its description, split, and stats.
- `results` for each sentence the following information is recorded:
  - `surface`: surface form
  - `derivation`: derivation information
  - `tree`: syntactic tree
  - `mrs` : mrs representation
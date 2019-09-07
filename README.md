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

- retreave [svn repository](http://svn.delph-in.net/erg/tags/1214/tsdb/gold) to ``~/redwoods`` (default option)

```python
profile = Treebank("wsj00a")  
```

User can edit the profiles stored in the bundle:

```python
profile.upload("wsj00b") # access to profiles wsj00a and wsj00b
profile.remove("wsj00a") # access to profiles wsj00b
profile.reload("wsjooc") # access to profiles wsj00c
```

Each profile can be interacted with standard ``TestSuite`` inteface:

```python
profile = Treebank("wsj00a")
profile["wsj00a"] # TestSuite stored in path/to/gold/wsj00a  
```

There exists support to create standard bundle sets of profiles:

```python
deepbank_train = Treebank("deepbank-train") # wsj section 0 - 19
deepbank_dev = Treebank("deepbank-dev") # wsj section 20
deepbank_test = ReTreebankdwoods("deepbank-test") # wsj section 21
deepbank = Treebank("deepbank") # wsj section 0 - 21
redwoods = Treebank("redwoods") # retrieves all existing profiles 
```

``TreebankResponse`` can be retrieved for a single profile or all profiles specified in the bundle:

```python
profile.get("wsj00a") # ``TreebankResponse`` for Profile wsj00a
profile.get_all() # ``TreebankResponse`` for all profiles specified in ``profile``
```

Each ``TreebankResponse`` consists of the following information:
- `ids`: unique ids for each sentence in redwoods (format: ``testsuite:i-id``)
- `partitions` identifier of ``TEST``, ``DEV``, or ``TRAIN`` partition for each sentence
- `results` for each sentence the following information is recorded:
  - `surface`: surface form
  - `derivation`: derivation information
  - `tree`: syntactic tree
  - `mrs` : mrs representation

# TODO
- [ ] Add further support for standard bundles
- [ ] Extend ``redwoods_test.py``
- [ ] Add interface to write results to file that can be later processed using ``delphin.codec``.
This includes specification of encoding format.
- [ ] Create release v.0.1.0

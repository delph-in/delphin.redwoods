# delphin.redwoods
PyDelphin interface for the LinGO Redwoods Treebank


## Installation

```bash
pip install delphin.redwoods
```

requirements:
- ``pydelphin >= 1.0.0``
- ``svn >= 0.3.46``

## Usage 

Interface is supported by ``Redwoods`` class that acts as a bundle for specified testsuites of interest. 

```python
from delphin.redwoods import Redwoods
```

Redwoods data can be retrieved from 3 sources:

- User specified path to gold parse

```python
profile = Redwoods("wsj00a", "path/to/gold/")  
```

- If environment ``$LOGONROOT`` is setup, use its remote copy of Redwoods

```python
profile = Redwoods("wsj00a")  
```

- retreave remote repository to ``~/redwoods`` (default option)

```python
profile = Redwoods("wsj00a")  
```

User can mofity the profiles stored in the bundle:

```python
profile.upload("wsj00b") # access to profiles wsj00a and wsj00b
profile.remove("wsj00a") # access to profiles wsj00b
profile.reload("wsjooc") # access to profiles wsj00c
```

Each profile can be interacted with standard ``TestSuite`` inteface:

```python
profile = Redwoods("wsj00a")
profile["wsj00a"] # TestSuite stored in path/to/gold/wsj00a  
```

There exists support to create standard bundle sets of profiles:

```python
deepbank_train = Redwoods("deepbank-train") # wsj section 0 - 19
deepbank_dev = Redwoods("deepbank-dev") # wsj section 20
deepbank_test = Redwoods("deepbank-test") # wsj section 21
deepbank = Redwoods("deepbank") # wsj section 0 - 21
redwoods = Redwoods("redwoods") # retrieves all existing profiles 
```

``RedwoodsResponse`` can be retrieved for a single profile or all profiles specified in the bundle:

```python
profile.get("wsj00a") # ``RedwoodsResponse`` for Profile wsj00a
profile.get_all() # ``RedwoodsResponse`` for all profiles specified in ``profile``
```

Each ``RedwoodsResponse`` consists of the following information:
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

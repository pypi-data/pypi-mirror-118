# Py XH POM Mgmt

A library provide functionality to gather a list of pom.xml by path and collect in to pom list.

# Installation

```shell script
pip install pyXhPomMgmt
```

or

```shell script
pip3 install pyXhPomMgmt
```


# Demo

## As Library

### Scan a list of directory
```python
from ScanDir import scan
from POMREPOS import POMRepos

paths_to_scan = [] # list of paths
repo = POMRepos() # new PomRepos instance or existing PomRepos instance
paths_to_skip = [] # list of key in path to skip e.g. target
scanMultiple(paths_to_scan, repo, paths_to_skip)

# repo will end up contain all dependencies found
```

### Scan a list of directory
```python
from ScanDir import scan
from POMREPOS import POMRepos

paths_to_scan = [] # list of paths
repo = POMRepos() # new PomRepos instance or existing PomRepos instance
paths_to_skip = [] # list of key in path to skip e.g. target
for path in paths_to_scan:
    scan(path, repo, paths_to_skip)

# repo will end up contain all dependencies found
```

## As executable module
```shell

python -m pyXhPomMgmt --pom-paths C:\Users\01731363\Documents --filter abc --skip-path-with target
# all dependencies found will be displayed
```

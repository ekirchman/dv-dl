# dv-dl
A small python download script for downloading datasets from the Dataverse Project

## Installation

1. Clone or download this repo from master
2. Download the requirements
   1. `pip install requirements.txt`

## Setting your API Key

Get an API key using this [reference](https://guides.dataverse.org/en/5.3/api/auth.html)

Create a config file in the same location as dv-dl.py called `dv-dl.conf`. The formate should look like this:

```
[demo.dataverse.org]
API = MY_API_KEY_GOES_HERE
```

Multiple sub headers (instances) can be put in the config file. If not specified in a cli arg, the first instanace is selected

## Usage

```
$ python3 dv-dl.py -h
usage: dv-dl.py [-h] {search,download} ...

A download tool for Dataverse instances

positional arguments:
  {search,download}  sub-command help
    search           Search and download datasets. Defaults to generic query
    download         Download individual datasets

optional arguments:
  -h, --help         show this help message and exit
```

- match - search for datasets and download
- doi - download the dataset matching which matches the given DOI
- URL -  download the dataset matching which matches the given URL [WIP]

## Goal Plans Ideas

- [ ] Be able to download original files (files must be downloaded individually)
- [X] Add default instance
- [ ] ~~config file only requires API if needed~~ *might not be possible*
- [ ] Group command line arguments
- [ ] Check file MD5sum when doing individual downloads
- [ ] More robust search features
- [ ] save location
- [ ] Options for wget or pydataverse downloads
- [ ] TUI/GUI
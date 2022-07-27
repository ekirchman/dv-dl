# dv-dl
A small python download script for downloading datasets from the Dataverse Project

## Installation

1. Clone or download this repo from master
2. Download the requirements
   1. `pip install requirements.txt`

## Setting your API Key

Create a `.api_key` file in the same directory as the dv-dl.py and paste in your API key from the site you are searching. More documentation about where to get an API key and how it works can be found [here](https://guides.dataverse.org/en/5.11/api/intro.html#what-is-an-api)

## Usage

`python3 dv-dl.py`

match - search for datasets and download
doi - download the dataset matching which matches the given DOI
URL -  download the dataset matching which matches the given URL

## Goal Plans Ideas

- [ ] Be able to download original files (files must be downloaded individually)
- [ ] Check file MD5sum when doing individual downloads
- [ ] More robust search features
- [ ] save location
- [ ] Options for wget or pydataverse downloads
- [ ] TUI/GUI
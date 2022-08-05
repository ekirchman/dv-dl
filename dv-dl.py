#!/usr/bin/env python3
import requests
import json
import pprint
import os
import re
import sys #sys.exit()
import zipfile
import argparse
import configparser

# default values 
unzip = False
debug = True

class dvinstance:
    def __init__(self, name, api, ):
        self.name = name
        self.api = api

# Read in API Key per dataverse instance
# API_req specifies if an API is required to be in the config or not
def read_conf(instance_name = "", API_req = True):

    #TODO check all options and make sure a config file is not required
    #read conf if present
    if os.path.exists('dv-dl.conf'):

        #instance is string of dataverse url base
        config = configparser.ConfigParser()
        config.read('dv-dl.conf')

        # if instance is not specified, default to the first option
        if(instance_name is None):
            try:
                instance_name = config.sections()[0]
                if debug:
                    print("Defaulting to use instance {}".format(instance_name))
            except:
                print("ERROR: No instances found in section headers of config file")
            if debug:
                print(instance_name)

        # Check if instance is found in config
        if instance_name in config:
            
            #Check if API is found for instance
            try:
                API_key = config.get(instance_name, 'API')
            except:
                if API_req:
                    print("ERROR: API for '{}' not found in config file".format(instance_name))
                    sys.exit(1)
                API_key = ""
                pass
        else:
            print("ERROR: '{}' not found in config file".format(instance_name))
            sys.exit(1)
            
        #API_key = config.get(instance_name, 'API')
        #API_key_html = "&key=" + API_key
        inst1 = dvinstance(instance_name, API_key)
        if debug:
            print(inst1.name)
            print(inst1.api)
        return inst1
    else:
        print("WARN: no conf file found")

# Basic URL encoding of string
def format_query(query):
    # This might be replaced with Slugify later if this proves to be too simplistic
    query = query.replace(' ','+')
    return query 

# create the dir if it does not exist
def create_dir_if_not_exist(path):
    if not os.path.exists('path'):
        try:
            os.mkdir(path)
        except OSError as error:
            # dir already exists
            pass

# Initalize parent directory
def init_dir():
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, "dataverse_datasets")
    create_dir_if_not_exist(path)

# Download to folder
def download(dir_name, global_id, base, API_key_html="", req_orig=False):
    if debug:
        print("Downloading...")
        print("download() req_orig: {}".format(req_orig))
    #create the sub dir
    parent_dir = os.getcwd()
    parent_dir = os.path.join(parent_dir, "dataverse_datasets")
    dl_path = os.path.join(parent_dir, dir_name)
    create_dir_if_not_exist(dl_path)
    file_path = dl_path + "/dataverse_files.zip"

    #TODO: Check if file needs API and if so, give propper error

    dl_url = base + '/api/access/dataset/:persistentId?persistentId=' + global_id + API_key_html
    if debug:
        print(dl_url)
    if req_orig:
        # download the original files
        # NOTE: Right now, dv-dl will not check if original files are already downloaded or not
        # This will be fixed when checksums are implemented
        if debug:
            print("Downloading original files")
        meta_url = 'https://' + base + '/api/datasets/:persistentId/?persistentId=' + global_id + API_key_html
        response = requests.get(meta_url)
        data = response.json()
        # get title name to create dir name from
        title = (data['data']['latestVersion']['metadataBlocks']['citation']['fields'][0]['value'])
        # TODO: Clean this up so that all files are put in ./dataverse_datasets/{title}/{files}
        dl_path = dl_path + '/dataverse_datasets/' + title + ' - ' + global_id + '/'
        if data['status'] != 'OK':
            print(data['status'])
            sys.exit()
        for i in data['data']['latestVersion']['files']:
            # i['dataFile']['id']) is the file id (database ID)

            dl_url = 'https://' + base + '/api/access/datafile/' + str(i['dataFile']['id'])
            file_name = i['label'] # filename of archived file 
            # Files which don't have an original file type will return a 404 when trying to
            # request the original format. So check if the file is a tab (archive file) before
            # attempting to download
            if file_name[-4:] == ".tab":
                dl_url = dl_url + '?format=original'
                os.system("wget -nc --content-disposition -P '{}' '{}'".format(dl_path, dl_url))
            else:
                os.system("wget -nc --content-disposition -P '{}' '{}'".format(dl_path, dl_url))
            # Note: Manifest is not downloaded, but for now, it's not really neccesary.
        pass
    # check if the files are already downloaded
    elif os.path.exists(file_path):
        print("File already exists")
    else:
        # download the file
        if debug:
            print(dl_path)
        os.system("wget -nc --content-disposition -P '{}' '{}'".format(dl_path, dl_url))
        if unzip:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                extract_path = os.path.join(dl_path + "/extract/")
                zip_ref.extractall(extract_path)


def search_and_dl(instance, search_term, API_key_html='', req_orig = False):
    if debug:
        print("Searching {} for '{}'".format(instance, search_term))

    init_dir()
    rows = 10
    start = 0
    page = 1

    base = "https://" + instance
    
    #check if API key is present
    if len(API_key_html) == 0:
        print("ERROR: Missing API Key")
        sys.exit()
        
    condition = True # emulate do-while    
    while (condition):
        url = base + '/api/search?q=' + search_term + "&type=dataset&type=file&show_entity_ids=true" + API_key_html + "&start=" + str(start)
        response = requests.get(url)
        data = response.json()
        if data['status'] != 'OK':
            print(data['status'])
            sys.exit()
        total = data['data']['total_count']
        print("=== Page", page, "===")
        print("start:", start, " total:", total)
        for i in data['data']['items']:
            print("- ", i['name'], "(" + i['type'] + ")")
            download(i['name'], i['global_id'], instance, req_orig = req_orig)
            sys.exit() # for testing purposes
            pass
        start = start + rows
        page += 1
        condition = start < total
        condition = False #For testing only and artificial limiter

# Parse a URL containing a DOI to get the DOI
def parse_URL_get_DOI(url):
    pattern = "(10\.\d{4,5}\/[\S]+[^;,.\s])"
    if bool(re.search(pattern, url)):
        result = re.search(pattern, url)
    else:
        # If a DOI cannot be found, print an error
        print("Could not find DOI in URL")
        sys.exit(1)
    return result.group()
    pass

def subcmd_search(args):
    # Read API Key if present in config
    inst1 = read_conf(args.instance, API_req = True)
    API_key_html = "&key=" + inst1.api
    if debug:
        print(API_key_html)
    instance = inst1.name
    search_term = format_query(args.search_term)
    req_orig = args.original
    search_and_dl(instance = instance, search_term = search_term, API_key_html = API_key_html, req_orig = req_orig)

def subcmd_download(args):

    path = os.getcwd()
    req_orig = args.original
        
    # Read API Key if present in config
    inst1 = read_conf(args.instance, API_req = True) # set to true unless can figure out if download needs API
    API_key_html = "&key=" + inst1.api
    if debug:
        print(API_key_html)
    if args.doi:
        download(path, args.doi, inst1.name, API_key_html, req_orig = req_orig)
    elif args.url:
        url = args.url
        parsed_DOI = parse_URL_get_DOI(url)
        download(path, parsed_DOI, inst1.name, API_key_html, req_orig = req_orig)
        
def main():

    
    # create the top-level parser
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='A download tool for Dataverse instances')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')

    # Global arguments
    parser.add_argument('--instance', help='Dataverse instance')
    parser.add_argument('--original', help='Specify that the original files should be fetched', action="store_true")
    
    # Parser for download subcommand
    parser_search = subparsers.add_parser('search', help='Search and download datasets. Defaults to generic query')
    parser_search.add_argument('search_term', help='search query')
    
    # Search params
    # https://guides.dataverse.org/en/latest/api/search.html#id1
    parser_search.add_argument('--title', help='Filter by title')
    # implement later
    #parser_search.add_argument('--type', help='Filter by type. Type can be Dataverse, dataset or file')
    parser_search.add_argument('--subtree', help='The identifier of the Dataverse collection to which the search should be narrowed')
    parser_search.add_argument('--sort', help='Sort results. Supported flags are name and date')
    parser_search.add_argument('--order', choices=['asc', 'desc'], help='The order by which to sort. Can be asc or desc')
    parser_search.add_argument('--per_page', type=int, default=10, help='The number of results to return per request. The default is 10, the max is 1000')
    parser_search.add_argument('--start', type=int, help='A cursor for paging through search results')
    parser_search.add_argument('--fq', help='Filter query')
    
    # Extended search params for dv-dl
    
    parser_search.set_defaults(func=subcmd_search)
    # TODO
    parser_search.add_argument('--print', help='Print dataset details')


    # Parser for download subcommand
    
    # create the parser for the "download" command
    parser_download = subparsers.add_parser('download', help='Download individual datasets')
    parser_download.set_defaults(func=subcmd_download)

    # Create a group for mutally exclusive options DOI and URL for download subcommand
    group_download = parser_download.add_mutually_exclusive_group(required=True)
    group_download.add_argument('--doi',  help='Download by DOI (or handle)')
    group_download.add_argument('--url',  help='Download by URL ')

    #calls subcmd_download, subcmd_search, or any other subcmd_* function created
    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)
    
#Start script
#main()
if __name__ == '__main__':
    main()

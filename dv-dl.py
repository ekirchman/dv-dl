import requests
import json
import pprint
import os
import re
import sys #sys.exit() and calling wget
import zipfile
import argparse

# default values 
base = 'https://dataverse.unc.edu'
search_term = 'Harris+1973+Nuclear+Power+Survey+study+no+2345'
unzip = True
clobber = False

# Read in API Key
try:
    api_file = open(".api_key","r")
except IOError:
    print("Cannot open API key file (.api_key)")
    sys.exit(1)

API_key = api_file.readlines()
api_file.close()
API_key_html = "&key=" + API_key[0]

# create the dir if it does not exist
def create_dir_if_not_exist(path):
    if not os.path.exists('path'):
        try:
            os.mkdir(path)
        except OSError as error:
            #print(error)
            pass

# Initalize parent directory
def init_dir():
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, "dataverse_datasets")
    create_dir_if_not_exist(path)

##Download to folder
def download(dir_name, global_id):
    #create the sub dir
    parent_dir = os.getcwd()
    parent_dir = os.path.join(parent_dir, "dataverse_datasets")
    dl_path = os.path.join(parent_dir, dir_name)
    create_dir_if_not_exist(dl_path)
    file_path = dl_path + "/dataverse_files.zip"

    #check if the files is already downloaded
    if os.path.exists(file_path):
        print("File already exists")
    else:
        #download the file
        dl_url = base + '/api/access/dataset/:persistentId?persistentId=' + global_id
        #print(dl_url)
        #print(dl_path)
        os.system("wget -nc --content-disposition -P '{}' '{}'".format(dl_path, dl_url))
        #print("wget --content-disposition -P '{}' '{}'".format(dl_path, dl_url))
        if unzip:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                extract_path = os.path.join(dl_path + "/extract/")
                zip_ref.extractall(extract_path)


def search_and_bulk_dl():
    init_dir()
    rows = 10
    start = 0
    page = 1
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
            download(i['name'], i['global_id'])
            pass
        start = start + rows
        page += 1
        condition = start < total
        condition = False #For testing only and artificial limiter

def parse_URL_get_DOI():
    # TODO
    sys.exit()
    pass

def subcmd_search(args):
    #print("subcmd_search")
    search_and_bulk_dl()

def subcmd_download(args):
    #print("subcmd_download")
    path = os.getcwd()
    if args.doi:
        download(path, args.doi)
    elif args.url:
        DOI = parse_URL_get_DOI()
        download(path, DOI)

def main():
    
    # create the top-level parser
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='A download tool for Dataverse instances')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "search" command
    parser_search = subparsers.add_parser('search', help='Search and download datasets. Defaults to generic query')

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
    
    # create the parser for the "download" command
    parser_download = subparsers.add_parser('download', help='Download individual datasets')
    parser_download.set_defaults(func=subcmd_download)

    # Create a group for mutally exclusive options DOI and URL for download subcommand
    group_download = parser_download.add_mutually_exclusive_group(required=True)
    group_download.add_argument('--doi',  help='Download by DOI (or handle)')
    group_download.add_argument('--url',  help='Download by URL ')

    #calls subcmd_download, subcmd_search, or any other subcmd_* function created
    args = parser.parse_args()
    if args.func:
        args.func(args)
    
    
#Start script
main()

import requests
import json
import pprint
import os
import re
import sys #sys.exit()
import zipfile

base = 'https://dataverse.unc.edu'
search_term = 'Harris+1973+Nuclear+Power+Survey+study+no+2345'
unzip = True

# Read in API Key
try:
    api_file = open(".api_key","r")
except IOError:
    print("Cannot open API key file (.api_key)")
    sys.exit(1)

API_key = api_file.readlines()
api_file.close()
API_key_html = "&key=" + API_key[0]

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
        #print(i['entity_id'])
        #print("global_id:", i['global_id'])
        #print("url:", i['url'])
        download(i['name'], i['global_id'])
        pass
    start = start + rows
    page += 1
    condition = start < total
    #For testing only and artificial limiter
    condition = False

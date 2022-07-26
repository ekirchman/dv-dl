import requests
import json
import pprint
import os
import re
import sys #sys.exit()

base = 'https://dataverse.unc.edu'
search_term = 'Harris+1973+Nuclear+Power+Survey+study+no+2345'

# Read in API Key
try:
    api_file = open(".api_key","r")
except IOError:
    print("Cannot open API key file (.api_key)")
    sys.exit(1)

API_key = api_file.readlines()
api_file.close()
API_key_html = "&key=" + API_key 
print(API_key[0])
sys.exit()

def create_dir_if_not_exist(path):
    if not os.path.exists('path'):
        try:
            os.mkdir(path)
        except OSError as error:
            #print(error)
            pass


def init_dir():
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, "dataverse_datasets")
    create_dir_if_not_exist(path)

    
        
##Download to folder
def download(dir_name, global_id, db_id):
    #create the sub dir
    parent_dir = os.getcwd()
    parent_dir = os.path.join(parent_dir, "dataverse_datasets")
    path = os.path.join(parent_dir, dir_name)
    create_dir_if_not_exist(path)
    
    #download the file
    #os.chdir(path)
    dl_url = base + '/api/access/dataset/:persistentId?persistentId=' + global_id
    print(dl_url)
    


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
        download(i['name'], i['global_id'], i['entity_id'])
        pass
    start = start + rows
    page += 1
    condition = start < total
    #For testing only
    condition = False

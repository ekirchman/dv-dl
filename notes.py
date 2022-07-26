#Search
#https://dataverse.unc.edu/api/search?q=title:energy&type=dataset&key=

#Get survey poll data
#https://dataverse.unc.edu/api/dataverses/nnsp/contents?key=


# File download example
# Dataset:
# https://dataverse.unc.edu/api/access/datafile/15139/?persistentId=doi:10.15139/S3/H74VUO
# PDF:
#  https://dataverse.unc.edu/api/access/datafile/7519834


# Processing data

##pretty print dictionary
#pprint.pprint(data)
##number of dict keys

#pprint.pprint(data['data']['items'])
#for i in data['data']['items']:
#    print("name:", i['name'])
    #print("name_of_dataverse:", i['name_of_dataverse'])
    #print("url:", i['url'])
    #print("global_id:", i['global_id'])
    #if 'description' in i: #check id description exists
    #    print("description:", i['description'])

#print("number of items:", count)

##raw json dump
#print(data)

## Serializing json  
#json_object = json.dumps(data, indent = 4) 
#Print pretty json
#print(json_object)

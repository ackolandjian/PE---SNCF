import json

# Adapt the path where you want to store the json files
jsonData_path="C:/Users/clapo/Documents/3A/PE/jsonData/"
pdt_file="TRA_LH_LHR_PDT_OP_2020-02-14_040000.json"

# Read the entire transport plan file (24443 items)
with open(jsonData_path+pdt_file) as file:
    dict_pdt = json.load(file)

# Remove the info key (count the number of items in the file)
l=dict_pdt['data']

# Filter the lines L and J
trains_L = list(filter(lambda i: i.get('codeLigneCommerciale') =='L', l))
trains_J = list(filter(lambda i: i.get('codeLigneCommerciale') =='J', l))

# Create two files for the two lines
with open(jsonData_path+'lineL.json', 'w') as fp:
        json.dump(trains_L, fp, indent=2)

with open(jsonData_path+'lineJ.json', 'w') as fp:
        json.dump(trains_J, fp, indent=2)
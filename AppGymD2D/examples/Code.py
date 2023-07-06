import json
import pandas as pd

folderPath = 'C:\\Users\\Suvadip\\Documents\\New D2D\\gym-d2d-master\\examples'
textFilename = 'out.txt'

# Open the text file and read its contents
with open(folderPath + '\\' + textFilename, 'r') as file:
    text = file.read()

text = text.replace("'", "\"")
# Insert line breaks before and after each curly brace to separate the objects
text = text.replace('}{', '}\n{')

    
keys = [] #it will contain distinct object name that is Radio Base Stations
# this code is to find out distinct object names
for line in text.splitlines():
    obj = json.loads(line)
    for key, value in obj.items():
        keys.append(key)
    break

# print(keys)

output = []
for i in keys:
    for line in text.splitlines():
        obj = json.loads(line)
        print('\n')
        data = json.dumps(obj, indent=4)
        for key, value in obj.items():
            if i == key:
                print('true')
                output.append(f"{key} rate_bps {value['rate_bps']}")
                

print("Output is : ")
print(output)

with open(folderPath + '\\temperoryText.txt', 'a') as file:
    file.write('\n'.join(output))
    

# create a list of dictionaries to store the data
data = []
# iterate over the lines and extract the required information
for line in output:
    line_values = line.split()
    if len(line_values) == 3:
        obj_name, metric, value = line_values
        data.append({'Radio Base Station': obj_name, 'Metric': metric, 'Value': value})

# create a dataframe from the data
df = pd.DataFrame(data)


# save the dataframe to an excel file
df.to_excel(folderPath + '\\temp.xlsx', index=False)
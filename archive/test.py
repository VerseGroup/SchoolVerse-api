# open json file and read data and convert to dictionary
import json
with open('student_data-2.json') as f:
    data = json.load(f)

new_data = {}

for item in data:
    new_data[item['student_email']] = item

# save new data to json file
with open('student_data-2.json', 'w') as f:
    json.dump(new_data, f)
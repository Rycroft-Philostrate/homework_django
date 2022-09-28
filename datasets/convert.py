import csv
import json

dict_data_csv = []
with open('ad.csv', encoding='utf-8') as csv_file:
	data_csv = csv.DictReader(csv_file)
	for value in data_csv:
		dict_data_csv.append(value)

with open('data_ads.json', 'w', encoding='utf-8') as json_file:
	data_str = json.dumps(dict_data_csv, indent=4, ensure_ascii=False)
	json_file.write(data_str)

dict_data_csv = []
with open('category.csv', encoding='utf-8') as csv_file:
	data_csv = csv.DictReader(csv_file)
	for value in data_csv:
		dict_data_csv.append(value)

with open('data_categories.json', 'w', encoding='utf-8') as json_file:
	data_str = json.dumps(dict_data_csv, indent=4, ensure_ascii=False)
	json_file.write(data_str)

dict_data_csv = []
with open('location.csv', encoding='utf-8') as csv_file:
	data_csv = csv.DictReader(csv_file)
	for value in data_csv:
		dict_data_csv.append(value)

with open('data_locations.json', 'w', encoding='utf-8') as json_file:
	data_str = json.dumps(dict_data_csv, indent=4, ensure_ascii=False)
	json_file.write(data_str)

dict_data_csv = []
with open('user.csv', encoding='utf-8') as csv_file:
	data_csv = csv.DictReader(csv_file)
	for value in data_csv:
		dict_data_csv.append(value)

with open('data_users.json', 'w', encoding='utf-8') as json_file:
	data_str = json.dumps(dict_data_csv, indent=4, ensure_ascii=False)
	json_file.write(data_str)

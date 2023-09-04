import json, os

# directory for json file
folder_dir = "Kpay received"
if not os.path.exists(folder_dir):
	os.makedirs(folder_dir)

#set the path to json file
json_file_path = os.path.join(folder_dir, "total_amount.json")

def edit_values(value):
	with open(json_file_path, 'r') as f:
		data = json.load(f)
	data["amount"] = value

	with open(json_file_path, 'w') as f:
		json.dump(data, f)

def read_value():
	with open(json_file_path, 'r') as f:
		data = json.load(f)
		return data["amount"]

def initial_info_setup():
	if not os.path.exists(json_file_path):
		with open(json_file_path, 'w') as f:
			original_info = {"amount": 0}
			json.dump(original_info, f)
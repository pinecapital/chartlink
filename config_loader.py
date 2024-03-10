import json

def load_config(config_file_path='config.json'):
    with open(config_file_path, 'r') as file:
        return json.load(file)

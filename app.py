import argparse
import sys
import json
import yaml
from faker import Faker
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- Start of generator.py code ---
fake = Faker()
def generate_mock_data(data_template):
    if isinstance(data_template, dict):
        mock_data = {}
        for key, value in data_template.items():
            if "name" in key.lower() or "author" in key.lower():
                mock_data[key] = fake.name()
            elif "email" in key.lower():
                mock_data[key] = fake.email()
            elif "id" in key.lower():
                mock_data[key] = fake.random_int(min=1, max=1000)
            elif "title" in key.lower() or "content" in key.lower() or "text" in key.lower():
                mock_data[key] = fake.text(max_nb_chars=200)
            elif "is_active" in key.lower() or "is_student" in key.lower():
                mock_data[key] = fake.boolean()
            elif isinstance(value, str):
                mock_data[key] = fake.word()
            elif isinstance(value, int):
                mock_data[key] = fake.random_int()
            elif isinstance(value, float):
                mock_data[key] = fake.random_int() / 100
            elif isinstance(value, bool):
                mock_data[key] = fake.boolean()
            else:
                mock_data[key] = generate_mock_data(value)
        return mock_data
    elif isinstance(data_template, list):
        return [generate_mock_data(data_template[0]) for _ in range(5)]
    else:
        return data_template
# --- End of generator.py code ---

# --- Start of parser.py code ---
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON.")
        return None

def parse_yaml_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error: The file at {file_path} is not a valid YAML. Details: {e}")
        return None

def parse_api_definition(file_path):
    if file_path.endswith('.json'):
        return parse_json_file(file_path)
    elif file_path.endswith(('.yaml', '.yml')):
        return parse_yaml_file(file_path)
    else:
        print("Error: Unsupported file format. Please use a .json or .yaml/.yml file.")
        return None
# --- End of parser.py code ---

parser = argparse.ArgumentParser(description="A local mock API generator.")
parser.add_argument('--file', '-f', type=str, required=True, help="Path to the OpenAPI YAML or JSON file to parse.")
args = parser.parse_args()
API_DEFINITION_FILE = args.file

app = Flask(__name__)
CORS(app)

api_schema = parse_api_definition(API_DEFINITION_FILE)
if not api_schema:
    print("Failed to start the server. Please check your API definition file.")
    sys.exit()

# The only thing you need to change is this for loop in app.py
for path, path_item in api_schema.get('paths', {}).items():
    if '{id}' in path:
        continue
    
    for method, method_item in path_item.items():
        if method == 'get':
            schema_ref = method_item['responses']['200']['content']['application/json']['schema']['items']['$ref']
            schema_name = schema_ref.split('/')[-1]
            
            # --- This is the fix: Access the 'properties' key ---
            data_template = api_schema['components']['schemas'][schema_name]['properties']
            
            mock_data = [generate_mock_data(data_template) for _ in range(5)]
            app.add_url_rule(path, endpoint=f'{path}_{method}', view_func=lambda data=mock_data: jsonify(data), methods=['GET'])

# The rest of your app.py file remains the same.
if __name__ == '__main__':
    app.run(debug=True, port=5000)
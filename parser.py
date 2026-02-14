import json
import yaml

def parse_json_file(file_path):
    """Parses a JSON file and returns the data as a dictionary."""
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
    """Parses a YAML file and returns the data as a dictionary."""
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
    """
    Parses an API definition file (JSON or YAML) and returns the data.
    """
    if file_path.endswith('.json'):
        return parse_json_file(file_path)
    elif file_path.endswith(('.yaml', '.yml')):
        return parse_yaml_file(file_path)
    else:
        print("Error: Unsupported file format. Please use a .json or .yaml/.yml file.")
        return None

if __name__ == '__main__':
    # This is an example of how to use the function.
    # For this to work, you will need a file named 'sample.json'
    # in the same directory.
    data = parse_api_definition('sample.json')
    if data:
        print("Successfully parsed data:")
        print(data)
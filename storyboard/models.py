'''
 Load JSON script files.  
 Scripts are not stored in the database so they are not derived from Django's Model
'''
import os
from pathlib import Path
import json
from jsonschema import validate


# array to hold all scripts loaded in
scripts = []


def load_scripts():
    # determine current directory, where the script json files live
    current_dir = Path(__file__).resolve().parent

    # Load the schema file for script field validation, this is 
    # helpful when creating & debugging new script components.
    # See API docs at https://python-jsonschema.readthedocs.io/en/stable/validate/
    filepath = os.path.join(current_dir, 'script_schema.json')
    print('Loading script schema file: ' + filepath)
    with open(filepath) as file_obj:
        schema = json.load(file_obj)

    # list all files in current directory & look for each script json file
    file_list = os.listdir(current_dir)
    for filename in file_list:
        if filename.endswith('_script.json'):

            # load the json data 
            filepath = os.path.join(current_dir, filename)
            print('Loading script file: ' + filepath)
            with open(filepath) as file_obj:
                script_data = json.load(file_obj)

            # run validation to make sure script json fields are correct.  
            validate(script_data, schema)

            # add each script item to global scripts list
            scripts.extend(script_data)

def get_script(script_id):
    print('loading script:' + script_id)
    for script in scripts:
        if script['script_id']== script_id: 
            return script
    print('found script:' + str(script))
    return None
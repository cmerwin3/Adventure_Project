'''
 Load JSON script files.  
 Scripts are not stored in the database so they are not derived from Django's Model
'''
import os
from pathlib import Path
import json
from jsonschema import validate



# array to hold all scripts loaded in
scripts = {}


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
    script_list = []
    for filename in file_list:
        if filename.endswith('_script.json'):

            # load the json data 
            filepath = os.path.join(current_dir, filename)
            print('Loading script file: ' + filepath)
            with open(filepath) as file_obj:
                script_data = json.load(file_obj)

            # add each script item to global scripts list
            script_list.extend(script_data)

    # gather a list of all script ids
    script_id_list = []
    for script in script_list:
        script_id = script['script_id']
        script_id_list.append(script_id)

    # dynamically update schema with script_id to validate that each script is properly mapped to another script
    schema["items"]["properties"]["responses"]["items"]["properties"]["next_script"]["enum"] = script_id_list
    
    # run validation to make sure script json fields are correct.  
    validate(script_list, schema)

    

    # convert script array into a global dictionary for ease of use based on script id
    for script_data in script_list:
        script_id = script_data['script_id']
        scripts[script_id] = script_data

    # ensure the child scripts have the npc_list and the background of the parent
    cascade_script_values('background')
    cascade_script_values('npc_list')
    
def cascade_script_values(field_name):
    script_id_list = scripts.keys()
    for script_id in script_id_list:
        script = scripts[script_id]
        if len(script[field_name]) > 0:
            continue
        
        names = script_id.split(".")
        field_value = find_parent_field(field_name, names, len(names))
        
        if field_value is not None:
            script[field_name] = field_value


def find_parent_field(field_name, names, max_index):
    if max_index <= 1:
        return None
    parent_names = names[0:max_index-1]
    new_script_id = ".".join(parent_names)
    

    script = scripts[new_script_id]
    if len(script[field_name]) > 0:
        return script[field_name]

    if max_index == 0:
        return None
    else: 
        return find_parent_field(field_name, names, max_index-1)




def get_script(script_id):
    print('loading script:' + script_id)
    return scripts[script_id]
    
    
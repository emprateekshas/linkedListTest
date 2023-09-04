import subprocess
import json
import os
import textfsm

cmd_table_present = False
emapi_debug_enabled = False
#----------------------------
try:
    from textfsm import clitable
    cmd_table_present = True
except ImportError:
    cmd_table_present = False 
#-----------------------------------
def enable_emautoapi_debug():
    global emapi_debug_enabled
    emapi_debug_enabled = True


def disable_emautoapi_debug():
    global emapi_debug_enabled
    emapi_debug_enabled = False   


def debug_log(message):
    global emapi_debug_enabled
    if emapi_debug_enabled == True:
        print(message)

   
def compile_program(input_file, exec_file):
    try:
        subprocess.run(["gcc", input_file, "-o", exec_file])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")   
        return False, None
    else:    
        return True, exec_file    

 
def run_program(exec_file):
    if os.path.exists(exec_file):
        try:
            process = subprocess.Popen(["stdbuf","-o0",exec_file],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            if process != None:
                print(f"Process {exec_file} started successfully")                   
            return process  
        except:
            print(f"An error occured")
            return None   
    else:
        print(f"Executable file {exec_file} does not exists") 
        return None                           

 
def read_prompt(process, expected_prompt):
    prompt = ""
    #debug_log(f'Expecting prompt: "{expected_prompt}"')
    while not prompt.endswith(expected_prompt):
        char = process.stdout.read(1)
        if char == "":
            break
        prompt += char
    return prompt


def provide_inputs(process, input_val, prompt_str= None):
    try:
        if prompt_str != None: 
            prompt = read_prompt(process, prompt_str)
            if prompt != prompt_str:
                print("Recieved prompt is not same as expected prompt")
                print(f'Expected: {prompt_str}')
                print(f'Recieved prompt: {prompt}')
                return False

        process.stdin.write(str(input_val) + "\n")
        process.stdin.flush()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")        


def read_text_output(process):
    read_text = ""
    while True:
        line = process.stdout.readline().strip()
        if not line:
            break
        read_text += line + "\n"  # Add the line to the accumulated text with a newline character   
    return read_text.rstrip("\n")  # Remove the trailing newline character if present


    
def template_to_fsm(template_file):
    with open(template_file) as template_file_obj:
        fsm = textfsm.TextFSM(template_file_obj)
    return fsm


def _get_template_dir():
    template_dir = os.environ.get("TEMPLATE_PATH")
    if template_dir is None:
        package_dir = os.path.dirname(__file__)
        template_dir = os.path.join(package_dir, "templates")
        if not os.path.isdir(template_dir):
            project_dir = os.path.dirname(os.path.dirname(os.path.dirname(template_dir)))
            template_dir = os.path.join(project_dir, "templates")
    return template_dir


def _clitable_to_dict(cli_table):
    """Convert TextFSM cli_table object to list of dictionaries."""
    obj = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        obj.append(temp_dict)
    return obj
    

# Convert parsed data to a list of dictionaries
def template_to_dict(input_text, fsm=None, command_str=None, platform=None):
    def merge_objects(obj_list):                              #this function will merge the result if there is multiple line
        # Merge objects in the list with a newline character
        merged_obj = {}
        for obj in obj_list:
            for key, value in obj.items():
                if key in merged_obj:
                    merged_obj[key] += '\n' + value
                else:
                    merged_obj[key] = value
        return [merged_obj]
    
    if fsm:
        input_text = fsm.ParseText(input_text)  # Fix this line
        header = fsm.header
        objs = []
        for row in input_text:
            temp_dict = {}
            for index, element in enumerate(row):
                temp_dict[header[index].lower()] = element
            objs.append(temp_dict)
        objs = merge_objects(objs)
    else:    
        if not cmd_table_present:
            msg = """ """
            raise ImportError(msg)
        template_dir = _get_template_dir()
        cli_table = clitable.CliTable("index", template_dir)
        attrs = {"Command": command_str, "Platform": platform}
        try:
            cli_table.ParseCmd(input_text, attrs)
            objs = _clitable_to_dict(cli_table)
        except clitable.CliTableError as err:
            raise Exception(f'Unable to parse command "{command_str}" on platform {platform} - {str(err)}') from err 

    return objs


def read_dict_output(process, template_file, read_length= None):
    result = ''
    if read_length == None:
        result = read_text_output(process)
    else:  
        result = process.stdout.read(read_length).strip()  
    # Load the TextFSM template
    template_fsm = template_to_fsm(template_file)
    # Parse the result using the template
    output = template_to_dict(result, fsm=template_fsm)
    debug_log(f'Generated dictionary: {output}')
    return output    
"""
def read_dict_output(process, template_file):
    result = read_text_output(process)
    #print(result)
    template_fsm = template_to_fsm(template_file)
    #print(template_fsm)
    output = template_to_dict(result, fsm = template_fsm)
    debug_log(f'Generated dictionary: {output}')
    return output
"""


def TC_banner(number, desc, reason = "None"):
    if reason.upper() == "STARTED":
        print("=" * 70)    
    print(f"TC {number}: {desc}: {reason}")
    if reason in ["ended", "PASSED", "FAILED"]:
        print("=" * 70)


def create_json(structured_data):
    # Print or save the structured data as JSON
    output_file_path = "structured_data.json"
    with open(output_file_path, "w") as json_file:
        json.dump(structured_data, json_file, indent=4)


def print_structured_data(structured_data):
    for entry in structured_data:
        print(entry)

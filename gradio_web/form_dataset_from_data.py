import os
import glob
import json

from modules.utils.instruction_processing import extract_jarray, extract_instructions

def get_json_files(folder_path):
    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    return json_files

if __name__ == '__main__':
    folder_path = 'data'
    json_files_list = get_json_files(folder_path)
    valid_data_list = []
    for json_file_path in json_files_list:
        with open(json_file_path,'r') as f:
            data = json.load(f)
        uncheck_commands = [cmd for jarrays in extract_jarray(data['output'][0]) for cmd in jarrays ]
        checked_commands = extract_instructions("config/cmd_pattern.json", data['output'][0])
        if len(uncheck_commands) == 0 or len(uncheck_commands) != len(checked_commands):
            print(uncheck_commands,"\n",checked_commands,"\n\n\n")
            continue
        data['output'] = data['output'][0]
        valid_data_list.append(data)
    
    with open("chat_dataset.json", 'w') as file:
        json.dump(valid_data_list, file, indent=4, ensure_ascii= False)
    print(f"Total: {len(json_files_list)} Valid: {len(valid_data_list)}\nValid Data Rate: {len(valid_data_list)/len(json_files_list)*100}%")


        




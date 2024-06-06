import json
from const import PATTERN_FILE_PATH

patterns: dict = json.load(open(PATTERN_FILE_PATH,'r'))
able2merge_commands = [command for command in patterns.keys() if patterns[command]['combine'] == True]

def extract_jarray(process_string:str):
    """
    ### This function extract jarrays in string
    ### Args
    ```
        process_string(str): string to exract
    ```
    ### Returns:
    ```
        jarrays(list[json_item]): extracted jarrays
    ```
    """
    sum = 0
    match_str=""
    match_strs=[]
    jarrays=[]
    for char in process_string:
        if char == "[":
            sum += 1
            match_str += char
            continue
        if char == "]":
            if sum == 1:
                match_str += char
                match_strs.append(match_str)
                match_str = ""
                sum = 0
            elif sum >= 1:
                match_str += char
                sum -= 1
            continue
        if sum > 0:
            match_str+=char
    for each in match_strs:
        try:
            jarray_item = json.loads(each)
            jarrays.append(jarray_item)
        except:
            continue

    return jarrays
 

def check_instruction(pattern_dict:dict, instruction:dict):
    # 如果pattern中无该指令，跳过
    if instruction.get("command", "key_err") not in pattern_dict.keys():
        print(f"command not match")
        return False
    # 如果paras类型不符，跳过
    if pattern_dict[instruction["command"]]["paras_type"] != None:
        if len(pattern_dict[instruction["command"]]["paras_type"]) !=len(instruction["paras"]):
            print(f"paras lenth not match")
            return False
        for para, right_type in zip(instruction["paras"], pattern_dict[instruction["command"]]["paras_type"]):
            if str(type(para)) != right_type:
                print(f"paras type not match")
                return False
    # 如果是enum且不满足，跳过
    if pattern_dict[instruction["command"]]["paras_enum"] != None:
        if instruction["paras"] not in pattern_dict[instruction["command"]]["paras_enum"]:
            for para, enum in zip(instruction["paras"], pattern_dict[instruction["command"]]["paras_enum"]):
                if enum != None and para not in enum:
                    print(f"enum not match")
                    return False
    # 如果不满足范围，跳过
    try:
        for each in instruction["paras"]:
            if pattern_dict[instruction["command"]]["paras_min"] != None and each < pattern_dict[instruction["command"]]["paras_min"]:
                print(f"paras range not match1")
                return False
            if pattern_dict[instruction["command"]]["paras_max"] != None and each > pattern_dict[instruction["command"]]["paras_max"]:
                print(f"paras range not match2")
                return False
    except:
        if pattern_dict[instruction["command"]]["paras_min"] != None and instruction["paras"] < pattern_dict[instruction["command"]]["paras_min"]:
                print(f"paras range not match3")
                return False
        if pattern_dict[instruction["command"]]["paras_max"] != None and instruction["paras"] > pattern_dict[instruction["command"]]["paras_max"]:
            print(f"paras range not match4")
            return False
    
    return True

def extract_instructions(pattern_file_path:str, string:str):
    """
    ### This method extract checked instructions from string
    ### Args:
    ```
        pattern_file_path(str) : path of the pattern file
        string(str) : string to extract
    ```
    ### Returns:
    ```
        instructions(list[dict]) : extracted instructions
    ```
    """
    instructions = []
    jarrays_list = extract_jarray(string)

    with open(pattern_file_path, 'r') as json_file:
        pattern_dict:dict = json.load(json_file)

    for instraction_list in jarrays_list:
        if type(instraction_list) != list:
            continue
        for instruction in instraction_list:
            if type(instruction) != dict:
                continue
            if check_instruction(pattern_dict, instruction):
                instructions.append(instruction)
    
    return instructions

def combine_commands(command_packages: list[dict]):
    merged_command_packages = []

    # Merge
    merged_change = merge_change(command_packages)
    merged_command_packages.append(merged_change) if merged_change != None else None

    merged_face = merge_face(command_packages)
    merged_command_packages.append(merged_face) if merged_face != None else None

    # Add commands that not able to merge
    [merged_command_packages.append(command_package) for command_package in command_packages if command_package['command'] not in able2merge_commands]
    

    # Sort commands through priority
    sorted_merged_command_packages = sorted(merged_command_packages, key=lambda item: patterns[item['command']]['priority'], reverse= True)

    return sorted_merged_command_packages

def merge_change(command_packages: list[dict]):
    change_command_packages = [command_package for command_package in command_packages if command_package['command'] == 'change']
    if len(change_command_packages) < 1:
        return None
    merged_change_command_package = {'command': 'change'}
    # merge tags
    tags = list(set([tag for change_command_package in change_command_packages for tag in change_command_package ['paras'][0]]))
    # merge prompt
    prompt = ''
    for change_command_package in change_command_packages:
        prompt += f', {change_command_package["paras"][1]}' if prompt != '' else change_command_package["paras"][1]
    
    merged_change_command_package['paras'] = [tags, prompt]

    return merged_change_command_package

def merge_face(command_packages: list[dict]):
    face_command_packages = [command_package for command_package in command_packages if command_package['command'] == 'face']
    if len(face_command_packages) < 1:
        return None
    merged_face_command_package = {'command': 'face'}
    # merge prompt
    prompt = ''
    for change_command_package in face_command_packages:
        prompt += f', {change_command_package["paras"][0]}' if prompt != '' else change_command_package["paras"][0]
    
    merged_face_command_package['paras'] = [prompt]

    return merged_face_command_package


    
if __name__ == '__main__':
    import os

    # 获取当前脚本文件的路径（包括文件名）
    current_script_path = __file__

    # 获取当前脚本文件所在的目录
    current_script_dir = os.path.dirname(current_script_path)

    # 构建相对路径，相对于当前脚本文件所在的目录
    absolute_path = os.path.join(current_script_dir, "../config/cmd_pattern.json")

    # 打印绝对路径
    print("绝对路径:", absolute_path)

    description = """根据描述，我们需要对图片进行美颜、背景颜色更改为白色、裁剪矩形区域并提高分辨率。具体实现方式如下：\n\n1. 美颜：使用beauty命令，参数为50，表示美颜50%。\n2. 背景颜色更改为白色：使用change background color命令，参数为\"white\"。\n3. 裁剪矩形区域：使用split命令，参数为[ a, b, c, d]表示裁剪矩形区域(a,b)到(c,d)。\n4. 提高分辨率：使用super resolution命令，参数为3.0。\n\n综上所述，可以得到以下JSON数组：\n```json\n[\n    {\n        \"command\" : \"change background color\",\n        \"paras\" : \"white\",\n        \"command\" : \"beauty\",\n        \"paras\" : 50,\n        \"command\" : \"split\",\n        \"paras\" : [0.25, 0.25, 0.75, 0.75]\n    },\n    {\n        \"command\" : \"super resolution\",\n        \"paras\" : 3.0\n    }\n]\n```"""
    print(description)
    print(extract_instructions(absolute_path, description))

    # 测试
    input_commands = [
        {'command': 'change', 'paras': [['Background'], 'Beach']},
        {'command': 'advice', 'paras': ['你可以尝试给图片增加一些夏天的元素，比如添加一把太阳伞或者沙滩玩具等等。']},
        {'command': 'change', 'paras': [['Upper-clothes'], 'Red dress']}
    ]
    print(combine_commands(input_commands))
    input_commands = [
        {'command': 'advice', 'paras': ['你可以尝试给图片增加一些夏天的元素，比如添加一把太阳伞或者沙滩玩具等等。']}
    ]
    print(combine_commands(input_commands))

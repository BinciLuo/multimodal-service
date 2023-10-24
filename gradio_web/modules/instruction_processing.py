from utils.json_extractor import extract_jarray
import json

def check_instruction(pattern_dict:dict,instruction:dict):
    # 如果pattern中无该指令，跳过
    if instruction["command"] not in pattern_dict.keys():
        print(f"command not match")
        return False
    # 如果paras类型不符，跳过
    if pattern_dict[instruction["command"]]["paras_type"] != str(type(instruction["paras"])):
        print(f"paras type not match")
        return False
    # 如果是enum且不满足，跳过
    if pattern_dict[instruction["command"]]["paras_enum"] != None:
        if instruction["paras"] not in pattern_dict[instruction["command"]]["paras_enum"]:
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
    instructions = []
    jarrays_list = extract_jarray(string)

    with open(pattern_file_path, 'r') as json_file:
        pattern_dict = json.load(json_file)
    
    for instraction_list in jarrays_list:
        if type(instraction_list) != list:
            continue
        for instruction in instraction_list:
            if type(instruction) != dict:
                continue
            if check_instruction(pattern_dict,instruction):
                instructions.append(instruction)
    
    return instructions

if __name__ == '__main__':
    import os

    # 获取当前脚本文件的路径（包括文件名）
    current_script_path = __file__

    # 获取当前脚本文件所在的目录
    current_script_dir = os.path.dirname(current_script_path)

    # 构建相对路径，相对于当前脚本文件所在的目录
    absolute_path = os.path.join(current_script_dir, "../config/pattern.json")

    # 打印绝对路径
    print("绝对路径:", absolute_path)

    description = """根据描述，我们需要对图片进行美颜、背景颜色更改为白色、裁剪矩形区域并提高分辨率。具体实现方式如下：\n\n1. 美颜：使用beauty命令，参数为50，表示美颜50%。\n2. 背景颜色更改为白色：使用change background color命令，参数为\"white\"。\n3. 裁剪矩形区域：使用split命令，参数为[ a, b, c, d]表示裁剪矩形区域(a,b)到(c,d)。\n4. 提高分辨率：使用super resolution命令，参数为3.0。\n\n综上所述，可以得到以下JSON数组：\n```json\n[\n    {\n        \"command\" : \"change background color\",\n        \"paras\" : \"white\",\n        \"command\" : \"beauty\",\n        \"paras\" : 50,\n        \"command\" : \"split\",\n        \"paras\" : [0.25, 0.25, 0.75, 0.75]\n    },\n    {\n        \"command\" : \"super resolution\",\n        \"paras\" : 3.0\n    }\n]\n```"""
    print(description)
    print(extract_instructions(absolute_path,description))

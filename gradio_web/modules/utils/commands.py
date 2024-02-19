import json
from const import PATTERN_FILE_PATH

patterns = json.load(open(PATTERN_FILE_PATH,'r'))
able2merge_commands = [command for command in patterns.keys() if patterns[command]['combine'] == True]


def combine_commands(command_packages: list[dict]):
    merged_command_packages = []
    merged_change = merge_change(command_packages)
    merged_command_packages.append(merged_change) if merged_change != None else None
    [merged_command_packages.append(command_package) for command_package in command_packages if command_package['command'] not in able2merge_commands]

    return merged_command_packages

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


if __name__ == '__main__':
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
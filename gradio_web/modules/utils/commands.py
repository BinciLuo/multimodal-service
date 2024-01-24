def combine_commands(command_packages: list[dict]):
    merged_command_packages = []
    merged_change_command_package = {}  # 用于存储 'change' 类型的命令的合并结果

    for command_package in command_packages:
        # if command == 'change', add to change_commands
        if command_package['command'] == 'change':
            if merged_change_command_package == {}:
                merged_change_command_package = command_package
                continue
            # merge tags
            merged_change_command_package['paras'][0] = merged_change_command_package['paras'][0]+[tag for tag in command_package['paras'][0] if tag not in merged_change_command_package['paras'][0]]
            # merge prompt
            merged_change_command_package['paras'][1] = merged_change_command_package['paras'][1]+f', {command_package["paras"][1]}'
        else:
            merged_command_packages.append(command_package)

    if merged_change_command_package != {}:
        merged_command_packages.append(merged_change_command_package)

    return merged_command_packages

if __name__ == '__main__':
    # 测试
    input_commands = [
        {'command': 'change', 'paras': [['Background'], 'Beach']},
        {'command': 'advice', 'paras': ['你可以尝试给图片增加一些夏天的元素，比如添加一把太阳伞或者沙滩玩具等等。']},
        {'command': 'change', 'paras': [['Upper-clothes'], 'Red dress']}
    ]
    print(combine_commands(input_commands))
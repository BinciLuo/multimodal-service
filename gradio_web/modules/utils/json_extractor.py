import json


def extract_jarray(process_string:str):
    """
    This function extract jarrays in string

    Args:
        process_string(str): String to exract
    
    Returns:
        List[json_item]: Extracted jarrays
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
                
if __name__ == "__main__":
    description = """根据描述，我们需要对图片进行美颜、背景颜色更改为白色、裁剪矩形区域并提高分辨率。具体实现方式如下：\n\n1. 美颜：使用beauty命令，参数为50，表示美颜50%。\n2. 背景颜色更改为白色：使用change background color命令，参数为\"white\"。\n3. 裁剪矩形区域：使用split命令，参数为[ a, b, c, d]表示裁剪矩形区域(a,b)到(c,d)。\n4. 提高分辨率：使用super resolution命令，参数为3.0。\n\n综上所述，可以得到以下JSON数组：\n```json\n[\n    {\n        \"command\" : \"change background color\",\n        \"paras\" : \"white\",\n        \"command\" : \"beauty\",\n        \"paras\" : 50,\n        \"command\" : \"split\",\n        \"paras\" : [0.25, 0.25, 0.75, 0.75]\n    },\n    {\n        \"command\" : \"super resolution\",\n        \"paras\" : 3.0\n    }\n]\n```"""
    print(description)
    print(extract_jarray(description))


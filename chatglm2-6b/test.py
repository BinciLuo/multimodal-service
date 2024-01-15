from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("/ark-contexts/imported_models/chatglm2-6b/huggingface/THUDM/chatglm2-6b", trust_remote_code=True)

model = AutoModel.from_pretrained("/ark-contexts/imported_models/chatglm2-6b/huggingface/THUDM/chatglm2-6b", trust_remote_code=True, device='cuda')
model = model.eval()

response, history = model.chat(tokenizer, '{"query": "现在我给出一段关于图片修改的描述，请将它解析为一串命令，格式为json，不支持的跳过，支持的有：\n[\n    {\n        \"command\" : \"change background color\",\n        \"paras\" : color\n    },\n    {\n        \"command\" : \"super resolution\",\n        \"paras\" : rate\n    },\n    {\n        \"command\" : \"beauty\",\n        \"paras\" : rate\n    },\n    {\n        \"command\" : \"split\",\n        \"paras\" : [ a, b, c, d]\n    },\n]\n其中change background color为更改背景颜色，color为颜色，类型为英文字符串，如\"red\"\nsuper resolution为超分辨率，rate为float，如1.5表示超分辨率1.5倍\nbeauty为美颜rate表示程度，类型为int，范围为1-100\nsplit为分割，abcd分别代表(a,b)和(c,d)确认的矩形相对范围，如a,b=0.25, c,d=0.75表示裁剪（1/4，1/4）到（3/4.3/4）\n\n下面是修改的描述：\n帮我美颜然后把背景换为白色，裁切中间的部分然后提高分辨率到原来的4倍\n\n给我的回答请只包含json array，在json array前后不要任何信息，模版如下：\n[\n    {\n        \"command\" : \"change background color\",\n        \"paras\" : : \"red\"\n    },\n    {\n        \"command\" : \"super resolution\",\n        \"paras\" : 1.5\n    },\n    {\n        \"command\" : \"beauty\",\n        \"paras\" : 50\n    },\n    {\n        \"command\" : \"split\",\n        \"paras\" : [0.25, 0.25, 0.75, 0.75]\n    },\n]\n"}', history=[])
print(response)

response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)
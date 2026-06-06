def clean_text(text):
    # 1. 去掉首尾空格
    text = text.strip()
    while '  ' in text:  
        text = text.replace('  ', ' ')
    text = text.replace('，', ',')
    text = text.replace('。', '.')
    text = text.replace('！', '!')
    text = text.replace('？', '?')
    text = text.replace('；', ';')
    text = text.replace('：', ':')
    return text

test = input("请输入要清洗的文本：")
result = clean_text(test)
print(f"清洗前: '{test}'")
print(f"清洗后: '{result}'")
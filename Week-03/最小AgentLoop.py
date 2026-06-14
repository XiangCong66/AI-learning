import requests
import json
import re
import os
from datetime import datetime


# 工具1：搜索（模拟）
def search(keyword):
    """模拟搜索工具"""
    fake_database = {
        '深圳': '深圳是城市。',
        '天气': '天气是一定时间内的气象状况。',
        'python': 'Python是编程语言。',
        'agent': 'AI Agent是智能体。',
        '龙虾': '龙虾是一种海洋动物，好吃😋。深圳大学龙虾工作室是一个AI学习小组。',
        '正则': '正则表达式是一种用于匹配字符串中字符组合的模式，常用于文本搜索和替换。'
    }
    
    for key, value in fake_database.items():
        if keyword in key or keyword in value:
            return f"搜索结果: {value}"
    
    return f"未找到与 '{keyword}' 相关的结果"


# 工具2：计算器（安全eval）
def calculator(expr):
    """安全计算器"""
    if not re.match(r'^[\d\+\-\*\/\.\(\)\s]+$', expr):
        return "错误: 表达式包含非法字符"
    
    try:
        result = eval(expr)
        return f"计算结果: {expr} = {result}"
    except ZeroDivisionError:
        return "错误: 不能除以零"
    except Exception as e:
        return f"计算错误: {e}"


# 工具3：天气查询
def get_weather(city):
    """调用wttr.in API获取天气"""
    url = f"https://wttr.in/{city}?format=j1&lang=zh"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()['current_condition'][0]
            temp = data['temp_C']
            weather = data['weatherDesc'][0]['value']
            humidity = data['humidity']
            return f"{city}天气: 温度{temp}°C, {weather}, 湿度{humidity}%"
        else:
            return f"查询{city}天气失败，状态码: {resp.status_code}"
    except requests.exceptions.Timeout:
        return f"查询{city}天气超时"
    except Exception as e:
        return f"查询{city}天气出错: {e}"


# 工具字典
tools = {
    'search': search,
    'calculator': calculator,
    'get_weather': get_weather
}


# 决策器
def decide_tool(query):
    # 包含数学运算符 计算器
    if re.search(r'[\d]+\s*[\+\-\*\/]\s*[\d]+', query):
        match = re.search(r'[\d\s\+\-\*\/\.\(\)]+', query)
        if match:
            expr = match.group().strip()
            return {'action': 'use_tool', 'tool': 'calculator', 'args': {'expr': expr}}
    
    # 提到天气 天气查询
    if '天气' in query or '温度' in query or '多少度' in query:
        clean_query = query.replace('问题:', '').replace('工具结果:', '').strip()
        
        # 提取天气关键词前面的城市名
        city_match = re.search(r'([\u4e00-\u9fa5a-zA-Z]+)(?:的)?(?:天气|温度|多少度)', clean_query)
        if city_match:
            city = city_match.group(1)
        else:
            # 没找到，取第一个中文词
            word_match = re.search(r'[\u4e00-\u9fa5a-zA-Z]+', clean_query)
            city = word_match.group() if word_match else '深圳'
        
        return {'action': 'use_tool', 'tool': 'get_weather', 'args': {'city': city}}
    
    # 包含搜索相关词 搜索
    if any(word in query for word in ['搜索', '查询', '什么是', '是谁', '介绍']):
        keyword = query
        for word in ['搜索', '查询', '什么是', '是谁', '介绍', '一下', '帮我', '请']:
            keyword = keyword.replace(word, '')
        keyword = keyword.strip().strip('的。，！？')
        
        if keyword:
            return {'action': 'use_tool', 'tool': 'search', 'args': {'keyword': keyword}}
    
    # 直接说城市名 天气
    for city in ['深圳', '北京', '上海', '广州', '杭州']:
        if city in query:
            return {'action': 'use_tool', 'tool': 'get_weather', 'args': {'city': city}}
    
    # 默认 搜索
    if query.strip():
        return {'action': 'use_tool', 'tool': 'search', 'args': {'keyword': query}}
    
    return {'action': 'finish', 'answer': '我无法理解这个问题，请换一种说法。'}

# Agent Loop
def agent_loop(query, max_steps=5):
    """最小Agent循环"""
    print(f"\n{'='*50}")
    print(f"用户问题: {query}")
    print(f"{'='*50}")
    for step in range(1, max_steps + 1):
        print(f"\n--- 第{step}步 ---")
        # 思考
        decision = decide_tool(query)
        print(f"[思考] 决策: {decision['action']}")
        # 结束判断
        if decision['action'] == 'finish':
            print(f"\n[完成] 最终回答: {decision['answer']}")
            return decision['answer']
        # Act
        tool_name = decision['tool']
        tool_args = decision['args']
        tool_func = tools[tool_name]
        print(f"行动 调用工具: {tool_name}")
        print(f"行动 参数: {tool_args}")
        
        result = tool_func(**tool_args)
        print(f"行动 结果: {result}")
        # 判断结果是否有效
        if '未找到' not in result and '失败' not in result and '错误' not in result and '超时' not in result:
            # 结果有效，直接返回
            print(f"\n[完成] 最终回答: {result}")
            return result
        else:
            # 结果无效，换个思路继续
            print(f"[思考] 当前工具未找到结果，尝试其他方式...")
            query = f"搜索 {query}"
    return "已尝试多种方式，仍未找到结果，请换一种问法。"

# 主程序 
def main():
    print("最小Agent Loop")
    print("支持: 天气查询 | 数学计算 | 信息搜索")
    print("输入 'q' 退出")
    
    while True:
        query = input("\n你: ").strip()
        if query.lower() == 'q':
            print("再见！")
            break
        if not query:
            continue
        
        answer = agent_loop(query)
        print(f"\nAgent: {answer}")


if __name__ == '__main__':
    main()
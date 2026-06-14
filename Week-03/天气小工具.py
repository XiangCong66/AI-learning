import requests
import json
import re
import os
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 缓存
def init_cache():
    """如果没有缓存文件，创建一个空的"""
    if not os.path.exists('Week-03/cache.json'):
        with open('Week-03/cache.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)
        print("[创建缓存文件 cache.json]")

def load_cache():
    if os.path.exists('Week-03/cache.json'):
        with open('Week-03/cache.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open('Week-03/cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False)

# 获取天气
def get_weather(city):
    # 先查缓存
    cache = load_cache()
    if city in cache:
        record = cache[city]
        if (datetime.now() - datetime.fromisoformat(record['time'])).seconds < 3600:
            print("[使用缓存]")
            return record['data']

    # 调API
    url = f"https://wttr.in/{city}?format=j1&lang=zh"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()['current_condition'][0]
            result = {
                'city': city,
                'temp': data['temp_C'],
                'weather': data['weatherDesc'][0]['value'],
                'humidity': data['humidity'],
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 存缓存
            cache[city] = {'data': result, 'time': datetime.now().isoformat()}
            save_cache(cache)
            return result
        elif resp.status_code == 404:
            print(f"城市 '{city}' 不存在")
        elif resp.status_code == 429:
            print("请求太频繁，请稍后再试")
        else:
            print(f"HTTP错误: {resp.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.ConnectionError:
        print("网络连接失败")
    return None

# 基础查询
def show_weather(city):
    info = get_weather(city)
    if not info:
        return
    print(f"\n城市: {info['city']}")
    print(f"温度: {info['temp']} C")
    print(f"天气: {info['weather']}")
    print(f"湿度: {info['humidity']}%")

    # 温度低于10度提示
    try:
        if int(info['temp']) < 10:
            print("提示: 记得加衣服！")
    except:
        pass

# 功能2：批量查询
def batch_query(cities_str):
    cities = re.split(r'[,，\s]+', cities_str.strip())
    cities = [c for c in cities if c]
    
    print(f"\n{'城市':<8} {'温度':<8} {'天气':<10} {'湿度':<8}")
    print("-" * 35)
    for city in cities:
        info = get_weather(city)
        if info:
            print(f"{info['city']:<8} {info['temp']+'C':<8} {info['weather']:<10} {info['humidity']+'%':<8}")

# 输入校验
def check_city(city):
    if not city or not city.strip():
        return False
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s\-]+$', city):
        return False
    return True

# 主程序
def main():
    init_cache()
    while True:
        print("\n 天气查询 ")
        print("1. 单个城市查询")
        print("2. 批量城市查询")
        print("3. 退出")
        choice = input("选择: ").strip()

        if choice == '1':
            city = input("城市名: ").strip()
            if not check_city(city):
                print("城市名不合法")
                continue
            show_weather(city)

        elif choice == '2':
            cities = input("城市列表(逗号分隔): ").strip()
            batch_query(cities)

        elif choice == '3':
            print("再见！")
            break

if __name__ == '__main__':
    main()
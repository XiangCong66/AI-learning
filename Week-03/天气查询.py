import requests
import json
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_weather(city):
    """
    获取指定城市的天气
    参数: city - 城市名（支持中文）
    返回: 包含天气信息的字典，失败返回 None
    """
    url = f"https://wttr.in/{city}?format=j1&lang=zh"

    try:
        print(f"正在查询 {city} 的天气...")
        resp = requests.get(url, headers=HEADERS, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            return parse_weather(data, city)
        elif resp.status_code == 404:
            print(f"城市 '{city}' 不存在，请检查城市名")
            return None
        else:
            print(f"HTTP错误，状态码: {resp.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接")
        return None
    except requests.exceptions.ConnectionError:
        print("网络连接失败，请检查网络")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None


def parse_weather(data, city):
    """解析天气数据"""
    try:
        current = data['current_condition'][0]
        weather_desc = current['weatherDesc'][0]['value'] if current.get('weatherDesc') else 'N/A'

        weather_info = {
            'city': city,
            'temp': current.get('temp_C', 'N/A'),
            'humidity': current.get('humidity', 'N/A'),
            'weather': weather_desc,
            'wind_speed': current.get('windspeedKmph', 'N/A'),
            'wind_dir': current.get('winddir16Point', 'N/A'),
            'feels_like': current.get('FeelsLikeC', 'N/A'),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_info

    except (KeyError, IndexError) as e:
        print(f"数据解析失败: {e}")
        return None


def show_weather(info):
    """显示天气信息"""
    if not info:
        return

    print(f"城市: {info['city']}")
    print(f"时间: {info['time']}")

    print(f"温度: {info['temp']}°C")
    print(f"体感: {info['feels_like']}°C")
    print(f"天气: {info['weather']}")
    print(f"湿度: {info['humidity']}%")
    print(f"风速: {info['wind_speed']} km/h")
    print(f"风向: {info['wind_dir']}")



def main():
    """主程序"""
    print("  天气查询工具")
    while True:
        city = input("请输入城市名（输入 q 退出）: ").strip()

        if city.lower() == 'q':
            print("再见！")
            break

        if not city:
            print("城市名不能为空")
            continue

        weather = get_weather(city)
        show_weather(weather)


if __name__ == '__main__':
    main()
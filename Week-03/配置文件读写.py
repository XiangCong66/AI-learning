import json
import os

def create_config():
    """配置文件不存在，创建一个默认配置"""
    config = {
        "window": {
            "width": 800,
            "height": 600
        },
        "theme": {
            "color": "#04006f",
        }
    }
    with open('Week-03/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print("已创建默认配置文件 config.json")

def read_config():
    """读取配置文件，返回字典"""
    if not os.path.exists('Week-03/config.json'):
        create_config()
    
    with open('Week-03/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def change_size(width, height):
    """修改窗口大小并保存"""
    config = read_config()
    config['window']['width'] = width
    config['window']['height'] = height
    
    with open('Week-03/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print(f"窗口大小已修改为 {width}x{height}")

def change_color(color):
    """修改主题颜色"""
    config = read_config()
    config['theme']['color'] = color
    
    with open('Week-03/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print(f"主题颜色已修改为 {color}")

def show_config():
    """友好地打印当前配置"""
    config = read_config()
    print(f"窗口大小: {config['window']['width']} x {config['window']['height']}")
    print(f"主题颜色: {config['theme']['color']}")

if __name__ == '__main__':
    show_config()
    
    change_size(1024, 768)
    show_config()
    
    change_color("#333333")
    show_config()
    
    print("请打开 config.json 文件查看保存的结果")
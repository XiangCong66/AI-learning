def divide():
    try:
        x = float(input("被除数: "))
        y = float(input("除数: "))
        print(f"结果: {x / y}")
    except ValueError:
        print("请输入数字！")
    except ZeroDivisionError:
        print("除数不能为0！")
divide()
address = {}

def add():
    name = input("请输入姓名：")
    phone = input("请输入电话：")
    address[name] = phone
    print(f"成功添加联系人：{name},{phone}")

def delete():
    name = input("请输入要删除的姓名：")
    if name in address:
        del address[name]
        print(f"已删除联系人：{name}")
    else:
        print(f"未找到联系人：{name}")

def search():
    name = input("请输入要查找的姓名：")
    if name in address:
        print(f"{name} 的电话是：{address[name]}")
    else:
        print(f"未找到联系人：{name}")


print("  通讯录管理系统")
print("1. 添加联系人")
print("2. 删除联系人")
print("3. 查找联系人")
print("4. 退出系统")
while True:
    choice = input("请选择操作(1-4)：")
    if choice == '1':
        add()
    elif choice == '2':
        delete()
    elif choice == '3':
        search()
    elif choice == '4':
        print("感谢使用，再见！")
        break
    else:
        print("输入错误，请输入1-4之间的数字")
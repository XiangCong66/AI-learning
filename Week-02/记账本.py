
import json
import os
from datetime import datetime

# 全局变量
expenses = []  # 存储所有账目
filename = "Week-02/expenses.json"  # 数据文件名

def load_expenses():
    global expenses
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                expenses = json.load(f)
            print(f"成功加载 {len(expenses)} 条账目记录")
        else:
            print("没有找到历史账目文件，将创建新文件")
            expenses = []
    except Exception as e:
        print(f"加载文件时出错：{e}，将使用空账目")
        expenses = []

def save_expenses():
    """保存账目数据到文件"""
    global expenses
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(expenses, f, ensure_ascii=False, indent=2)
        print("账目已保存")
        return True
    except Exception as e:
        print(f"保存失败：{e}")
        return False

def validate_date(date_str):
    """验证日期格式"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    """验证金额是否为有效数字"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "金额必须大于0"
        return True, amount
    except ValueError:
        return False, "请输入有效的数字"

def validate_category(category):
    """验证类别是否有效"""
    if not category or category.strip() == "":
        return False
    return True

def add_expense():
    """功能1：添加账目"""
    global expenses
    
    print("\n" + "="*50)
    print("添加新账目")
    print("="*50)
    
    while True:
        date = input("日期 (YYYY-MM-DD): ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            print(f"使用当前日期：{date}")
        if validate_date(date):
            break
        else:
            print("日期格式错误，请使用 YYYY-MM-DD 格式，如：2024-01-15")
    
    # 输入并验证类别
    categories = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "住房", "其他"]
    print(f"可选类别：{', '.join(categories)}")
    while True:
        category = input("类别: ").strip()
        if validate_category(category):
            break
        else:
            print("类别不能为空")
    
    # 输入并验证金额
    while True:
        amount_input = input("金额: ").strip()
        is_valid, result = validate_amount(amount_input)
        if is_valid:
            amount = result
            break
        else:
            print(f"{result}")
    
    # 输入备注（可选）
    note = input("备注 (可选): ").strip()
    
    # 生成新的ID
    if expenses:
        new_id = max([e['id'] for e in expenses]) + 1
    else:
        new_id = 1
    
    # 创建账目记录
    expense = {
        "date": date,
        "category": category,
        "amount": round(amount, 2),
        "note": note,
        "id": new_id
    }
    
    expenses.append(expense)
    
    # 字符串格式化输出添加的账目
    print("\n" + "─"*50)
    print(f"  已添加账目：")
    print(f"  ID: {expense['id']}")
    print(f"  日期：{expense['date']}")
    print(f"  类别：{expense['category']}")
    print(f"  金额：¥{expense['amount']:.2f}")
    print(f"  备注：{expense['note'] if expense['note'] else '无'}")
    print("─"*50)
    
    save_expenses()

def view_expenses():
    """功能2：查看所有账目"""
    global expenses
    
    print("所有账目列表")
    
    if not expenses:
        print("暂无账目记录")
        return
    
    # 格式化输出表格
    print(f"{'ID':<4} {'日期':<12} {'类别':<8} {'金额':<10} {'备注':<30}")
    
    total = 0
    for expense in expenses:
        print(f"{expense['id']:<4} {expense['date']:<12} {expense['category']:<8} "
              f"¥{expense['amount']:<9.2f} {expense['note']:<30}")
        total += expense['amount']
    
    print("-"*80)
    print(f"总计：¥{total:.2f}")
    print(f"共 {len(expenses)} 条记录")

def statistics_by_category():
    """功能3：按类别统计支出"""
    global expenses
    
    print("按类别统计支出")
    
    if not expenses:
        print("暂无账目记录")
        return
    
    category_stats = {}
    total_all = 0
    
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        
        # 字典操作：如果类别不存在则设为0，再加金额
        if category in category_stats:
            category_stats[category] += amount
        else:
            category_stats[category] = amount
        
        total_all += amount
    
    # 排序并输出
    print(f"\n{'类别':<10} {'支出总额':<12} {'占比':<10}")
    print("-"*40)
    
    # 将字典转换为列表并排序
    sorted_items = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_items:
        percentage = (amount / total_all * 100) if total_all > 0 else 0
        print(f"{category:<10} ¥{amount:<11.2f} {percentage:>6.1f}%")
    
    print("-"*40)
    print(f"总计：¥{total_all:.2f}")
    print(f"共 {len(category_stats)} 个类别")

def delete_expense():
    """删除账目"""
    global expenses
    
    if not expenses:
        print("暂无账目记录")
        return
    
    try:
        expense_id = int(input("请输入要删除的账目ID: "))
        
        # 查找要删除的账目
        expense_to_delete = None
        for expense in expenses:
            if expense['id'] == expense_id:
                expense_to_delete = expense
                break
        
        if expense_to_delete:
            confirm = input(f"确认删除账目 '{expense_to_delete['category']} ¥{expense_to_delete['amount']}'? (y/n): ")
            if confirm.lower() == 'y':
                # 删除账目
                new_expenses = []
                for e in expenses:
                    if e['id'] != expense_id:
                        new_expenses.append(e)
                expenses = new_expenses
                
                # 重新编号ID
                for i, expense in enumerate(expenses, 1):
                    expense['id'] = i
                
                save_expenses()
                print("账目已删除")
            else:
                print("已取消删除")
        else:
            print(f"未找到ID为 {expense_id} 的账目")
    except ValueError:
        print("请输入有效的数字ID")

def main():
    """主程序"""
    print("="*60)
    print("  欢迎使用个人记账本程序")
    print("="*60)
    
    load_expenses()
    
    while True:
        print("【主菜单】")
        print("1. 添加账目")
        print("2. 查看所有账目")
        print("3. 按类别统计")
        print("4. 删除账目")
        print("0. 退出并保存")
        print("─"*40)
        
        choice = input("请选择操作 (0-4): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            statistics_by_category()
        elif choice == '4':
            delete_expense()
        elif choice == '0':
            save_expenses()
            print("感谢使用记账本！")
            break
        else:
            print("无效选择，请重新输入")

main()
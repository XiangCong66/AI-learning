class BankAccount:
    def __init__(self,balance,name):
        self.balance = float(balance)
        self.name = name
    def deposit(self,todeoisit):
        self.balance += float(todeoisit)
        print(f"存款成功，余额{self.balance}元")
    def withdraw(self, towithdraw):
        if self.balance <  towithdraw:
            print("取款失败！余额不足！")
        else :
            self.balance -= towithdraw
            print(f"取款成功！余额{self.balance}元")
    def display(self):
        print(f"账户：{self.name},余额{self.balance}元")

name = input("输入账户名：")
balance = float(input("输入余额"))
t = int(input("输入测试次数:"))
Bank = BankAccount(balance,name)
for i in range(t):
    todo = input("请输入操作：")
    if todo == "withdraw":
        towithdraw = float(input("请输入取款金额:"))
        Bank.withdraw(towithdraw)
    elif todo == "deposit":
        todeposit = float(input("请输入存款金额:"))
        Bank.deposit(todeposit)
    elif todo == "display":
        Bank.display()
    else :
        print("无效操作！")



        
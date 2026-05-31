import random
num = random.randint(1,100)
guess = 0
time = 0
while num != guess:
    guess = int(input("请输入数字:"))
    time += 1
    if num < guess:
        print("猜大了！")
    elif num > guess:
        print("猜小了！")
    else:
        print("猜对了！")
        print("一共猜了",time,"次")
    

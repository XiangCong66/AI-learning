height = float(input("请输入身高："))
weight = float(input("请输入体重："))
BMI = weight / height / height
print("BMI为",BMI)
if BMI >= 28:
    print("肥胖！")
elif BMI >= 24:
    print("超重!")
elif BMI >= 18.5:
    print("正常!")
else:
    print("偏瘦！")
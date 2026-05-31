import random

wincom = 0
winplayer = 0

while True:
    computer = random.randint(1,3)
    player = int(input("请出拳：1石头，2剪刀，3布"))
    if player == computer:
        print("相同！")
    else:
        if (player == 1 and computer == 2) or (player == 2 and computer == 3) or (player == 3 and computer == 1):
            print("本回合，你赢了！")
            winplayer += 1
        else :
            print("本回合，你输了！")
            wincom += 1
    if wincom == 3:
        print("你输了！")
        break
    if winplayer == 3:
        print("你赢了！")
        break
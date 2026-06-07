import random
import string

def getpassword():
    password = list(string.ascii_letters + string.digits)
    while len(password) != 8:
        index = random.randint(0,len(password) -1)
        del password[index]
    random.shuffle(password)
    return ''.join(password)

password = getpassword()
print(password)
import re

text = """
Xiangcong的联系方式如下：
手机号：11451419198，备用号码：10114514111
邮箱：xiangcong@123e.com，工作邮箱：xiangcong@company.cn
出生日期：2007-04-11，入职日期：2023/11/15
身份证号：123456789011112345
另外还有：test@test.org，电话：18899998888，日期：2024.01.01
"""

phones = re.findall(r'1[3-9]\d{9}', text)
emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
dates = re.findall(r'\d{4}[-/.]\d{2}[-/.]\d{2}', text)

print(f"手机号: {phones}")
print(f"邮箱:   {emails}")
print(f"日期:   {dates}")
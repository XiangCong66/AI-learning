# 第三周
agent思考题：如果给 Agent Loop 加「记忆」功能，需要改哪里？写下思路
添加memory = []
给决策器增加memory参数
不必调用工具而直接使用memory中数据（类似缓存？）
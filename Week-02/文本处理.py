with open('Week-02/test.txt', 'r',encoding='utf-8') as file:
    text = file.read()

punctuation = '.,!?;:()[]{}"\'<>@#$%^&*=-_'
for p in punctuation:
    text = text.replace(p, ' ')

words = text.lower().split()

word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

sortedwords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
top10 = sortedwords[:10]

print("频率最高的10个单词：")
for i, (word, count) in enumerate(top10, 1):
    print(f"{i}. {word}: {count}次")
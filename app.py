from flask import Flask, render_template, request
import random
import pandas as pd

app = Flask(__name__)

# 读取CSV文件到DataFrame
# 使用 `usecols` 参数只读取第一列，假设单词在第一列
word_bank_df = pd.read_csv('word_bank.csv', header=None, usecols=[0], names=['word'])

# 确保所有数据都是字符串类型，并去除空行和空格
word_bank_df['word'] = word_bank_df['word'].astype(str).str.strip()

# 过滤掉空字符串
word_bank_df = word_bank_df[word_bank_df['word'] != '']

# 转换为小写
word_bank_df['word'] = word_bank_df['word'].str.lower()

# 将DataFrame转换为列表
word_bank = word_bank_df['word'].tolist()

# 打印单词列表以进行调试
print("Loaded words:", word_bank)

# 通用的句子模板库
sentence_templates = [
    "{{word}} is the heart of {{theme}}.",
    "In the realm of {{theme}}, {{word}} shines bright.",
    "{{word}} embodies the spirit of {{theme}}.",
    "The essence of {{word}} is deeply rooted in {{theme}}.",
    "{{word}} and {{theme}} are intertwined in a dance of life."
]

# 为每个主题选择一个通用的模板
themes = ['love', 'nature', 'life', 'joy', 'sorrow']

@app.route("/", methods=["GET", "POST"])
def index():
    poem = ""
    if request.method == "POST":
        user_input = request.form["user_input"].lower().strip()
        keywords = user_input.split()
        poem_lines = []

        for keyword in keywords:
            # 去除关键词前后的空格并转换为小写
            keyword = keyword.strip().lower()
            # 检查单词是否存在于word_bank中
            if keyword in word_bank:
                # 从模板库中随机选择一个模板
                template = random.choice(sentence_templates)
                # 为模板选择一个主题
                theme = random.choice(themes)
                # 将单词和主题插入模板
                poem_line = template.replace('{{word}}', keyword).replace('{{theme}}', theme)
                poem_lines.append(poem_line)
            else:
                poem_lines.append("No matching keyword found for: " + keyword)

        if poem_lines:
            poem = " ".join(poem_lines)
        else:
            poem = "No matching keywords found."

    return render_template("index.html", poem=poem)

if __name__ == "__main__":
    app.run(debug=True)
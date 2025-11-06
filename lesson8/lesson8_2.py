import os

# 使用names.txt的絕對路徑
current_dir = os.path.dirname(os.path.abspath("__file__"))
file_path = os.path.join(current_dir,'assets','names.txt')

with open(file_path, encoding="utf-8") as file:
    content = file.read()

names = content.split(',')
print(names)
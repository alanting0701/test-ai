import os
import random
import csv

def get_names(file_name):
    # 使用names.txt的絕對路徑
    current_dir = os.path.dirname(os.path.abspath("__file__"))
    file_path = os.path.join(current_dir,'assets',file_name)

    with open(file_path, encoding="utf-8") as file:
        content = file.read()

    return content.split('\n')

def get_scores(names, num=10):
    stu_names = random.sample(names,num)
    scores = []
    for name in stu_names:
        info = {"姓名":name,
                "國文":random.randint(50, 100),
                "英文":random.randint(50, 100),
                "數學":random.randint(50, 100)
                }
        scores.append(info)
    return scores
    
def save_csv(students,filename):
    fieldnames = students[0].keys()
    current_dir = os.path.dirname(os.path.abspath("__file__"))
    file_path = os.path.join(current_dir,'assets',filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in students:
            writer.writerow(d)

names = get_names("names.txt")
num = int(input("請輸入學生數量:"))
students = get_scores(names,num=num)
save_csv(students,'students.csv')
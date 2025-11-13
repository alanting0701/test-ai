import random
import csv

def get_names(file_path: str) -> list[str]:
    """
    傳入檔案路徑,讀取assets內的txt,並且轉換txt成為list,並傳出
    """   
    
    try:
        with open(file_path, encoding="utf-8") as file:
            content = file.read()
        return [name for name in content.split('\n') if name.strip()]
    except FileNotFoundError:
        print(f"錯誤:找不到檔案 {file_path}")
        return []

def get_scores(names: list[str], num: int = 10) -> list[dict]:
    """隨機選取學生並產生成績"""
    if num > len(names):
        print(f"警告:要求 {num} 位學生,但只有 {len(names)} 個名字,將使用全部名字")
        num = len(names)
    
    if num <= 0 or not names:
        return []
    
    stu_names = random.sample(names, num)
    scores = []
    for name in stu_names:
        info = {
            "姓名": name,
            "國文": random.randint(50, 100),
            "英文": random.randint(50, 100),
            "數學": random.randint(50, 100)
        }
        scores.append(info)
    return scores
    
def save_csv(students: list[dict], file_path: str) -> None:
    """將學生資料儲存為 CSV 檔案"""
    if not students:
        print("警告:沒有學生資料可儲存")
        return
    
    fieldnames = students[0].keys()
    

    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in students:
                writer.writerow(d)
        print(f"成功儲存 {len(students)} 筆資料到 {file_path}")
    except Exception as e:
        print(f"儲存檔案時發生錯誤: {e}")
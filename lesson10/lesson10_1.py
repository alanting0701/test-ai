import os
import tools

def get_asset_path(filename: str) -> str:
    """取得 assets 資料夾內檔案的完整路徑"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'assets', filename)



def main():
    file_path = get_asset_path("names.txt")

    names: list[str] = tools.get_names(file_path)
    
    if not names:
        print("無法讀取名單,程式結束")
        return
    
    try:
        num: int = int(input(f"請輸入學生數量(1-{len(names)}):"))
        if num <= 0:
            print("學生數量必須大於 0")
            return
    except ValueError:
        print("請輸入有效的數字")
        return
    
    students: list[dict] = tools.get_scores(names, num=num)
    file_path = get_asset_path('students.csv')
    tools.save_csv(students, file_path)

if __name__ == '__main__':
    main()
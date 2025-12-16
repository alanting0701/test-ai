import os
import pandas as pd
from pandas import DataFrame

def get_data_file_path(filename: str) -> str:
    """輸入檔案名稱,傳出目前檔案的絕對工作路徑"""
    # 取得目前工作目錄
    current_directory = os.getcwd()
    # 取得該目錄下的`data`資料夾內的`每日各站進出站人數2020.csv`檔案路徑
    file_path = os.path.join(current_directory, "data", filename)
    return file_path

def merge_station_passenger_data(filename: str) -> DataFrame:
    """
    合併每日乘客資料與車站資訊。
    
    此函數讀取每日乘客資料的 CSV 檔案，重新命名欄位為中文，
    並根據車站代碼與車站資訊（代碼、名稱、地址）進行合併。
    
    Args:
        filename (str): 每日乘客資料 CSV 檔案的檔案名稱
        
    Returns:
        DataFrame: 包含乘客資料與車站資訊的合併資料表
    """
    # 讀取每日乘客資料檔案
    file_path = get_data_file_path(filename)
    passenger_data = pd.read_csv(file_path)
    
    # 重新命名欄位為中文以保持一致性
    passenger_data_renamed = passenger_data.rename(columns={
        "trnOpDate": "乘車日期",
        "staCode": "車站代碼",
        "gateInComingCnt": "進站人數",
        "gateOutGoingCnt": "出站人數"
    })
    
    # 讀取車站資訊資料
    station_path = get_data_file_path("台鐵車站資訊.csv")
    station_data = pd.read_csv(station_path)
    
    # 從車站資料中選取需要的欄位
    station_data_filtered = station_data[['stationCode', 'stationName', 'stationAddrTw']]
    
    # 重新命名車站資料欄位為中文
    station_data_renamed = station_data_filtered.rename(columns={
        "stationCode": "車站代碼",
        "stationName": "車站名稱",
        "stationAddrTw": "車站地址"
    })
    
    # 根據車站代碼合併乘客資料與車站資訊
    merged_data = pd.merge(passenger_data_renamed, station_data_renamed, on='車站代碼', how='left')
    
    return merged_data

def get_datafolder_files() -> list[str]:
    current_directory = os.getcwd()
    # 取得該目錄下的`data`資料夾的路徑
    data_directory = os.path.join(current_directory, "data")

    # 列出data資料夾內的所有檔案,只要檔案
    # 不要使用list的comprehension寫法
    file_list = []
    for f in os.listdir(data_directory):
        if os.path.isfile(os.path.join(data_directory, f)) and "每日各站進出站人數" in f:
            file_list.append(f)
    return file_list

def main():
    # 取得所有每年乘客資料檔案名稱
    data_list:list[str] = get_datafolder_files()
    all_years_data = []
    for year_file in data_list:
        year_DataFrame = merge_station_passenger_data(year_file)
        all_years_data.append(year_DataFrame)

    final_dataFrame = pd.concat(all_years_data, ignore_index=True)
    final_dataFrame.sort_values(by=["乘車日期"],inplace=True)
    keelung_data = final_dataFrame.query("車站名稱 == '基隆'")
    keelung_data.to_excel("基隆車站每日進出站人數.xlsx", index=False)
    


if __name__ == "__main__":
    main()
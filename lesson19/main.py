import os
import pandas as pd
from pandas import DataFrame


def get_data_file_path(filename: str) -> str:
    """輸入檔案名稱,傳出目前檔案的絕對工作路徑"""
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "data", filename)
    return file_path


def merge_station_passenger_data(filename: str) -> DataFrame:
    """
    合併每日乘客資料與車站資訊。
    """
    file_path = get_data_file_path(filename)
    passenger_data = pd.read_csv(file_path)

    passenger_data_renamed = passenger_data.rename(columns={
        "trnOpDate": "乘車日期",
        "staCode": "車站代碼",
        "gateInComingCnt": "進站人數",
        "gateOutGoingCnt": "出站人數",
    })

    station_path = get_data_file_path("台鐵車站資訊.csv")
    station_data = pd.read_csv(station_path)

    station_data_filtered = station_data[['stationCode', 'stationName', 'stationAddrTw']]

    station_data_renamed = station_data_filtered.rename(columns={
        "stationCode": "車站代碼",
        "stationName": "車站名稱",
        "stationAddrTw": "車站地址",
    })

    merged_data = pd.merge(
        passenger_data_renamed,
        station_data_renamed,
        on="車站代碼",
        how="left",
    )
    return merged_data


def get_datafolder_files() -> list[str]:
    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, "data")

    file_list: list[str] = []
    for f in os.listdir(data_directory):
        if os.path.isfile(os.path.join(data_directory, f)) and "每日各站進出站人數" in f:
            file_list.append(f)
    return file_list


def all_data_concat() -> DataFrame:
    """合併所有年份乘客資料"""
    data_list: list[str] = get_datafolder_files()
    all_years_data: list[DataFrame] = []

    for year_file in data_list:
        year_df = merge_station_passenger_data(year_file)
        all_years_data.append(year_df)

    final_df = pd.concat(all_years_data, ignore_index=True)
    final_df.sort_values(by=["乘車日期"], inplace=True)
    return final_df


def main():
    data_list: list[str] = get_datafolder_files()
    all_years_data: list[DataFrame] = []

    for year_file in data_list:
        year_df = merge_station_passenger_data(year_file)
        all_years_data.append(year_df)

    final_df = pd.concat(all_years_data, ignore_index=True)
    final_df.sort_values(by=["乘車日期"], inplace=True)

    keelung_data = final_df.query("車站名稱 == '基隆'")
    keelung_data.to_excel("基隆車站每日進出站人數.xlsx", index=False)


if __name__ == "__main__":
    main()
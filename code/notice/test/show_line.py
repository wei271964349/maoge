from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time
import re
import os
import matplotlib.pyplot as plt 


# 定义函数读取文件并绘制指定币种的折线图
# 函数里面参数bottom  控制折线的Y轴是否从0开始
def plot_hourly_transaction_volume_for_symbol(symbol):   
    file_path = os.path.join(os.path.dirname(__file__), "data_save.csv")

    try:
        # 读取 CSV 文件
        df = pd.read_csv(file_path, on_bad_lines='skip')

        # 打印初始数据样例（调试用）
        print("Initial data sample:")
        print(df.head())

        # 确保时间格式正确并排序
        df['write_time'] = pd.to_datetime(df['write_time'], errors='coerce')
        df = df.dropna(subset=['write_time'])  # 删除无效时间的数据

        # 检查是否有数据
        if df.empty:
            raise ValueError("The CSV file is empty or all rows are invalid.")

        # 筛选指定币种的数据
        df = df[df['名称'] == symbol]

        # 检查是否有指定币种的数据
        if df.empty:
            raise ValueError(f"No data available for the symbol: {symbol}")

        # 提取成交额数字部分（去掉单位和货币符号）
        df['成交额'] = df['成交额'].str.extract(r'\$([\d,\.]+)')
        df['成交额'] = df['成交额'].str.replace(',', '', regex=True).astype(float)

        # 打印提取后的成交额样例（调试用）
        print("Transaction volume sample after extraction:")
        print(df['成交额'].head())

        df = df.dropna(subset=['成交额'])  # 删除无效的成交额数据

        # 按时间聚合成交额
        df.sort_values(by='write_time', inplace=True)
        hourly_data = df.groupby('write_time')['成交额'].sum()

        # 打印聚合后的数据（调试用）
        print("Hourly aggregated data:")
        print(hourly_data.head())

        # 检查是否有有效数据
        if hourly_data.empty:
            raise ValueError("No valid transaction volume data to plot.")

        # 绘制折线图
        plt.figure(figsize=(10, 6))
        plt.plot(hourly_data.index, hourly_data.values, marker='o', linestyle='-', color='b', label=f'{symbol} Hourly Transaction Volume')

        # 设置图表标题和标签
        plt.title(f"Hourly Transaction Volume for {symbol}", fontsize=16)
        plt.xlabel("Time", fontsize=12)
        plt.ylabel("Transaction Volume (USDT)", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()

        # 设置 Y 轴从 0 开始
        plt.ylim(bottom=0)

        # 显示图表
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        


plot_hourly_transaction_volume_for_symbol('PEPE')
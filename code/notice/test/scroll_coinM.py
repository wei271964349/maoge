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





# 把数据写入csv文件
def write_dataframe_to_csv(df, filename='data_save.csv', mode='a', header=False):
    """将 DataFrame 写入 CSV 文件，使用相对路径，支持追加写入，包含写入时间。"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    # 获取当前时间，并格式化为 ISO 8601 字符串
    current_time = datetime.now().isoformat() # 東八區時間，不含 Z 字尾
    df['write_time'] = current_time
    df.to_csv(filepath, mode=mode, header=header, index=False, encoding='utf-8')



# 文件列表变成用于CSV文件记录的数据 并且写入
def string_write_to_file(data_string):
    print(data_string)
    if data_string == "" :
        print("获取网页数据失败")
        return -1
    # 使用正则表达式提取数据
    pattern = r"市值排名:(\d+)名称:([\w]+)成交额:\$([\d,]+)USDT"
    matches = re.findall(pattern, data_string)

    # 转换为表格
    df = pd.DataFrame(matches, columns=["市值排名", "名称", "成交额"])
   
    
    df["成交额"] = df["成交额"].str.replace(",", "", regex=False).astype(float)
    df["成交额"] = df["成交额"] / 1000000  # 除以一百萬，轉換為百萬單位
    df = df.sort_values(by="成交额", ascending=False).reset_index(drop=True) # 重新設置索引並刪除舊索引

    # 新增「成交额排名」欄位
    df.insert(0, "成交额排名", range(1, len(df) + 1)) #在最前面插入新的一列,並給予排名

    df["成交额"] = df["成交额"].apply(lambda x: "${:,.2f} M-USDT".format(x)) # 格式化為百萬單位 M-USDT



    # 显示结果
    print(f"df得数据类型是{type(df)}")
    print(df)

    write_dataframe_to_csv(df, mode='a', header=True)
    return df





# 获取解析网页数据
def parse_data(html):
    # 启动浏览器
    driver = webdriver.Chrome()
    try :
        driver.get(html)    //打开网页
    except Exception as e:
        print("网页打不开",e)
    data_string = ''
    # 找到滚动条并不断向下滚动
    element = driver.find_element(By.TAG_NAME, "body")
    for _ in range(30):
        element.send_keys(Keys.PAGE_DOWN)
    # # 等待页面加载完成
    try :
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-936354b2-2.bOgFCq")))
    except Exception as e:
        print("找DIV卡住")

    print('找class在卡住')
    rows1 = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor:pointer']")
    rows2 = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor: pointer;']")
    rows = []
    rows.extend(rows1)
    rows.extend(rows2)
    strings = ["","市值排名","名称","价格","1小时变化","1天变化","一周变化","总市值","成交额","成交数",""]

    # 遍历每一行，打印每个单元格的内容
    for row in rows:
        # 获取该行的所有<td>元素
        index = 0
        cells = row.find_elements(By.TAG_NAME, "td")
        # print(f"type:{type(cells)}--{cells}")
        # 打印每个单元格的文本
        for cell in cells:
            cell_text = cell.text.strip()  # 获取文本并去除前后空格
            cell_class = cell.get_attribute("class")  # 获取class属性
            
            # 打印单元格的文本
            # print(f"{strings[index]}: {cell_text}")
            if strings[index] == "市值排名" :
                # print(f"{strings[index]}: {cell_text}")
                data_string += "市值排名:" + cell_text
                # print(data_string)
            if strings[index] == "名称" :
                lines = cell_text.splitlines()
                value = lines[1]
                data_string += "名称:" + value
                # print(data_string)
                # print(f"{strings[index]}: {value}")
            if strings[index] == "成交额" :
                lines = cell_text.splitlines()
                value = lines[0]+"USDT"
                # value = value.replace("$", "")
                data_string += "成交额:" + value
                # print(data_string)
                # print(f"{strings[index]}: {value}")
            index += 1
            # print(data_string)
            # data_list.append(data_string)     
        # print("-" * 20)  # 分隔线，区分不同的行
        # current_time = datetime.now()
        # print(f"当前时间{current_time}")

    # 关闭浏览器
    driver.quit()
    return data_string

while True:
    print("START")
    # ret_string = parse_data("https://coinmarketcap.com/")
    ret_string = parse_data("https://coinmarketcap.com1/")
    # parse_data("https://coinmarketcap.com/?page=2")
    print(ret_string)
    string_write_to_file(ret_string)
    time.sleep(3000)



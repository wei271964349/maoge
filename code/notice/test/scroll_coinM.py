from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import re


def string_to_list(data_string):
    # 使用正则表达式提取数据
    pattern = r"排名:(\d+)名称:([\w]+)成交额:\$([\d,]+)USDT"
    matches = re.findall(pattern, data_string)

    # 转换为表格
    df = pd.DataFrame(matches, columns=["排名", "名称", "成交额"])


    # 显示结果
    print(df)
    return df






def parse_data(html):
    # 启动浏览器
    driver = webdriver.Chrome()
    driver.get(html)
    data_string = ''
    # 找到滚动条并不断向下滚动
    element = driver.find_element(By.TAG_NAME, "body")
    for _ in range(30):
        element.send_keys(Keys.PAGE_DOWN)

    # # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-936354b2-2.bOgFCq")))


    rows1 = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor:pointer']")
    rows2 = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor: pointer;']")
    rows = []
    rows.extend(rows1)
    rows.extend(rows2)
    strings = ["","排名","名称","价格","1小时变化","1天变化","一周变化","总市值","成交额","成交数",""]

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
            if strings[index] == "排名" :
                # print(f"{strings[index]}: {cell_text}")
                data_string += "排名:" + cell_text
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

ret_string = parse_data("https://coinmarketcap.com/")
# parse_data("https://coinmarketcap.com/?page=2")
# current_time = datetime.now()
# print(f"当前时间{current_time}")
print(ret_string)
string_to_list(ret_string)
# print(data_list)


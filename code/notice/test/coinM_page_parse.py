import requests
import random
import time
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# 初始化 User-Agent 生成器
ua = UserAgent()

# 目标 URL
url = "https://coinmarketcap.com/"

# 设置请求头，使用随机 User-Agent 来模拟不同浏览器访问
headers = {
    "User-Agent": ua.random,  # 随机生成 User-Agent
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# 模拟访问，获取页面数据
def fetch_data(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果返回状态码不是 200，会抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 滚动滚轮获取更多数据
def mouse_skroll():
    # 初始化 WebDriver
    driver = webdriver.Chrome()  # 或 webdriver.Firefox()

    # 開啟網頁
    driver.get("https://www.binance.com/zh-CN/markets/overview")

    # 找到需要滾動的元素 (如果沒有特定元素，則滾動整個頁面)
    element = driver.find_element(By.TAG_NAME, "body")

    # 執行滾動操作，這裡以滾動 10 次為例
    for _ in range(10):
        element.send_keys(Keys.PAGE_DOWN)
        sleep(1)  # 等待網頁載入
    print(element.text)

# 解析网页数据
def parse_data(html):
    # mouse_skroll()
    soup = BeautifulSoup(html, "html.parser")
    
    # 根据网页的结构提取市场数据，例如数字货币的价格、24小时变动等
    # 这里需要根据实际页面的 HTML 结构来调整
    markets = []

    # 假设数据在某个特定的 div 中，你可以根据页面的实际 HTML 标签来修改
    # market_table = soup.find("div", class_="sc-936354b2-2 bOgFCq")  # 示例 class，具体需要根据页面内容调整
    market_table = soup.find_all('div', class_='sc-936354b2-2 bOgFCq')

    # print(market_table)
    # market_table = soup.find_all(class_=re.compile(r"\bbg-bg1\b"))  # 示例 class，具体需要根据页面内容调整 soup.find_all(class_=re.compile(r"\bbg-bg1\b"))
    # market_table = soup.select(".bg-bg1")  # 示例 class，具体需要根据页面内容调整
     # 找到所有 class 為 "flex-1" 的 div 元素
    # divs = market_table.find_all('div', class_='sc-b3fc6b7-0 dzgUIj')
    for element in market_table:
        divs = element.find_all('div', class_='sc-b3fc6b7-0 dzgUIj')
    # return divs
    # 將所有 div 元素的文本內容連接成一個字串
    all_text = ""
    for div in divs:
        all_text += div.text.strip()
    all_text = all_text.replace('\n', '')
    all_text = all_text.replace('%', '\n')
    return all_text


# 主函数，爬取并处理数据
def main():
    html = fetch_data(url)
    if html:
        market_data = parse_data(html)
        if market_data:
            print("获取到的市场数据：")
            # for market in market_data:
            print(market_data)
        else:
            print("没有找到有效的市场数据。")
    else:
        print("无法获取网页内容。")

    # 设置随机的请求间隔，避免频繁请求同一网站
    time.sleep(random.uniform(2, 5))  # 每次请求间隔在 2 到 5 秒之间

if __name__ == "__main__":
    main()


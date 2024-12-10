from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 启动浏览器
driver = webdriver.Chrome()
driver.get("https://coinmarketcap.com/")

# 找到滚动条并不断向下滚动
element = driver.find_element(By.TAG_NAME, "body")
for _ in range(30):
    element.send_keys(Keys.PAGE_DOWN)

# # 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-936354b2-2.bOgFCq")))

# 获取指定的元素
# elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-936354b2-2.bOgFCq")

# # 打印每个元素的文本内容
# for elem in elements:
#     text = elem.text
#     class_attr = elem.get_attribute('class')  # 获取class属性
#     print('------------------------------------')
#     print(f"Text: {text}")

# # 关闭浏览器
# driver.quit()


rows = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor:pointer']")
rows = driver.find_elements(By.CSS_SELECTOR, "tr[style='cursor: pointer;']")
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
        print(f"{strings[index]}: {cell_text}")
        index += 1
    
        
    print("-" * 20)  # 分隔线，区分不同的行
# 关闭浏览器
driver.quit()



# <div class="sc-b3fc6b7-0 dzgUIj"><span>$97,151.12</span></div>
# <span class="icon-Caret-up" style="width:12px;height:18px;display:inline-block"></span>


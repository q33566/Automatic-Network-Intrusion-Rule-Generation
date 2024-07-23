from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 设置 ChromeDriver 的路径
chrome_driver_path =  r"C:\NCU\Intern\AutomaticNetwork IntrusionRuleGeneration\chromedriver-win32\chromedriver.exe"

# 创建 ChromeDriver 服务
service = Service(chrome_driver_path)

# 创建 Chrome 驱动程序对象
driver = webdriver.Chrome(service=service)

# 打开一个网页
driver.get('https://www.google.com')
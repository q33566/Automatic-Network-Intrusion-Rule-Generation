import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from pathlib import Path

# ChromeDriver 路径
chrome_driver_path = r"C:\NCU\Intern\AutomaticNetwork IntrusionRuleGeneration\chromedriver-win32\chromedriver.exe"
# 设置 ChromeDriver
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
experiment_name = 'test'
# 遍历目录中的 .txt 文件
prompt_directory = r"C:\NCU\Intern\AutomaticNetwork IntrusionRuleGeneration\experiment\test\prompt"

output_directory = os.path.join('./experiment', experiment_name, 'output')
url = "https://chatgpt.com/g/g-df45SPLWq-2024-07-regex-finder"

# 确保输出目录存在
os.makedirs(output_directory, exist_ok=True)

# 遍历 .txt 文件
for filename in os.listdir(prompt_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(prompt_directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        driver.get(url)
        print(f"Opened URL: {url}")
        
        try:
            # 使用 WebDriverWait 等待 textarea 元素出现
            textarea = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
            print("Textarea found")
            textarea.clear()
            textarea.send_keys(content)
            textarea.send_keys(Keys.RETURN)  # 提交内容
            
            sleep(2)  # 等待返回内容加载
            
            # 获取返回的内容（假设返回内容在特定的 div 或其他标签中）
            response_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.response-selector"))  # 修改此处选择器为实际返回内容所在的元素
            )
            response_text = response_element.text
            
            # 保存返回的内容
            output_filename = f"{Path(filename).stem}_response.txt"
            output_path = os.path.join(output_directory, output_filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(response_text)
            print(f"Saved response for {filename} to {output_filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# 关闭驱动
driver.quit()

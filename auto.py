import time
import os
import requests
from time import sleep
from pathlib import Path
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def autoCall(prompt, retries=3):   
    def find_input_element():
        return driver.find_elements(By.TAG_NAME, "textarea")

    def find_code_elements():
        return driver.find_elements(By.TAG_NAME, "code")

    for attempt in range(retries):
        try:
            input_elements = find_input_element()
            if input_elements:
                input_elements[0].send_keys(prompt)
                time.sleep(2)
                input_elements[0].send_keys(Keys.ENTER)
                time.sleep(60)
                print("30 seconds wait completed.")

                code_elements = find_code_elements()
                time.sleep(10)
              
                results = ""
                for element in code_elements:
                    results += element.text + "\n"
                print("Results collected:")
                print(results)
                writeData(results)
                break
            else:
                print("No text area elements found.")
                break
        except StaleElementReferenceException as e:
            if attempt < retries - 1:
                print(f"StaleElementReferenceException encountered. Retrying... ({attempt + 1}/{retries})")
                time.sleep(2)
            else:
                print("Failed to interact with the element after several retries.")
                raise e

def writeData(results):
    with open('ans.txt', 'a') as file:
        file.write(results)

# Connect to the existing Chrome session
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

# User login manually
input("Please log in to ChatGPT and then press Enter here...")

with open('ans.txt', 'w') as file:
    pass  # Clearing the file content

experiment_name = 'test'
prompt_directory = r"/Users/jasminegau/Automatic-Network-Intrusion-Rule-Generation/experiment/6 out of 9/prompt"
output_directory = os.path.join('./experiment', experiment_name, 'output')

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Sort files in directory alphabetically
sorted_filenames = sorted(os.listdir(prompt_directory))

count = 0
for filename in sorted_filenames:
    if filename.endswith('.txt'):
        count += 1
        if count == 5:
            break
        file_path = os.path.join(prompt_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            prompt = file.read()
        print(f"Reading file: {filename}")
        
        driver.get('https://chatgpt.com/g/g-df45SPLWq-2024-07-regex-finder')  # You can replace this with any URL
        new_tab_url = 'https://chatgpt.com/g/g-df45SPLWq-2024-07-regex-finder'
        driver.execute_script(f"window.open('{new_tab_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(5)  # Wait to observe the action
        autoCall(prompt)

driver.quit()

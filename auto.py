import time
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
               time.sleep(30)
               print("30")


               input_elements = find_code_elements()
               time.sleep(10)
              
               results = ""
               for element in input_elements:
                   results += element.text + "\n"
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


# user login manually
input("Please log in to ChatGPT and then press Enter here...")


with open('ans.txt', 'w') as file:
   pass


print("start")


for i in range(2):
   print("1")
   # Open a webpage (can be any page)
   driver.get('https://chatgpt.com/g/g-dB9e8cEts-regex-helper')  # You can replace this with any URL
   print("get")
   # The URL you want to open in a new tab
   new_tab_url = 'https://chatgpt.com/g/g-dB9e8cEts-regex-helper'
   print("url")


   # Open a new tab with the specified URL
   driver.execute_script(f"window.open('{new_tab_url}', '_blank');")


   # Switch to the new tab
   driver.switch_to.window(driver.window_handles[-1])


   # Optional: Wait to observe the action
   import time
   time.sleep(5)
   autoCall("this is a test")


driver.quit()
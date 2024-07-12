import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Connect to the existing Chrome session
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)

with open('test.txt', 'r') as file:
    text_to_copy = file.read()

prompt =  "This is a test "
prompt = prompt+" [OUTPUT: "

# Wait for the user to log in manually
input("Please log in to ChatGPT and then press Enter here...")

# Now continue with the automation steps
input_elements = driver.find_elements(By.TAG_NAME, "textarea")

if input_elements:
    input_elements[0].send_keys(prompt)
    time.sleep(2)
    input_elements[0].send_keys(Keys.ENTER)
    time.sleep(10)

    input_elements = driver.find_elements(By.TAG_NAME, "p")
    time.sleep(5)
    
    results = []
    for element in input_elements:
        results.append(element.text)
    
    print(results)
else:
    print("No text area elements found.")

driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def autoCall(prompt):
    # Now continue with the automation steps
    input_elements = driver.find_elements(By.TAG_NAME, "textarea")
    if input_elements:
        input_elements[0].send_keys(prompt)
        time.sleep(2)
        input_elements[0].send_keys(Keys.ENTER)
        time.sleep(50)

        input_elements = driver.find_elements(By.TAG_NAME, "code")
        time.sleep(10)
        
        results = []
        for element in input_elements:
            lines = element.text.splitlines()
            for line in lines:
                results.append(line)
        
        writeData(results)
    else:
        print("No text area elements found.")

def writeData(results):
    with open('ans.txt', 'w') as file:
        pass

    with open('ans.txt', 'a') as file:
        file.write(' '.join(results))

# Connect to the existing Chrome session
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)

# user login manually
input("Please log in to ChatGPT and then press Enter here...")

with open('test.txt', 'r') as file:
    text_to_copy = file.read()

with open ('prompt.txt', 'r') as file:
    count = 1
    paragraph = ""
    first = True
    for line in file:
        if line == '\n' and first:
            first = False
        elif first != True:
            paragraph+=line
            if line == '\n':
                count+=1
                if count == 4:
                    print(paragraph)
                    prompt = paragraph
                    count = 1
                    paragraph = ""
                    first = True
                    autoCall(prompt)
                    break
driver.quit()

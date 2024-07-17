import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def test_click_and_release(driver):
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div/div/nav/div[1]/span[2]/button')
    ActionChains(driver)\
        .click(clickable)\
        .perform()
        
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
        file.write(' '.join(results))

# Connect to the existing Chrome session
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)

# user login manually
input("Please log in to ChatGPT and then press Enter here...")

with open('test.txt', 'r') as file:
    text_to_copy = file.read()

with open('ans.txt', 'w') as file:
    pass

lists_of_prompts = []

with open('prompt.txt', 'r') as file:
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
                    prompt = paragraph
                    count = 1
                    paragraph = ""
                    first = True
                    lists_of_prompts.append(prompt)

i = 0
for prompt in lists_of_prompts:
    i+=1
    if i == 2:
        break
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    test_click_and_release(driver)
    autoCall(prompt)

driver.quit()
## Author: Azriel Wang
## Date: 09/04/24
## CC BY 4.0
## Version: Dev/Beta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os

class_number = "12275"
course_name = "Introduction to Databases"
chrome_driver_path = "/opt/homebrew/bin/chromedriver"
text_xpath = '//*[@id="COURSE' + class_number + 'nyu"]/div[4]/span[2]'


def get_current_time():
    return datetime.now().strftime("%m/%d - %H:%M:%S")

def check_if_open(driver, text_xpath):
    try:
        text_element = driver.find_element(By.XPATH, text_xpath)
        return text_element.text == "Open"
    except Exception as e:
        print(f"Error finding or retrieving the text: {e}")
        return False

def monitor_class_status(driver, button_xpath, text_xpath):
    last_checked_time = None
    change_detected = False
    
    try:
        while True:
            try:
                button = driver.find_element(By.XPATH, button_xpath)
                button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Error finding or clicking the button: {e}")
                driver.quit()
                exit()

            is_open = check_if_open(driver, text_xpath)
            current_time = get_current_time()

            if is_open:
                print(f"{current_time}: Class is OPEN, TAKE ACTION!!!")
                change_detected = True
                for _ in range(5):
                    os.system('afplay /System/Library/Sounds/Glass.aiff')
            else:
                if not change_detected:
                    if last_checked_time is None or (datetime.now() - last_checked_time).total_seconds() >= 3000:
                        print(f"{current_time}: Still watching...")
                        last_checked_time = datetime.now()

            time.sleep(30)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user (Control-C).")

    finally:
        if driver:
            driver.quit()
        print("Browser closed and program exited.")


try:
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://sis.nyu.edu/psc/csprod/EMPLOYEE/SA/c/NYU_SR.NYU_CLS_SRCH.GBL')

    input("Press Enter after passing CAPTCHA...")
    
    try:
        input_field = driver.find_element(By.XPATH, '//*[@id="NYU_CLS_DERIVED_DESCR100"]')
        input_field.clear()
        input_field.send_keys(course_name)
        print(f"Filled {course_name}.")
    except Exception as e:
        print(f"Error finding or filling the input field: {e}")
        driver.quit()
        exit()
    
    monitor_class_status(driver, '//*[@id="BUTTON_SMALL"]', text_xpath)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if driver:
        driver.quit()
    print("Browser closed and program exited.")

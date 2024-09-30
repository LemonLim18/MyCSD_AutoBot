from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# For sending the instruction key, i.e. Enter key
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a service object that uses the chromedriver.exe
service = Service(executable_path="chromedriver.exe")
# Then, create a driver object using the chrome service
driver = webdriver.Chrome(service=service)

# driver.get("https://docs.google.com/forms/d/e/1FAIpQLSefF1Xnit9Z66bDgIfDwyZGIN663USgB-EPQvfFX8uwQS9oPA/viewform")
driver.get("https://www.google.com/")

# Wait up to 5s for the page to load, until it can retrieve the HTML element
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

# Get the HTML element using its class name
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear() # Clear the input element
# Enter the key or value into the HTML element
input_element.send_keys("tech with tim" + Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Tech With Tim"))
)

# LINK_TEXT: is
# PARTIAL_LINK_TEXT: contains
# find_element: find only one
# find_elements: find multiple
link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
link.click()

time.sleep(10)

driver.quit()
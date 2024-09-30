from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# For sending the instruction key, i.e. Enter key
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialization
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSefF1Xnit9Z66bDgIfDwyZGIN663USgB-EPQvfFX8uwQS9oPA/viewform")

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.M7eMe")),
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf"))
)

# Find the field names existing in the form

raw_field_lists_ = driver.find_elements(By.CSS_SELECTOR, "span.M7eMe")
sanitized_field_lists = [field.text for field in raw_field_lists_]
print(sanitized_field_lists)

input_element = driver.find_element(By.CSS_SELECTOR, "input.whsOnd.zHQkBf")

input_element.clear()   # Clear the input field (optional) 
input_element.send_keys("I LOVES GYATTTT")

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Tech With Tim"))
# )


# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
# link.click()

time.sleep(10)

driver.quit()


# ------------------------------------  NOTES SECTION   -----------------------------------------------------------------

# 1. 'whsOnd zHQkBf' is the short text input field's class name
# 2. CLASS_NAME only works with one classname, while CSS_SELECTOR handles multiple
# 3. presence_of_element_located does not work here as it mainly checks if the elements exist in the DOM even if it is not visible. The element might be loaded later, so it detects no presence of that element
# 4. visibility_of_element_located is preferrable as it interacts with the elements that is visible to the user
# 5. 'M7eMe' is the class name for the field name

# -----------------------------------------------------------------------------------------------------------------------



# ------------------------------------  REQUIREMENTS SECTION  -----------------------------------------------------------------

# 1. IDENTIFY THE FIELD NAMES (i.e. name, ic, matric, email)
# 2. ENTER THE VALUES ACCORDINGLY (using the send_keys)
# 3. SUBMIT THE FORM
# 4. NAVIGATE TO THE NEXT PAGE (Advanced)
# 5.

# -----------------------------------------------------------------------------------------------------------------------


# ------------------------------------  MANUAL SECTION  -----------------------------------------------------------------

# webdriver allows you to control the web browser using Python
# selenium is a web testing library that contains webdriver
# Service class from the Selenium Chrome Webdriver is like a switch to this chrome driver, allowing to start and stop the webdriver
# By class from Selenium Webdriver is used to locate the element on the web page
# Keys class from Selenium Webdriver is used to send special keystrokes like Enter
# WebDriverWait class is used to wait for a certain condition to occur before proceeding
# expected_conditions or EC is used with WebDriverWait to define a condition
# time class is commonly used to add delays in the scripting
# Service is used to initialize an executable file to become a service
# webdriver.Chrome to initialize a driver/controller to interact with Chrome using the service(chromedriver.exe) defined earlier

# -----------------------------------------------------------------------------------------------------------------------

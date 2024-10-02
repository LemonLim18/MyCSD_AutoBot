from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# For sending the instruction key, i.e. Enter key
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json

# Initialization
file_path = "info.json"
with open(file_path, "r") as file:
    json.data = json.load(file)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSefF1Xnit9Z66bDgIfDwyZGIN663USgB-EPQvfFX8uwQS9oPA/viewform")

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div > span.M7eMe")),
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf"))
)

# LOCAL JSON FILES
json_field_lists = list(json.data.keys())
# print("JSON Available Fields: ", json_field_lists) 

# GFORM FIELD NAMES
raw_field_lists_ = driver.find_elements(By.CSS_SELECTOR, "div > span.M7eMe")
gform_field_lists = [field.text for field in raw_field_lists_]
# print("GFORM Required Fields: ", gform_field_lists)  # Uncomment this later

# SANITIZED FIELD LISTS
# GFORM RESPONSE CORE FUNCTIONS
# PART 1: Collect the field names and their corresponding div id
gform_field_id_lists = []
raw_field_id_lists = driver.find_elements(By.CSS_SELECTOR, "div > span.M7eMe")
for field in raw_field_id_lists:
    field_name = field.text
    field_parent_div = field.find_element(By.XPATH, "..")  # Get the parent div of the span field
    field_div_id = field_parent_div.get_attribute("id")  # Extract the id of the parent div
    gform_field_id_lists.append({"field_name": field_name, "field_id": field_div_id, "field_value": ""})
# Print out the collected data
# for entry in gform_field_id_lists:
#     print(f"Field Name: {entry['field_name']};      Div ID: {entry['field_id']};    Field Value: {entry['field_value']}")


# PART 2: Assign the field value to the corresponding entry based on the field name
usm_email_pattern = re.compile(r'(usm|university).*email', re.IGNORECASE)

generated_answer_list = gform_field_id_lists
for answer_entry in generated_answer_list:
    for json_key in json.data.keys():
        if usm_email_pattern.search(answer_entry["field_name"]):    # if the question contains these regex
            answer_entry["field_value"] = json.data['usm_email']    # assign the answer schema with usm email
        elif json_key.lower() in answer_entry["field_name"].lower():
            answer_entry["field_value"] = json.data[json_key]
            break   # Break the loop if the key is found & go to the next answer_entry/field_value

print("\nTHIS IS THE RESPONSE ANSWER LIST!!!: \n")
print(json.dumps(generated_answer_list, indent=4)) # 'dumps' to make it more readable


# LOGGING & CHECKING PURPOSE: #Comment these if unused | Check if each JSON field value is contained within the corresponding GForm field value
# answer_list = {}
# for json_field in json_field_lists:
#     found = False
#     for gform_field in sanitized_field_lists:
#         # Rmb to convert the gform to lowercase
#         if json_field in gform_field.lower():    # If the word field is found inside the word gform_field; Iterate one json_field for every field in the gform_field_list
#             print(f"JSON Field '{json_field}' found in GForm '{gform_field}'\n")
#             answer_list[json_field] = data[json_field]
#             found = True
#             break
#         if not found:
#             print(f"The JSON field '{json_field}' is not found in the GForm at all.")
# print("\nAnswer List: ", answer_list)


# PART 3: Automatically fill the form fields
for entry in generated_answer_list:
    # print("1.", entry['field_id'])
    answer_id = entry['field_id']
    answer_value = entry['field_value']
    # Get the corresponding question based on its id
    question = driver.find_element(By.CSS_SELECTOR, f"input.whsOnd.zHQkBf[type='text'][aria-labelledby='{answer_id}']") #f-string allows the variables to be embedded into the strings and evaluated.
    question.clear()
    question.send_keys(answer_value) #Key-in the answer value

time.sleep(1.5)

# PART 4: Submit the form
submit_button = driver.find_element(By.CSS_SELECTOR, "span.l4V7wb.Fxmcue")
submit_button.click()




# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
# link.click()

time.sleep(5)

driver.quit()


# ------------------------------------  NOTES SECTION   -----------------------------------------------------------------

# 1. 'whsOnd zHQkBf' is the short text input field's class name
# 2. [] is for list, {} is for dictionary/key-value pair
# 3. 
# 4. 
# 5. 'M7eMe' is the class name for the field name
# 6. Now I collect the field names and store them in a list
# 7. So there are field names and field inputs, they are linked by id
# 8. The field names are under the <div id="X"> <span class="M7eMe"> Field Name </span> </div>
# 
# 
# Working flow:
# To enter the correct value into the correct fields, I need to know the field names,
# This prolly can be done by finding the id of the field name and then ..... 
# if field name exist in database, then check its id, then find the input field with the same id, then send the value to the field
# This would need a for loop, to check each field name
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
# CLASS_NAME only works with one classname, while CSS_SELECTOR handles multiple classnames
# presence_of_element_located does not work here as it mainly checks if the elements exist in the DOM even if it is not visible. The element might be loaded later, so it detects no presence of that element
# visibility_of_element_located is preferrable as it interacts with the elements that is visible to the user 
#  

# -----------------------------------------------------------------------------------------------------------------------

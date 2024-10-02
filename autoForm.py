from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# For sending the instruction key, i.e. Enter key
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException   # For handling the exceptions for selenium
import re
import math
import time
import random
import json

# Initialization
file_path = "info.json"
with open(file_path, "r") as file:
    json_data = json.load(file)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Simple Single Page: https://docs.google.com/forms/d/e/1FAIpQLSefF1Xnit9Z66bDgIfDwyZGIN663USgB-EPQvfFX8uwQS9oPA/viewform
# Advance Single Page: https://docs.google.com/forms/d/e/1FAIpQLSd44GLLFck_5oG_kUP2KYi2WGbgPxnK9kZpngEUV-bRi3OvjQ/viewform?usp=sf_link
# Advance Multi Page: https://docs.google.com/forms/d/e/1FAIpQLSezCQuSdrsWJ2W6OG6eW0QCIsNk0cXC6WgRI1LG0bxAa-X1mQ/viewform?usp=sf_link
# Simple Multi Page: https://docs.google.com/forms/d/e/1FAIpQLSewT-6UcISyMuZqrYPAcIo9s382MCyOmUU5EQCAj46q6nt7pQ/viewform?usp=sf_link
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSezCQuSdrsWJ2W6OG6eW0QCIsNk0cXC6WgRI1LG0bxAa-X1mQ/viewform?usp=sf_link")

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div > span.M7eMe")),
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf"))
)

# LOCAL JSON FILES (USELESS)
json_field_lists = list(json_data.keys())
# print("JSON Available Fields: ", json_field_lists) 

# GFORM FIELD NAMES (USELESS)
raw_field_lists_ = driver.find_elements(By.CSS_SELECTOR, "div > span.M7eMe")
gform_field_lists = [field.text for field in raw_field_lists_]
# print("GFORM Required Fields: ", gform_field_lists)  # Uncomment this later

while True:
    # SANITIZED FIELD LISTS
    # GFORM RESPONSE CORE FUNCTIONS
    # PART 1: Collect the gform field names/questions and their corresponding div id
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
    usm_email_pattern = re.compile(r'(usm|university).*email', re.IGNORECASE) # Match usm or university and email

    generated_answer_list = gform_field_id_lists
    for answer_entry in generated_answer_list:
        for json_key in json_data.keys():
            if usm_email_pattern.search(answer_entry["field_name"]):    # if the question contains these regex
                answer_entry["field_value"] = json_data['usm_email']    # assign the answer schema with usm email
            elif json_key.lower() in answer_entry["field_name"].lower():
                answer_entry["field_value"] = json_data[json_key]
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


# LMN: CONTINUOUSLY NAVIGATE PAGES AND FILL OUT THE FORM
# ALERT: LOOP CANNOT Start from HERE AS THE IDS WILL BE RESET AND REUSED FOR ALL INPUTS

    # PART 3: Automatically fill the form fields
    # This might not work with the field that is not type of text (e.g. radio button, checkbox, linear scale, date)
    for entry in generated_answer_list:
        # print("1.", entry['field_id'])
        answer_id = entry['field_id']
        answer_value = entry['field_value']
        # CONDITION: Only the text-type input field would be set aria-labelledby value
        # as there is no input text field for the radio button, checkbox, linear scale, date, so it's meaningless
        # and will cause error cause there is no input text field with the id of the radio button field, checkbox, linear scale, date.
        # Find the corresponding question blank based on its id
        try:
            question_blank = driver.find_element(By.CSS_SELECTOR, f"input.whsOnd.zHQkBf[type='text'][aria-labelledby='{answer_id}']") #f-string allows the variables to be embedded into the strings and evaluated.

            # Only process if the input field if found (meaning it's a text-type input field)
            if question_blank: 
                question_blank.clear()
                question_blank.send_keys(answer_value) #Key-in the answer value
        except NoSuchElementException:  # Handle the exception caused by missing element desired
            # Skip the entry if there is no text input field with the given answer_id (meaning it could be radio, checkbox, linear scale, date)
            print(f"No text input found for answer_id: {answer_id}. Skipping...")
            continue

    # PART 4: Select the top rate or rate of 5
    # Linear Scale
    # Handling Linear Scale questions
    try:
        scales_questions = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.BpKDyb[role='radiogroup']"))
        )

        for scale_question in scales_questions:
            scale_options = scale_question.find_elements(By.CSS_SELECTOR, "div.PY6Xd[jscontroller='FYWcYb'] label.T5pZmf")
            for scale_option in scale_options:
                if scale_option.text == "5":
                    scale_option.click()
                    break
    except Exception as e:
        print("No scale questions found or an error occurred while retrieving them. Skipping this section...")
        



    # PART 5: Select the correct radio option from the list that carries the same meaning or is the synonym of the answer from the schema
    # Radio (Race, University, Religion)
    # Automatically click the right radio button based on the answer
    # Radios: contains multiple radio type questions
    # Radio Options: contains the radio options for each radio question
    try:
        radios_questions = driver.find_elements(By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.cNDBpf[role='radiogroup']")
        for radio_question in radios_questions:
            # Get its question name
            radio_question_text = radio_question.find_element(By.XPATH, "../../..").find_element(By.CSS_SELECTOR, "div.M4DNQ span.M7eMe").text
            # Get its radio button/option list
            radio_options = radio_question.find_elements(By.CSS_SELECTOR, "label.docssharedWizToggleLabeledContainer.ajBQVb span")

            # LOGGING: Question and Options
            print("Radio Question: ", radio_question_text) 
            for radio_option in radio_options:
                print("Radio Option: ", radio_option.text)

            # Check which answer's field name is this radio question
            for answer_entry in generated_answer_list: # the answer list use the gform question as field_name, this is to bind it with value
                if radio_question_text.lower() == answer_entry['field_name'].lower():
                    # if found the question, then extract answer from the list as selection reference
                    answer_value = answer_entry['field_value'] # E.g. "Chinese/Cina"

            # Click the right radio button based on the answer
            found_syn = False
            for radio_option in radio_options: # Options: Chinese / Cina  or  Melayu / Malay  |   Answer: Chinese or Malay
                # Check if the answer value is a list or not
                if type(answer_value) is not list:   # if not a list but a value, just check for the option
                    if answer_value.lower() in radio_option.text.lower():
                        print("Found the matching radio option: ", answer_value)
                        radio_option.click()
                        found_syn = True
                        break
                else:  # if it is a list, iterate through the list to find the matching or synonym radio option
                    for answer_value_synonym in answer_value: 
                        if answer_value_synonym.lower() in radio_option.text.lower():
                            print("Found the matching radio option: ", answer_value_synonym)
                            radio_option.click()
                            found_syn = True
                            break
                        
            if not found_syn:
                print("There is no matching radio option for these answer values.")
    except Exception as e:
        print("No radio questions found or an error occurred while retrieving them. Skipping this section...")
        

    # PART 5: Select the desired checkbox options (For now select the first and middle one)
    # Checkbox (type list)
    try:
        checkboxes_questions = driver.find_elements(By.CSS_SELECTOR, "div.geS5n[jscontroller='sWGJ4b'] div[role='list']")

        for checkboxes_question in checkboxes_questions:
            # Cannot use the list item as it is a shared attribute for both the question list items and the checkbox list items
            checkboxes_options = checkboxes_question.find_elements(By.CSS_SELECTOR, "div.eBFwI[role='listitem'] > label.docssharedWizToggleLabeledContainer.Yri8Nb")

            # Get the count of checkbox options
            options_count = len(checkboxes_options)
            print(f"Checkbox Options Count: {options_count}")

            # Generate a random index within range of available options
            if options_count > 0:
                num_to_select = random.randint(math.ceil(options_count * 1/4), round(options_count * 3/5))     # Randomly select 1 to all the options
                print(f"Number of options to select: {num_to_select}")

                random_option_index = random.randint(0, options_count - 1)

                # Randomly select the specified number of options without repetition / Now we have a set of unique selected options
                selected_options = random.sample(checkboxes_options, num_to_select)

                # Now we should click the options based on the randomly selected set
                for checkbox_option in selected_options:
                    option_text = checkbox_option.text
                    print(f"Checkbox Option: '{option_text}' is clicked.")
                    checkbox_option.click()
    except Exception as e:
        print("No checkbox questions found or an error occurred while retrieving them. Skipping this section...")
        


    # PART 6: Select the correct dropdown option from the list
    # Dropdown
    # There will be 2 methods: 1. Find the answer based on the json data, 2. If not found, then randomly select one

    # Task: Get the dropdown question first
    # Wait until the list box exists first, before we can interact and assign it to the dropdown_expands
    try: 
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='listbox']"))
        )
        dropdown_expands = driver.find_elements(By.CSS_SELECTOR, "div[role='listbox']")
        dropdown_answer_value = None
        dropdown_answer_found = False

        for dropdown_expand in dropdown_expands:
            dropdown_question = dropdown_expand.find_element(By.XPATH, "../..").find_element(By.CSS_SELECTOR, "div[role='heading'] span.M7eMe").text
            print("\n\nDropdown Question: ", dropdown_question)
            # Dropdown Question: What gender are you
            for answer_entry in generated_answer_list:
                if answer_entry['field_name'].lower() == dropdown_question.lower():
                    print("Found relevant field name in the generated answer list")
                    print("Finding the answer value ...")
                    dropdown_answer_value = answer_entry['field_value']
                    if dropdown_answer_value:
                        print("Relevant Answer: ", dropdown_answer_value)
                        dropdown_answer_found = True
                        break
                    else:
                        print("The answer for this field name is empty")
                    break

            # time.sleep(1.5) # Give initial start delay after the answer value is found
            dropdown_expand.click() # Click the dropdown to expand
            time.sleep(1.1)    # Wait for the dropdown options to appear before making a selection

            dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")

            if dropdown_answer_found:   # if the dropdown answer found in the list, then select the dropdown option
                # dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")
                if type(dropdown_answer_value) is list:     # if the answer is a list, iterate through the list to find the matching or synonym dropdown option
                    for dropdown_option in dropdown_options:
                        for dropdown_answer_synonym in dropdown_answer_value:       # Iterate through the list of answer synonyms
                            if dropdown_answer_synonym.lower() == dropdown_option.text.lower():   # For the male, can exist in Female, use == better
                                print("Found the matching dropdown option: ", dropdown_answer_synonym)
                                dropdown_option.click()
                                break
                else:   # if the answer is not a list (Exact object value), just check for the option
                    for dropdown_option in dropdown_options:
                        if dropdown_answer_value.lower() == dropdown_option.text.lower():
                            print("Found the matching dropdown option: ", dropdown_answer_value)
                            dropdown_option.click()
                            break

            else:   # if the dropdown answer not found in the list, then randomly select one
                print("Randomly select option for the question: ", dropdown_question)
                # dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")      # This exists as a list, can use index to locate an element
                random_option_index = random.randint(1, len(dropdown_options) - 1)      # Cannot start for it becuz the default first option is 'Choose' value
                random_option_picked = dropdown_options[random_option_index]
                print("Randomly selected option: ", random_option_picked.text, "at index: ", random_option_index)
                random_option_picked.click()
    except Exception as e:
        print("No dropdown questions found or an error occurred while retrieving them. Skipping this section...")
        


    time.sleep(0.5)

    # Now locate all the dropdown options visible after expanding
    # dropdown_options = driver.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")

    # # Loop through and print all available dropdown options
    # for dropdown_option in dropdown_options:
    #     option_text = dropdown_option.text
    #     print("Dropdown Option: ", option_text)

    #     # You can modify this to click a specific option if needed
    #     if option_text == "Yes I am":  # Replace with the actual option you want to select
    #         dropdown_option.click()
    #         break



    # PART 7: Enter the Date 
    # Date
    try:
        date_questions = driver.find_elements(By.CSS_SELECTOR, "div[role='textbox'] input.whsOnd.zHQkBf")
        date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")

        for entry in generated_answer_list:
            # print("1.", entry['field_id'])
            answer_date_id = entry['field_id']
            answer_date_value = entry['field_value']


        # for date_input in date_inputs:

        #     date_input.clear()

        #     current_date = time.strftime("%d-%m-%Y")
        #     print("Current Date: ", current_date)
        #     date_input.send_keys(current_date)

            try:
                question_date_blank = driver.find_element(By.CSS_SELECTOR, f"div[aria-labelledby='{answer_date_id}'] input.whsOnd.zHQkBf[type='date']") #f-string allows the variables to be embedded into the strings and evaluated.

                # Only process if the input field if found (meaning it's a date-type input field)
                if question_date_blank: 
                    question_date_blank.clear()
                    if answer_date_value:
                        question_date_blank.send_keys(answer_date_value)
                        print("This is the birthdate: ", answer_date_value)
                    else:
                        current_date = time.strftime("%d-/%m-%Y")
                        question_date_blank.send_keys(current_date) #Key-in the current date as substitute
                        print("This is the current date: ", current_date)
            except NoSuchElementException: 
                # Skip the entry if there is no text input field with the given answer_id (meaning it could be radio, checkbox, linear scale, date)
                print(f"No date input found for answer_id: {answer_date_id}. Skipping...")
                continue
    except Exception as e:
        print("No date questions found or an error occurred while retrieving them. Skipping this section...")
        

    print("Log 1")
    time.sleep(1.2)
    print("Log 2")
    # LAST PART: Submit the form
    # Check if thre is a 'Next' button or 'Submit' button
    try:
        print("Log 3")
         # Try to find the 'Next' button first
        print("Log 4")
        next_button = driver.find_element(By.CSS_SELECTOR, "span.l4V7wb.Fxmcue").find_element(By.XPATH, "//span[text()='Next']")    # With Next value
        print("Next Button: ", next_button.text)
        next_button.click()
        time.sleep(2)  # Wait for the next page to load

    except NoSuchElementException:  # Meaning the 'Next' button is not found
        print("Next Button not found. Proceed to Submit Button.")  
        try:
            # If there is no 'Next' button, then try to find the 'Submit' button
            print("Log 5")
            print("Log 6")
            submit_button = driver.find_element(By.CSS_SELECTOR, "span.l4V7wb.Fxmcue").find_element(By.XPATH, "//span[text()='Submit']")    # With Submit value
            print("Submit button found. Clicking ", submit_button.text)
            submit_button.click()
            break   # Break the loop if the form is submitted
        except NoSuchElementException:
            print("No 'Submit' button found either. Something went wrong.")
            break   # Exit if neither button is found (you might want to handle this more gracefully)




# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
# link.click()

# time.sleep(10)

# driver.quit()


# ------------------------------------  NOTES SECTION   -----------------------------------------------------------------

# 1. 'whsOnd zHQkBf' is the short text input field's class name
# 2. [] is for list, {} is for dictionary/key-value pair
# 3. For radio, cannot use the radio id, as the answers have multiple ids, but the question has only one id
# 4. 
# 5. 'M7eMe' is the class name for the field name
# 6. Now I collect the field names and store them in a list
# 7. So there are field names and field inputs, they are linked by id
# 8. The field names are under the <div id="X"> <span class="M7eMe"> Field Name </span> </div>
#
#
# !!! CANNOT LOOP THE PROCESS FROM STEP 3, AS NAVIGATING TO OTHER MULTI-PAGE WILL RESET AND REUSE PREVIOUSLY-ASSIGNED IDS FOR ALL OF THE INPUT FIELDS !!!
# !!! THIS WILL CAUSE THE ID-BASED VALUE ASSIGNMENT TO FAIL !!!
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
# 5. Cannot start the loop for navigation from only Step 3, as the ids will be reset and reused for all inputs.

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

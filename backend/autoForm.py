from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import json
import re
import math

# Function to fill out the Google Form given its URL
def fill_google_form(url, json_data):
    # Initialization
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # # URLs for the Google Form
    # simple_single_page = "https://docs.google.com/forms/d/e/1FAIpQLSefF1Xnit9Z66bDgIfDwyZGIN663USgB-EPQvfFX8uwQS9oPA/viewform?usp=sf_link"
    # simple_multi_page = "https://docs.google.com/forms/d/e/1FAIpQLSewT-6UcISyMuZqrYPAcIo9s382MCyOmUU5EQCAj46q6nt7pQ/viewform?usp=sf_link"
    # advanced_single_page = "https://docs.google.com/forms/d/e/1FAIpQLSd44GLLFck_5oG_kUP2KYi2WGbgPxnK9kZpngEUV-bRi3OvjQ/viewform?usp=sf_link"
    # advanced_multi_page = "https://docs.google.com/forms/d/e/1FAIpQLSezCQuSdrsWJ2W6OG6eW0QCIsNk0cXC6WgRI1LG0bxAa-X1mQ/viewform?usp=sf_link"
    
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div > span.M7eMe")),
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf"))
    )

    # PART 1: Collect the gform field names/questions and their corresponding div id
    def collect_gform_fields():
        gform_field_id_lists = []
        raw_field_id_lists = driver.find_elements(By.CSS_SELECTOR, "div > span.M7eMe")
        for field in raw_field_id_lists:
            field_name = field.text
            field_parent_div = field.find_element(By.XPATH, "..")
            field_div_id = field_parent_div.get_attribute("id")
            gform_field_id_lists.append({"field_name": field_name, "field_id": field_div_id, "field_value": ""})
        return gform_field_id_lists

    # PART 2: Assign field values based on the JSON data
    def assign_field_values(gform_field_id_lists):
        usm_email_pattern = re.compile(r'(usm|university).*email', re.IGNORECASE)
        # Specifically made for ic and matric because ic exists within the matric
        ic_pattern = re.compile(r'\bic\b', re.IGNORECASE)  # Looks for 'ic' as a whole word
        matric_pattern = re.compile(r'\bmatric\b', re.IGNORECASE)  # Looks for 'matric' as a whole word
        
        for entry in gform_field_id_lists:
            for json_key in json_data.keys():
                if usm_email_pattern.search(entry["field_name"]):
                    entry["field_value"] = json_data['usm_email']
                elif ic_pattern.search(entry["field_name"]):
                    entry["field_value"] = json_data['ic']
                elif matric_pattern.search(entry["field_name"]):
                    entry["field_value"] = json_data['matric']
                elif json_key.lower() in entry["field_name"].lower():
                    entry["field_value"] = json_data[json_key]
                    break
        return gform_field_id_lists

    # PART 3: Fill text fields
    def fill_text_fields(generated_answer_list):
        for entry in generated_answer_list:
            answer_id = entry['field_id']
            answer_value = entry['field_value']
            try:
                text_input = driver.find_element(By.CSS_SELECTOR, f"input.whsOnd.zHQkBf[type='text'][aria-labelledby='{answer_id}']")
                text_input.clear()
                text_input.send_keys(answer_value)
            except NoSuchElementException:
                continue

    # PART 4: Handle Linear Scale questions
    def handle_linear_scale():
        try:
            scales_questions = driver.find_elements(By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.BpKDyb[role='radiogroup']")
            for scale_question in scales_questions:
                scale_options = scale_question.find_elements(By.CSS_SELECTOR, "div.PY6Xd[jscontroller='FYWcYb'] label.T5pZmf")
                for scale_option in scale_options:
                    if scale_option.text == "5":
                        scale_option.click()
                        break
        except NoSuchElementException:
            pass

    # PART 5: Handle Radio buttons
    def handle_radio_buttons(generated_answer_list):
        try:
            radios_questions = driver.find_elements(By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.cNDBpf[role='radiogroup']")
            for radio_question in radios_questions:
                radio_question_text = radio_question.find_element(By.XPATH, "../../..").find_element(By.CSS_SELECTOR, "div.M4DNQ span.M7eMe").text
                radio_options = radio_question.find_elements(By.CSS_SELECTOR, "label.docssharedWizToggleLabeledContainer.ajBQVb span")
                for answer_entry in generated_answer_list:
                    if radio_question_text.lower() == answer_entry['field_name'].lower():
                        print("radio question: ", radio_question_text)
                        answer_value = answer_entry['field_value']

                        # If answer_value is a list, handle it
                        if isinstance(answer_value, list):
                            matched = False  # Flag to track if a matching option is met
                            for synonym in answer_value:
                                for radio_option in radio_options:
                                    if synonym.lower() in radio_option.text.lower():
                                        print(f"Found matching radio option for synonym: {synonym}")
                                        radio_option.click()
                                        matched = True
                                        # continue
                                        break  # Exit the loop once a match is found
                                if matched:
                                    break  # Exit the outer loop if a match is found

                            # If no match is found, randomly pick an option
                            if not matched:
                                random_option = random.choice(radio_options)  # Select a random radio option
                                print(f"No matching option found. Randomly selecting: {random_option.text}")
                                random_option.click() 

                        else:
                            matched = False  # Flag to track if a matching option is found
                            for radio_option in radio_options:
                                if answer_value.lower() in radio_option.text.lower():
                                    print(f"Found matching radio option: {answer_value}")
                                    radio_option.click()
                                    matched = True
                                    # continue 
                                    break

                            # If no match is found, randomly pick an option
                            if not matched:
                                random_option = random.choice(radio_options)  # Select a random radio option
                                print(f"No matching option found. Randomly selecting: {random_option.text}")
                                random_option.click()    

        except NoSuchElementException:
            pass

    # PART 6: Handle Checkboxes
    def handle_checkboxes():
        try:
            checkboxes_questions = driver.find_elements(By.CSS_SELECTOR, "div.geS5n[jscontroller='sWGJ4b'] div[role='list']")
            for checkboxes_question in checkboxes_questions:
                checkboxes_options = checkboxes_question.find_elements(By.CSS_SELECTOR, "div.eBFwI[role='listitem'] > label.docssharedWizToggleLabeledContainer.Yri8Nb")
                if checkboxes_options:
                    num_to_select = random.randint(math.ceil(len(checkboxes_options) * 1/4), round(len(checkboxes_options) * 3/5))
                    selected_options = random.sample(checkboxes_options, num_to_select)
                    for checkbox_option in selected_options:
                        checkbox_option.click()
        except NoSuchElementException:
            pass

    # PART 7: Handle Dropdowns
    def handle_dropdowns(generated_answer_list):
        try:
            dropdown_expands = driver.find_elements(By.CSS_SELECTOR, "div[role='listbox']")
            for dropdown_expand in dropdown_expands:
                dropdown_question = dropdown_expand.find_element(By.XPATH, "../..").find_element(By.CSS_SELECTOR, "div[role='heading'] span.M7eMe").text
                print("The current dropdown question: ", dropdown_question)
                for answer_entry in generated_answer_list:
                    if answer_entry['field_name'].lower() == dropdown_question.lower():
                        dropdown_answer_value = answer_entry['field_value']
                        dropdown_expand.click()
                        time.sleep(1)
                        dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")

                        if isinstance(dropdown_answer_value, list):
                            for synonym in dropdown_answer_value:
                                for dropdown_option in dropdown_options:
                                    try:
                                        if synonym.lower() == dropdown_option.text.lower():
                                            print(f"Found matching dropdown option for synonym: {synonym}")
                                            time.sleep(1)
                                            dropdown_option.click()
                                            time.sleep(1)
                                            break  # Stop searching when a match is found
                                    except StaleElementReferenceException:
                                        print("Dropdown option reference is stale. Re-fetching options.")
                                        dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")
                        else:
                            if dropdown_answer_value:
                                for dropdown_option in dropdown_options:
                                    try:
                                        if dropdown_answer_value.lower() in dropdown_option.text.lower():
                                            print(f"Found matching dropdown option: {dropdown_answer_value}")
                                            time.sleep(1)
                                            dropdown_option.click()
                                            time.sleep(1)
                                            break  # Stop searching when a match is found
                                    except StaleElementReferenceException:
                                        print("Dropdown option reference is stale. Re-fetching options.")
                                        dropdown_options = dropdown_expand.find_elements(By.CSS_SELECTOR, "div[role='option'] span.vRMGwf.oJeWuf")
                            else:   # if there is no answer from the json file
                                print(f"Randomly selecting an option for the question: {dropdown_question}")
                                random_option_index = random.randint(1, len(dropdown_options) - 1)  # Start from 1 because index 0 is usually "Choose"
                                random_option_picked = dropdown_options[random_option_index]
                                print(f"Randomly selected option: {random_option_picked.text} at index: {random_option_index}")
                                time.sleep(1)
                                random_option_picked.click()
                                time.sleep(1)                            
        except NoSuchElementException:
            print("Dropdown not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    # PART 8: Handle Date fields
    def handle_date_fields(generated_answer_list):
        try:
            for entry in generated_answer_list:
                answer_date_id = entry['field_id']
                answer_date_value = entry['field_value']
                try:
                    date_input = driver.find_element(By.CSS_SELECTOR, f"div[aria-labelledby='{answer_date_id}'] input.whsOnd.zHQkBf[type='date']")
                    date_input.clear()
                    if answer_date_value:
                        date_input.send_keys(answer_date_value)
                    else:
                        current_date = time.strftime("%Y-%m-%d")
                        date_input.send_keys(current_date)
                except NoSuchElementException:
                    continue
        except NoSuchElementException:
            pass

    # Part 9: Navigation / Check for Next or Submit button 
    def navigate_next_or_submit():
        try:
            next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
            return False  # Continue if there's another page
        except NoSuchElementException:
            try:
                submit_button = driver.find_element(By.XPATH, "//span[text()='Submit']")
                time.sleep(0.7)
                submit_button.click()
                return True  # Stop the loop, as the form is submitted
            except NoSuchElementException:
                return True  # Stop if neither button is found
            

    # Main loop for filling the form
    while True:
        # Collect fields on the current page
        gform_field_id_lists = collect_gform_fields()

        # Assign values based on the json data
        generated_answer_list = assign_field_values(gform_field_id_lists)

        # Call appropriate functions based on page content
        fill_text_fields(generated_answer_list)
        handle_linear_scale()
        handle_radio_buttons(generated_answer_list)
        handle_checkboxes()
        handle_dropdowns(generated_answer_list)
        handle_date_fields(generated_answer_list)

        # Check if there is a 'Next' or 'Submit' button to continue or finish
        if navigate_next_or_submit():
            break  # Exit the loop if the form is submitted

    time.sleep(1)
    driver.quit()

# Avoid the script from running when imported
if __name__ == "__main__":
    with open("info.json", "r") as file:
        json_data = json.load(file)
    # The URL and json data here are locally independent testing sample; if called from telebot.py, the URL and json data will be passed from the telebot.py
    fill_google_form("https://docs.google.com/forms/d/e/1FAIpQLSd44GLLFck_5oG_kUP2KYi2WGbgPxnK9kZpngEUV-bRi3OvjQ/viewform?usp=sf_link", json_data)




# --------------------- TESTING ----------------------------------

# RECORD OF TIME
# Without Detection of Question Types:
# 1. Simple Single Page:  2.694812297821045 seconds
# 2. Simple Multi Page: 6.691177845001221 seconds
# 3. Advanced Single Page: 9.720359802246094 seconds
# 4. Advanced Multi Page: 17.663202047348022 seconds

# With Detection of Question Types:
# 1. Simple Single Page: 2.4234766960144043 seconds
# 2. Simple Multi Page: 6.756955623626709 seconds
# 3. Advanced Single Page: 9.771028518676758 seconds
# 4. Advanced Multi Page: 18.024168968200684 seconds

# ------------------ END OF TESTING -----------------------------


# ------------------ FUNCTIONS --------------------------------------

# Add the detection method by replacing the 
#   fill_text_fields(generated_answer_list)
        # handle_linear_scale()
        # handle_radio_buttons(generated_answer_list)
        # handle_checkboxes()
        # handle_dropdowns(generated_answer_list)
        # handle_date_fields(generated_answer_list)
#
#  
# Detect question types (DETECTION METHOD)
        # question_types = detect_question_types()

        # # Only call the relevant functions based on detected question types
        # if question_types['text']:
        #     fill_text_fields(generated_answer_list)
        # if question_types['linear_scale']:
        #     handle_linear_scale()
        # if question_types['radio']:
        #     handle_radio_buttons(generated_answer_list)
        # if question_types['checkbox']:
        #     handle_checkboxes()
        # if question_types['dropdown']:
        #     handle_dropdowns(generated_answer_list)
        # if question_types['date']:
        #     handle_date_fields(generated_answer_list)

# 
# PART 9: Detect question types on the page
# def detect_question_types():
    # question_types = {
        # 'text': False,
        # 'linear_scale': False,
        # 'radio': False,
        # 'checkbox': False,
        # 'dropdown': False,
        # 'date': False
    # }
    # 
    # try:
        # Detect text input fields
        # if driver.find_elements(By.CSS_SELECTOR, "input.whsOnd.zHQkBf[type='text']"):
            # question_types['text'] = True
        # 
        # Detect linear scale questions
        # if driver.find_elements(By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.BpKDyb[role='radiogroup']"):
            # question_types['linear_scale'] = True
        # 
        # Detect radio buttons
        # if driver.find_elements(By.CSS_SELECTOR, "div.lLfZXe.fnxRtf.cNDBpf[role='radiogroup']"):
            # question_types['radio'] = True
        # 
        # Detect checkboxes
        # if driver.find_elements(By.CSS_SELECTOR, "div.geS5n[jscontroller='sWGJ4b'] div[role='list']"):
            # question_types['checkbox'] = True
        # 
        # Detect dropdowns
        # if driver.find_elements(By.CSS_SELECTOR, "div[role='listbox']"):
            # question_types['dropdown'] = True
        # 
        # Detect date input fields
        # if driver.find_elements(By.CSS_SELECTOR, "input.whsOnd.zHQkBf[type='date']"):
            # question_types['date'] = True
    # 
    # except NoSuchElementException as e:
        # print(f"Error detecting question types: {e}")
    # 
    # return question_types
#    

# ------------------ END OF NOTES -------------------------------
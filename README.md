# MyCSD_Autofiller
**MyCSD_Autofiller** is an intelligent automation tool powered by Python and Selenium, designed to streamline the process of filling out Google Forms. With data pulled from a local JSON file, the tool dynamically matches form fields to their respective IDs, ensuring accurate and efficient input. But that’s not all – it takes automation to the next level by instantly capturing the form URL as soon as a Telegram notification pops up, identifying the required fields, and seamlessly populating them with the relevant data from the JSON file.

## Features
- **Automatically** fill in Google Forms with data from a JSON file.
- Matches form fields using **field names and unique IDs**.
- Supports input fields such as text (e.g., name, IC number, telephone number, email).
- Ensures the **required fields** in the form match the data in the JSON file.
- Handles **partial matches** (e.g., form fields partially pre-filled).

## Prerequisites
To use **MyCSD_Autofiller**, you need the following installed on your system:

- **Python 3.x**
- **Google Chrome**
- **ChromeDriver (Make sure the ChromeDriver version matches your Chrome browser version)**
- **Python libraries:**
  - `selenium`
  - `json`
  - `time`

**Install required Python packages using:**
```python
pip install selenium
```

# Setup and Configuration
1. ### Clone the Repository
Clone this repository to your local machine:

```python
git clone https://github.com/LemonLim18/MyCSD_Autofiller.git
```
2. ### Setup ChromeDriver
Download the appropriate version of ChromeDriver and place it in the project directory or set it in your PATH.

In the Python script, update the ChromeDriver path in the code:

```python
service = Service(executable_path="path_to_your_chromedriver")
driver = webdriver.Chrome(service=service)
```

3. ### JSON Data
Ensure the local JSON file follows this structure to map the required form fields correctly:

```python
{
    "name": "Lim Miin Ning",
    "ic": "030118020451",
    "tel": "011-15411073",
    "matric": "163133",
    "email": "limmiinning@gmail.com",
    "usm_email": "limmiinning@student.usm.my"
}
```

4. ### Script Overview
The main script performs the following actions:

1. **Load JSON Data**: Loads the input data from a local JSON file.
2. **Open Google Form**: Opens the specified Google Form using Selenium.
3. **Match Fields**: Finds form fields using their CSS Selectors (e.g., field names and IDs).
4. **Fill Form Fields**: Automatically fills each form field with the corresponding value from the JSON data.
5. **Submit the Form (Optional)**: Optionally, submit the form if required.

## Sample Code
Here’s a brief look at the automation process in the script:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Setup Chrome WebDriver
service = Service(executable_path="path_to_your_chromedriver")
driver = webdriver.Chrome(service=service)

# Open Google Form
form_url = "https://docs.google.com/forms/d/e/your_form_id/viewform"
driver.get(form_url)

# Locate and fill form fields
for field in data.keys():
    field_element = driver.find_element(By.CSS_SELECTOR, f"input[name='{field}']")
    field_element.send_keys(data[field])

# Optionally submit the form
# driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

driver.quit()
```

## Run the Script
Run the Python script from your terminal:

```python
python autoForm.py
```

The script will automatically open the form, locate the fields by their names and IDs, and fill them with the data from the JSON file.

## How It Works
- **Field Name Matching**: The script retrieves field names from the form using CSS Selectors. It matches these fields with the corresponding keys in the JSON data.
- **Error Handling**: If a required field is missing in the JSON file or the form contains unexpected fields, the script will handle it gracefully.
- **Flexible Field Matching**: The script can handle partial form entries (e.g., if some fields are already pre-filled).
 
## Limitations
- The tool currently supports only **text input fields**.
- It assumes that the JSON file will contain all the necessary data for the Google Form fields.
- If the Google Form layout changes, the **CSS Selectors** may need to be updated.

## Future Improvements
Add support for other input types (e.g., radio buttons, dropdowns).
Add a mechanism to dynamically handle form changes.
Include options for user interaction, such as reviewing the form before submission.

## Contributing
Feel free to submit issues or pull requests if you find any bugs or want to contribute to the project.

License
This project is open-source and available under the **MIT License**.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# get user input of book to check
book = input("Enter book name: ")

url = "https://www.readings.com.pk/"

options = Options()
options.add_argument("-headless")  # run Firefox in headless mode
service = Service("geckodriver-v0.33.0-win64")  # path to gecko webdriver
driver = webdriver.Firefox(service=service, options=options)

driver.get(url)

# find the search input element
search_input = driver.find_element(By.ID, "Search")

# set the value of the search input to the book name
driver.execute_script("arguments[0].value = arguments[1];", search_input, book)

# get the JavaScript function call from the input element's onclick attribute
onkeypress_value = search_input.get_attribute("onkeypress")

if onkeypress_value:
    # extract the JavaScript function name and parameters from the onclick value
    function_name = onkeypress_value.split("(")[0]
    function_params = onkeypress_value.split("(")[1].split(")")[0]

    # create the JavaScript function call with the book name as the parameter
    javascript_call = f'{function_name}("{function_params}", "{book}");'

    # execute the JavaScript function call
    driver.execute_script(javascript_call)

else:
    print("No search function found.")

# print the current URL to verify if the search was successful
print(driver.current_url)

driver.quit()

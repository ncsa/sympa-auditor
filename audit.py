# audit.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dataclasses import dataclass, asdict
import json
from pathlib import Path


# GLOBAL VARIABLES
MAILING_LIST_URL = 'https://lists.ncsa.illinois.edu'
COOKIES_FILE = 'cookies.pkl'
OUTPUT_FILE = 'output.json'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' 

@dataclass
class EmailList:
    list_name: str
    info: str
    subscribe: str
    add: str
    unsubscribe: str
    delete: str
    invite: str
    remind: str
    review: str

def connect():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument(f"--user-agent={USER_AGENT}")
    
    driver = webdriver.Chrome(options=options)

    driver.get(MAILING_LIST_URL)

    driver.delete_all_cookies()
    
    if not Path(COOKIES_FILE).exists():
        print(f"{COOKIES_FILE} doesn't exist")
        get_cookies(MAILING_LIST_URL)

    # Load cookies
    with open(COOKIES_FILE, 'rb') as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        copy_cookie = cookie.copy()
        try:
            copy_cookie.pop('sameSite')
            driver.add_cookie(copy_cookie)
        except Exception as e:
            print(f"Error adding cookie: {cookie['name']} - {e}")
    return driver

def get_cookies(url):
    # Start a Selenium session
    driver = webdriver.Chrome()

    # Open the login page
    driver.get(url)

    # Pause to let you log in manually
    print("Log in manually, then press ENTER here...")
    input()

    # Save cookies to a file
    with open(COOKIES_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

    print("Cookies saved!")
    driver.quit()

def get_all_lists(driver):
    res = list()
    url = f"{MAILING_LIST_URL}/lists/lists"
    driver.get(url)

    element = driver.find_elements('css selector', 'li.listenum > a')
    for item in element:
        res.append(item.text)
    return res
    
def get_list_option(driver, option):
    selection = f"param.{option}"
    select_element = driver.find_element(By.ID, selection)

    select = Select(select_element)

    # Get the currently selected option
    selected_option = select.first_selected_option
    return selected_option.get_attribute("value")

def get_list_metadata(driver, list_name):
    list_name = list_name.split('@')[0]
    res = dict()
    url = f"{MAILING_LIST_URL}/lists/edit_list_request/{list_name}/command"
    driver.get(url)

    time.sleep(1)
    list_info = EmailList(
        list_name = list_name,
        info = get_list_option(driver, 'info'),
        add = get_list_option(driver, 'add'),
        subscribe = get_list_option(driver, 'subscribe'),
        unsubscribe = get_list_option(driver, 'unsubscribe'),
        delete = get_list_option(driver, 'del'),
        invite = get_list_option(driver, 'invite'),
        remind = get_list_option(driver, 'remind'),
        review = get_list_option(driver, 'review'),
    )
    return list_info

def dump_list_metadata(path, all_list_metadata):
    data = dict()
    for list_entry in all_list_metadata:
        data[list_entry.list_name] = asdict(list_entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    # Connect to lists.ncsa.illinois.edu
    driver = connect()

    # Get all lists
    all_lists = get_all_lists(driver)

    # Get list metadata
    all_list_metadata = list()
    for list_name in all_lists:
        all_list_metadata.append(get_list_metadata(driver, list_name))
    
    # Dumps data to json file
    dump_list_metadata(OUTPUT_FILE, all_list_metadata)

    driver.quit()

if __name__ == '__main__':
    main()

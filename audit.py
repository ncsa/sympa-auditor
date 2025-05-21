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
import argparse
import os
from collections import defaultdict

# GLOBAL VARIABLES
MAILING_LIST_URL = ''
COOKIES_FILE = 'cookies.pkl'
OUTPUT_FILE = ''
USER_AGENT = '' 

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
        print(cookie)
        copy_cookie = cookie.copy()
        try:
            # copy_cookie.pop('sameSite')
            driver.add_cookie(copy_cookie)
        except Exception as e:
            print(f"Error adding cookie: {cookie['name']} - {e}")
    return driver

def connect_with_session(sympa_session):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument(f"--user-agent={USER_AGENT}")
    
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',  # Selenium host & port
        options=options
    )

    driver.get(MAILING_LIST_URL)
    
    driver.delete_all_cookies()

    cookies = [{
        'domain': 'lists.ncsa.illinois.edu',
        'httpOnly': True,
        'name': 'sympa_session',
        'path': '/',
        'sameSite': 'Lax',
        'secure': True,
        'value': sympa_session
    }]

    for cookie in cookies:
        copy_cookie = cookie.copy()
        try:
            driver.add_cookie(copy_cookie)
        except Exception as e:
            print(f"Error adding cookie: {cookie['name']} - {e}")
    return driver

def get_all_lists(driver):
    res = list()
    url = f"{MAILING_LIST_URL}/lists/lists"
    driver.get(url)

    element = driver.find_elements('css selector', 'li.listenum > a')
    for item in element:
        res.append(item.text)

    if len(res) != 0:
        print("Success")
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

def dump_to_file(all_list_metadata):
    data = dict()
    for list_entry in all_list_metadata:
        data[list_entry.list_name] = asdict(list_entry)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def dump_to_console(all_list_metadata):
    data = dict()
    for list_entry in all_list_metadata:
        data[list_entry.list_name] = asdict(list_entry)
    output = json.dumps(data)
    print(output)

def categorize_data():

    with open(OUTPUT_FILE, "r") as f:
        data = json.load(f)

    res = defaultdict(lambda: defaultdict(list))
    for list_name, list_entry in data.items():
        for option, selection in list_entry.items():
            if option == 'list_name': continue

            res[option][selection].append(list_name)

    with open(CATEGORIZE_FILE, 'w') as f:
        json.dump(res, f, indent=2)

def parse_args():
    parser = argparse.ArgumentParser(description="Get symmpa_session")
    parser.add_argument("-s", "--sympa_session", type=str, default='', help="sympa_session cookie for logged in session. Outputs a file with list names and their configurations")
    parser.add_argument("-o", "--console", action='store_true', help="Dump list metatdata to console")
    parser.add_argument("-c", "--categorize", action='store_true', help="Structure list items by their options. Ouputs a file categorize by configurations")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    driver = connect_with_session(args.sympa_session)

    # Get all lists
    all_lists = get_all_lists(driver)

    # Get list metadata
    all_list_metadata = list()
    for list_name in all_lists:
        all_list_metadata.append(get_list_metadata(driver, list_name))  

    # Dumps data
    if args.console:
        dump_to_console(all_list_metadata)
    else:
        dump_to_file(all_list_metadata)

    driver.quit()

    if args.categorize:
        categorize_data()

if __name__ == '__main__':
    # Loading in Environment variables
    MAILING_LIST_URL = os.getenv('MAILING_LIST_URL')
    OUTPUT_FILE = os.getenv('OUTPUT_FILE')
    CATEGORIZE_FILE = os.getenv('CATEGORIZE_FILE')
    USER_AGENT = os.getenv('USER_AGENT')

    main()
    

# save_cookies.py
from selenium import webdriver
import pickle
import time

# Start a Selenium session
driver = webdriver.Chrome()

# Open the login page
driver.get("https://lists.ncsa.illinois.edu")

# Pause to let you log in manually
print("Log in manually, then press ENTER here...")
input()

# Save cookies to a file
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("Cookies saved!")
driver.quit()

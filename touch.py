from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

def human_touch(link):
    print("it is touching")

    # Specify the path to geckodriver if needed
    service = Service('/path/to/geckodriver')  # Update the path if necessary
    driver = webdriver.Firefox(service=service)

    # Navigate to the initial URL
    driver.get(link)

    # Wait for the "Continue to your image" link to appear
    time.sleep(4)

    # Find the "Continue to your image" link and click it
    continue_link = driver.find_element(By.LINK_TEXT, "Continue to your image")
    continue_link.click()

    # Wait for the image to load
    time.sleep(4)

    # After clicking, extract the image URL
    img_tag = driver.find_element(By.CLASS_NAME, 'main-image')
    high_res_url = img_tag.get_attribute('src')
    print("High-resolution image URL:", high_res_url)

    # Don't forget to close the browser when done
    driver.quit()

human_touch('https://www.imagebam.com/image/fc69ec891356554')

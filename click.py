from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_and_return(url):
    # Set up Firefox options
    firefox_options = webdriver.FirefoxOptions()

    # Start a new Firefox session
    driver = webdriver.Firefox(options=firefox_options)

    try:
        # Navigate to the page
        driver.get(url)

        # Wait until the "Continue to your image" link is clickable and then click it
        try:
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#continue a'))
            )
            continue_button.click()
            print("Link clicked successfully.")
        except Exception as e:
            print("Failed to click the link:", e)
            return None

        # Wait for the image to load and retrieve its URL
        try:
            img_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img.main-image'))
            )
            img_url = img_element.get_attribute('src')
            print("Image URL:", img_url)
            return img_url
        except Exception as e:
            print("Failed to retrieve the image URL:", e)
            return None

    finally:    
        # Close the browser
        driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By

# Connect to the existing ChromeDriver instance
driver = webdriver.Remote(command_executor='http://127.0.0.1:9515', options=webdriver.ChromeOptions())

# Example usage
driver.get('https://www.imagebam.com/image/e5a54f891357694')

# Wait until the "Continue to your image" link is clickable and click it
continue_button = driver.find_element(By.LINK_TEXT, 'Continue to your image')
continue_button.click()

# Wait until the image is loaded and then get its URL
img_element = driver.find_element(By.TAG_NAME, 'img')
img_url = img_element.get_attribute('src')
print("Image URL:", img_url)

# Close the browser (optional)
driver.quit()

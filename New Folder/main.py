import requests
from bs4 import BeautifulSoup

def scrape_image_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve content from {url}")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags that contain an <img> tag
    image_page_links = []
    for a_tag in soup.find_all('a', href=True):
        if a_tag.find('img'):
            image_page_links.append(a_tag['href'])
    
    return image_page_links

def scrape_final_image_src(image_page_url):
    # Send a GET request to the image page URL
    response = requests.get(image_page_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve content from {image_page_url}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <img> tag with id 'main-image' or whatever unique identifier it has
    img_tag = soup.find('img', id='main-image')  # Assuming the image has an id 'main-image'
    
    if img_tag:
        print(img_tag['src'])
        return img_tag['src']
    else:
        print(f"Image not found on page {image_page_url}")
        return None

def main_scraper(start_url):
    # Step 1: Scrape the initial set of links from the main page
    image_page_links = scrape_image_links(start_url)

    # Step 2: Follow each link and scrape the image src
    final_image_sources = []
    for link in image_page_links:
        final_image_src = scrape_final_image_src(link)
        if final_image_src:
            final_image_sources.append(final_image_src)
    
    return final_image_sources

# Example usage
start_url = input("url: ")  # Replace with the URL of the page you want to scrape
final_image_sources = main_scraper(start_url)

for img_src in final_image_sources:
    print(img_src)

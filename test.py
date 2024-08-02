#! /usr/bin/env python

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all anchor elements with class 'rel-link' on the page
    image_links = soup.find_all('a', class_='rel-link')
    
    # Create a folder to store downloaded images
    folder_name = input("Enter folder name for downloaded images: ")
    os.makedirs(folder_name, exist_ok=True)
    
    # Download and save each image
    for link in image_links:
        # Get the URL of the image
        image_url = link['href']
        
        # Check if the image URL ends with '.jpg'
        if image_url.endswith('.jpg'):
            # Send a GET request to the image URL
            image_response = requests.get(image_url)
            
            # Extract the image filename
            filename = os.path.join(folder_name, os.path.basename(image_url))
            
            # Save the image to the folder
            with open(filename, 'wb') as f:
                f.write(image_response.content)
                print(f"Downloaded: {filename}")

# Ask the user for the URL of the website
website_url = input("Enter the URL of the website: ")

# Call the function to download images
download_images(website_url)

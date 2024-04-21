#! /usr/bin/env python 

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def download_images(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the page to create a folder
        title = soup.title.string.strip()
        folder_name = title.replace(" - PornPics.com", '')
        folder_name = "/home/adam178/.pornpics/" + folder_name
        
        # Create a folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # Find all elements with class 'rel-link'
        rel_links = soup.find_all(class_='rel-link')
        
        # Download each JPG image
        for rel_link in rel_links:
            # Get the href attribute containing the image URL
            img_url = rel_link['href']
            
            # Check if the URL is relative or absolute
            if not bool(urlparse(img_url).netloc):
                img_url = url + img_url
            
            # Check if the image is a JPG
            if img_url.endswith('.jpg'):
                # Get the filename from the URL
                img_name = os.path.basename(img_url)
                
                # Get the image content
                img_response = requests.get(img_url)
                
                # Check if the request was successful
                if img_response.status_code == 200:
                    # Save the image to the folder
                    with open(os.path.join(folder_name, img_name), 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"Downloaded: {img_name}")
                else:
                    print(f"Failed to download image from {img_url}")
    else:
        print("Failed to retrieve page content.")

# Ask the user for the URL
url = input("Enter the URL to scrape images from: ")

# Call the function to download images
download_images(url)


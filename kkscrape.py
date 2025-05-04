#!/usr/bin/env python

import os
import requests
from bs4 import BeautifulSoup
import time
import pyfiglet
from termcolor import colored
import math
import tkinter as tk
from tkinter import messagebox
from urllib.parse import urlparse
import json
import logging
from pathlib import Path
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/aiden178/.config/kkscrape/kkscrape.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
CONFIG_DIR = Path('/home/aiden178/.config/kkscrape')
DOWNLOADED_URL_FILE = CONFIG_DIR / 'downloaded_url.txt'
SAVE_BASE_DIR = Path("/home/aiden178/Pictures/.kkscrape/")

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def get_state_file(save_folder):
    """Get the path to the state file within the download folder."""
    return save_folder / ".download_state.json"

def get_unique_filename(directory, filename):
    """Check if a file exists and, if it does, find a unique filename by appending an incrementing suffix."""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    # Loop until we find a unique filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}-{counter}{ext}"
        counter += 1

    return new_filename

def create_ascii(site):
    # Create ASCII art
    ascii_art = pyfiglet.figlet_format(site, font="slant")
    colored_ascii_art = colored(ascii_art, color="cyan")
    print(colored_ascii_art)

def load_state(save_folder):
    """Load the download state from the state file if it exists."""
    state_file = get_state_file(save_folder)
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load state file: {e}")
            return {}
    return {}

def save_state(save_folder, state):
    """Save the current download state to the state file."""
    state_file = get_state_file(save_folder)
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f)
    except IOError as e:
        logger.error(f"Failed to save state file: {e}")

def clear_state(save_folder):
    """Clear the download state."""
    state_file = get_state_file(save_folder)
    if state_file.exists():
        try:
            state_file.unlink()
            logger.info("Download state cleared.")
        except IOError as e:
            logger.error(f"Failed to clear state file: {e}")

def download_with_retry(url, headers, max_retries=3, timeout=10):
    """Download content with retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed for {url}. Retrying in {wait_time} seconds... Error: {e}")
                time.sleep(wait_time)
            else:
                raise
    return None

def process_image_link(link, headers, save_folder, existing_files, state, count, total_images):
    """Process an individual image link with retry logic."""
    redirect_url = link.get('href')
    high_res_url = ""
    
    try:
        # Get the redirected page
        redirect_response = download_with_retry(redirect_url, headers)
        if not redirect_response:
            logger.error(f"Failed to process redirect URL after retries: {redirect_url}")
            return None, False  # Return False to indicate failure

        # Parse the redirected page's HTML
        redirect_soup = BeautifulSoup(redirect_response.text, 'html.parser')

        # Get the hostname of the redirected URL
        parsed_url = urlparse(redirect_url)
        hostname = parsed_url.hostname
        logger.info(f"Host name is {hostname}")

        if hostname is None:
            logger.warning(f"Invalid URL with no hostname: {redirect_url}")
            return None, False

        # Handle different image hosts
        if "imagetwist.com" in hostname:
            high_res_link = redirect_soup.find('a', {'data-fancybox': 'gallery'})
            if high_res_link:
                high_res_url = high_res_link.get('href')

        elif "imgspice.com" in hostname:
            img_tag = redirect_soup.find('img', id='imgpreview')
            if img_tag:
                high_res_url = img_tag.get('src')

        elif "turboimagehost.com" in hostname:
            img_tag = redirect_soup.find('img', id='imageid')
            if img_tag:
                high_res_url = img_tag.get('src')

        elif "imagebam.com" in hostname:
            img_tag = redirect_soup.find('img', class_='main-image')
            if img_tag:
                high_res_url = img_tag.get('src')

        else:
            logger.warning(f"Unhandled hostname: {hostname}")
            return None, False

        if not high_res_url:
            logger.warning("Skipping this link. Probably dead image")
            return None, False

        # Get the unique filename in the target directory
        img_name = get_unique_filename(save_folder, os.path.basename(high_res_url))

        # Skip downloading if the image already exists
        if img_name in existing_files:
            logger.info(f"Image already exists, skipping: {img_name}")
            return None, True  # Return True to indicate this was a "successful" skip

        # Download the high-resolution image
        img_start_time = time.time()
        img_response = download_with_retry(high_res_url, headers)
        if not img_response:
            logger.error(f"Failed to download image after retries: {high_res_url}")
            return None, False

        img_path = os.path.join(save_folder, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
            logger.info(f"\033[1;32;40mImage saved: {img_path}\033[0m")

        # Update state after successful download
        state['last_successful_url'] = redirect_url
        state['last_successful_count'] = count
        save_state(save_folder, state)

        # Calculate and display ETA
        elapsed_time_per_image = time.time() - img_start_time
        images_remaining = total_images - count
        eta_seconds = images_remaining * elapsed_time_per_image
        eta_minutes = eta_seconds // 60
        eta_seconds = eta_seconds % 60

        logger.info(f"\033[34mProgress: {count}/{total_images}\033[0m")
        logger.info(f"ETA: {int(eta_minutes)} minutes, {int(eta_seconds)} seconds remaining")

        return {
            'url': high_res_url,
            'path': img_path,
            'time': time.time() - img_start_time
        }, True

    except Exception as e:
        logger.error(f"Error processing image link {redirect_url}: {e}")
        return None, False

def show_popup(message):
    """Show a popup notification."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Download Status", message)
    root.destroy()

def handle_interrupt(save_folder, state):
    """Handle interrupt signal by saving state."""
    logger.info("\nDownload interrupted by user. Saving state...")
    save_state(save_folder, state)
    exit(1)

def main():
    url = input("Enter the kitty-katz url to scrape: ")
    logger.info(f"URL: {url}")

    # Check if the URL has already been processed
    if not DOWNLOADED_URL_FILE.exists():
        DOWNLOADED_URL_FILE.touch()

    with open(DOWNLOADED_URL_FILE, 'r') as f:
        downloaded_urls = f.read().splitlines()

    if url in downloaded_urls:
        logger.info(f"URL '{url}' has already been processed. Exiting.")
        exit()

    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Extract folder name from the last segment of the URL
    folder_name = url.rstrip('/').split('/')[-1]
    save_folder = SAVE_BASE_DIR / folder_name

    # Create the folder if it doesn't exist
    save_folder.mkdir(parents=True, exist_ok=True)

    # List of already downloaded image filenames
    existing_files = os.listdir(save_folder)

    # Load previous state if exists
    state = load_state(save_folder)
    state['current_url'] = url  # Always update current URL
    resume_mode = False
    
    if 'last_successful_url' in state:
        resume_mode = True
        logger.info("Resuming from previous download...")

    # Set up interrupt handler
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(save_folder, state))

    # Send request to the main page
    try:
        logger.info("Sending request to main page...")
        response = download_with_retry(url, headers)
        if not response:
            logger.error("Failed to download main page after retries.")
            exit()
        logger.info("Request successful!")
    except Exception as e:
        logger.error(f"Error during request: {e}")
        exit()

    # Parse the main page's HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image containers
    logger.info("Finding image containers...")
    image_containers = soup.find_all('div', class_='bbWrapper')
    logger.info(f"Found {len(image_containers)} image containers.")

    # List to store high-resolution image URLs
    high_res_images = []
    start_time = time.time()
    total_images = 0
    processed_images = 0

    # Count total images first
    for container in image_containers:
        total_images += len(container.find_all('a', class_='link--external'))

    # Loop through each container to extract image URLs
    for container in image_containers:
        image_links = container.find_all('a', class_='link--external')

        for count, link in enumerate(image_links, start=1):
            redirect_url = link.get('href')
            
            # Skip already processed links in resume mode
            if resume_mode:
                if 'last_successful_url' in state and state['last_successful_url'] == redirect_url:
                    logger.info(f"Resuming from last successful URL: {redirect_url}")
                    resume_mode = False  # Next links are new
                    continue
                elif resume_mode:
                    logger.info(f"Skipping already processed URL: {redirect_url}")
                    processed_images += 1
                    continue

            result, success = process_image_link(link, headers, save_folder, existing_files, state, count, total_images)
            if success:
                if result:  # Only append if we actually downloaded something new
                    high_res_images.append(result['url'])
                processed_images += 1

    # Mark download as complete
    (save_folder / ".download_all_finished").touch()
    logger.info("All high-resolution images downloaded:")
    for img_url in high_res_images:
        logger.info(img_url)

    # Clear the state after successful completion
    clear_state(save_folder)

    # Calculate and display total time taken
    total_time = time.time() - start_time
    logger.info(f"Total time taken: {math.floor(total_time // 60)} minutes, {int(total_time % 60)} seconds")

    # Show completion popup
    show_popup(f"Downloading Done: {folder_name}")

    with open(DOWNLOADED_URL_FILE, 'a') as f:
        f.write(url + '\n') 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # This is handled by the signal handler now
        pass
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)

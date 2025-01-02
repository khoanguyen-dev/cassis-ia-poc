import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def scrape_content(url):
    """
    Scrapes the content (text only) of a page, including dynamic JavaScript-rendered content.
    :param url: URL of the page to scrape.
    :return: Extracted text content of the page.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Visit the page and wait for network activity to settle
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")

            # Extract all the text content from the page
            content = page.evaluate("() => document.body.innerText")

            browser.close()
            return content
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return None

def send_to_process_input(text_content, api_endpoint):
    """
    Sends the extracted text content to the process_input endpoint.
    :param text_content: The text extracted from the page.
    :param api_endpoint: URL of the Flask API endpoint to process the input.
    """
    try:
        response = requests.post(api_endpoint, data={"text": text_content})
        if response.status_code == 201:
            print("Success:", response.json())
        elif response.status_code == 409:
            print("Duplicates detected:", response.json())
        else:
            print("Error response:", response.json())
    except Exception as e:
        print(f"Error occurred while sending data to the server: {e}")

if __name__ == "__main__":
    # Input the URL to scrape and the Flask endpoint
    url_to_scrape = input("Enter the URL to scrape: ")
    api_endpoint = os.getenv("PROCESS_INPUT_ENDPOINT", "http://127.0.0.1:5000/process-annuaire")

    print("Scraping the page...")
    scraped_text = scrape_content(url_to_scrape)

    if scraped_text:
        print("Text content extracted successfully.")
        print("Sending to process_input endpoint...")
        send_to_process_input(scraped_text, api_endpoint)
    else:
        print("Failed to extract content from the page.")

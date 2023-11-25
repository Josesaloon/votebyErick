from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Faker
import random
import time
from pyppeteer import launch
from playwright.sync_api import sync_playwright, TimeoutError

# Create Faker instance
fake = Faker()

# Function to submit form using Selenium
def submit_form_selenium():
    # Generate fake data
    name = fake.name()
    email = f"{name.split()[0].lower()}@gmail.com"
    phone = fake.phone_number()

    # Form data with current timestamp
    form_data = {
        'swfpname': name,
        'swfpmail': email,
        'swfpphone': phone,
        'swfpgender': random.choice(['Male', 'Female']),
        'swfpregion': random.choice([
            'Dar', 'Dodoma', 'Arusha', 'Kilimanjaro', 'Tanga', 'Morogoro', 'Pwani', 'Lindi',
            'Mtwara', 'Ruvuma', 'Iringa', 'Mbeya', 'Singida', 'Tabora', 'Rukwa', 'Kigoma', 'Shinyanga', 'Kagera',
            'Mwanza', 'Mara', 'Manyara', 'Njombe', 'Katavi', 'Simiyu', 'Geita', 'Songwe', 'Unguja Kaskazini',
            'Unguja Kusini', 'Unguja Mjini Magharibi', 'Pemba Kaskazini', 'Pemba Kusini'
        ]),
        'swfpvote': '0',
        'swfpstamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Submit the form using Selenium
        url = 'https://swahilifashionweek.com/nomsignup.php'
        driver.get(url)
        time.sleep(2)  # Wait for the page to load (adjust as needed)

        for key, value in form_data.items():
            element = driver.find_element_by_name(key)

            # Check if the element is visible before sending keys
            if element.is_displayed():
                element.send_keys(value)
            else:
                print(f"Element {key} is not visible.")

        # Use JavaScript to click the submit button
        submit_button = driver.find_element_by_css_selector('button[name="nominationsignup"]')
        driver.execute_script("arguments[0].click();", submit_button)

        # Wait for some time to allow potential JavaScript redirection
        time.sleep(5)

        # Return the current URL after potential redirection
        current_url = driver.current_url

        return current_url

    finally:
        # Close the WebDriver
        driver.quit()

# Function to submit form using Playwright
def submit_form_playwright(url_from_selenium: str):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        try:
            # Navigate to the URL obtained from Selenium
            page.goto(url_from_selenium)

            # Here we select our radio button
            # Wait for the radio button to be present before clicking
            page.wait_for_selector('input[name="hs"][value="157"]')
            page.click('input[name="hs"][value="157"]')

            # Click the submit button and wait for navigation to complete
            page.click('button[name="vote"]')
            # We put a longer timeout for potential delays in loading
            page.wait_for_load_state(state="load", timeout=60000)

            # Retrieve the current URL using the evaluated JavaScript property
            current_url = page.evaluate('(window.location.href)')

            # Check if the page is still open before accessing the URL
            if not page.is_closed():
                if 'voteend.php' in current_url:
                    print(f'Current URL (Playwright): {current_url}')
                    return True

        except (TimeoutError, playwright._impl._errors.TimeoutError) as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
                # Close the browser
            browser.close()

    return False

# Check if the environment is suspended
def is_suspended():
    return os.path.exists("/var/run/codespace-suspended")

if __name__ == "__main__":
    successful_votes = 0
    total_iterations = 1000000

    while True:
        if is_suspended():
            print("Environment is suspended. Pausing execution.")
            while is_suspended():
                time.sleep(5)  # Check every 5 seconds

        # Get the URL from Selenium
        selenium_url = submit_form_selenium()

        if submit_form_playwright(selenium_url):
            successful_votes += 1
            print(f"Vote #{successful_votes} submitted successfully for JOSE SALON!")

        if successful_votes >= total_iterations:
            break

    print("Total Number of Votes:", successful_votes)

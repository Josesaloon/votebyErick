from playwright._impl._errors import TargetClosedError
from playwright.sync_api import sync_playwright, TimeoutError
import time
import os

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        try:
            # Our URL
            page.goto('https://www.swahilifashionweek.com/vote.php?x=75166a43cc49364d814a3d26061e9cc5')

            # Here we select our radio button
            page.click('input[name="hs"][value="157"]')

            # Click the submit button and wait for navigation to complete
            page.click('button[name="vote"]')
            # we put timeout for error of loading page if happens
            page.wait_for_load_state(state="load", timeout=30000)

            # Retrieve the current URL using the evaluated JavaScript property since ametumia js kwenye button ya submit
            current_url = page.evaluate('(window.location.href)')

            # Check if the page is still open before accessing the URL hapa tunaweka tuu mazingira sawa kwa ajili ya
            # kuhandle error
            if not page.is_closed():
                if 'voteend.php' in current_url:
                    return True

        except (TimeoutError, TargetClosedError) as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            # Close the browser
            browser.close()

    return False

def is_suspended():
    # Check if the environment is suspended
    return os.path.exists("/var/run/codespace-suspended")

if __name__ == "__main__":
    successful_votes = 0
    total_iterations = 10000000

    for _ in range(total_iterations):
        if is_suspended():
            print("Environment is suspended. Pausing execution.")
            while is_suspended():
                time.sleep(5)  # Check every 5 seconds

        if main():
            successful_votes += 1
            print(f"Vote #{successful_votes} submitted successfully for JOSE SALON!")

    print("Total Number of Votes:", successful_votes)

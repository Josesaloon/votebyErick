from playwright._impl._errors import TargetClosedError
from playwright.sync_api import sync_playwright, TimeoutError

def main():
    successful_votes = 0

    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context()
        page = context.new_page()

        try:
            # Replace the URL with your actual URL
            page.goto('https://www.swahilifashionweek.com/vote.php?x=75166a43cc49364d814a3d26061e9cc5')

            # Select the radio button with value "157"
            page.click('input[name="hs"][value="157"]')

            # Click the submit button and wait for navigation to complete
            page.click('button[name="vote"]')
            page.wait_for_load_state(state="load", timeout=30000)

            # Retrieve the current URL using the evaluated JavaScript property
            current_url = page.evaluate('(window.location.href)')

            # Check if the page is still open before accessing the URL
            if not page.is_closed():
                if 'voteend.php' in current_url:
                    successful_votes += 1
                    print(f"Vote #{successful_votes} submitted successfully for JOSE SALON!")
        except (TimeoutError, TargetClosedError) as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Close the browser
        browser.close()

    print("Total Number of Votes:", successful_votes)

if __name__ == "__main__":
    for _ in range(1000):
        main()

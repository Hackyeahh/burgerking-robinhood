from playwright.async_api import async_playwright, TimeoutError
import asyncio
from datetime import datetime, timedelta
import random

import time
import statistics

# Constants
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]
NEXT_BTN_SELECTOR = "#NextButton"
ONTARIO_OPTION = "46"  # For page 2 - location dropdown
SATISFACTION_FB = responses = [
    "everything was good, no issues with the order! service was fast & efficient like usual. restaurant was clean and experiencemet expectations",
    "had a great experience today! staff was friendly and helpful. food came out hot and fresh as expected",
    "quick service and accurate order! restaurant appeared clean and well-maintained. overall satisfied with the visit",
    "smooth transaction from start to finish! employees were courteous and the food quality was consistent with previous visits",
    "no complaints at all! order was prepared correctly and delivered promptly. dining area was tidy and comfortable",
    "positive experience overall! staff worked efficiently and the food met my expectations. would definitely return",
    "everything went smoothly during my visit! service was professional and the restaurant maintained good cleanliness standards",
    "satisfied customer here! order accuracy was perfect and staff demonstrated good customer service skills throughout",
    "great job by the team today! food quality was solid and the service timeline was reasonable for the lunch rush",
    "nothing to complain about! restaurant operations seemed well-organized and the final product met expectations as usual",
    "everything was good, no issues with the order! service was fast & efficient like usual. restaurant was clean and experiencemet expectations",
    "had a great experience today! staff was friendly and helpful. food came out hot and fresh as expected",
    "quick service and accurate order! restaurant appeared clean and well-maintained. overall satisfied with the visit",
    "smooth transaction from start to finish! employees were courteous and the food quality was consistent with previous visits",
    "no complaints at all! order was prepared correctly and delivered promptly. dining area was tidy and comfortable",
    "positive experience overall! staff worked efficiently and the food met my expectations. would definitely return",
    "everything went smoothly during my visit! service was professional and the restaurant maintained good cleanliness standards",
    "satisfied customer here! order accuracy was perfect and staff demonstrated good customer service skills throughout",
    "great job by the team today! food quality was solid and the service timeline was reasonable for the lunch rush",
    "nothing to complain about! restaurant operations seemed well-organized and the final product met expectations as usual",
]

STAGE_5_7_SELECTORS = [
    "#QID13-2-label",  # Order type
    "#QID12-2-label",  # Order placement location
    "#QID83-2-label",  # Royal Perks membership
]

# Stage selectors for Q13 to last question
STAGE_SELECTORS = [
    "#QID48-12-label",  # Whopper satisfaction
    "#QR\\~QID60\\~3",  # Number of revisits within 30 days
    "QID60-3-label",  # Number of revisits within 30 days
    "#QR\\~QID49\\~1\\~12",  # Whopper categories
    "#QID50-1-label",  # Whopper repurchase likelihood
    "#QID121-2-label",  # Additional Whopper preference question
    "#QID60-1-label",  # Final Whopper preference question
    "#QR\\~QID62\\~4",  # Reason for visit
    "#QID62-4-label",  # Reason for visit
    "#QID57-2-label",  # Sandwich customization preferences
    "#QID94-2-label",  # Additional customization question
    "#QID55-1-label",  # Party size information
    "#QID97-1-label",  # Survey source information
    "#QID78-2-label",  # Outstanding service question
    "#QID100-2-label",  # Promotional opportunities question
]

# Variables
random_user_agent = random.choice(USER_AGENTS)
now = datetime.now()

# Calculate a random visit time between 10:30 AM and 10:30 PM yesterday
# For page 2 - visit date and time dropdowns
visit_datetime = (
    datetime(year=now.year, month=now.month, day=now.day, hour=10, minute=30)
    - timedelta(days=1)
    + timedelta(seconds=random.randint(0, 12 * 60 * 60))
)

time_selectors = [
    ("#QR\\~QID8\\#1\\~1", visit_datetime.strftime("%I")),  # Hour
    ("#QR\\~QID8\\#2\\~1", visit_datetime.strftime("%M")),  # Minute
    ("#QR\\~QID8\\#3\\~1", visit_datetime.strftime("%p")),  # AM/PM
]

# Select a random satisfaction feedback
satisfaction_feedback = random.choice(SATISFACTION_FB)


async def stage_13_24_dynamic(page):
    """
    Handles dynamic survey questions in stages 13-24.

    This stage accounts for questions that may be reordered or conditionally included,
    looping through STAGE_SELECTORS until the survey is completed.

    Inputs:
        page (playwright.async_api.Page): The Playwright page instance to interact with.

    Output:
        None — this function performs actions on the page and proceeds to the end of the survey.
    """
    while not await page.locator("#EndOfSurvey").is_visible():
        for selector in STAGE_SELECTORS:
            try:
                await page.click(selector, timeout=100)

                # Handle multi-select special case (Whopper categories)
                if selector == "#QR\\~QID49\\~1\\~12":
                    for suffix in ["2", "3", "4", "5", "6", "7", "9"]:
                        await page.click(f"#QR\\~QID49\\~{suffix}\\~12")

                await page.click(NEXT_BTN_SELECTOR)
                break  # Exit inner loop and go to next page

            except TimeoutError:
                continue  # Try next selector if current one isn't found


async def run():
    async with async_playwright() as p:
        # Browser setup to maximize performance
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",  # Required in most headless/container setups
                "--disable-dev-shm-usage",  # Prevents shared memory issues in Docker
                "--disable-gpu",  # Disable GPU (required for headless)
                "--disable-background-networking",  # No pings, prefetch, sync, etc.
                "--no-first-run",  # Skip first-run tasks
                "--no-default-browser-check",  # Don’t check if Chrome is default
                "--disable-background-timer-throttling",  # Don't throttle JS timers
                "--headless=new",  # Use modern headless mode (faster, more accurate)
            ],
        )
        context = await browser.new_context(
            user_agent=random_user_agent, ignore_https_errors=True, no_viewport=True
        )
        page = await context.new_page()

        # Intercept and block unnecessary resources
        async def block_unwanted_requests(route, request):
            if request.resource_type in ["image", "stylesheet", "font"]:
                await route.abort()
            else:
                await route.continue_()

        await page.route("**/*", block_unwanted_requests)

        # Now navigate to the site
        # This is the source survey link for: https://www.mybkexperience.com/
        await page.goto("https://rbixm.qualtrics.com/jfe/form/SV_555CTB7cbZ434fs")

        # Stage 1: Input store location id
        await page.wait_for_selector("#QR\\~QID114")
        await page.fill("#QR\\~QID114", "5079")
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 2: Select location, date, and time
        await page.select_option("#QR\\~QID6", ONTARIO_OPTION)
        # Fill the date input (using JS because it may be read-only)
        await page.eval_on_selector(
            "#QR\\~QID118\\~2",
            f"(el) => el.value = '{visit_datetime.strftime('%m/%d/%Y')}'",
        )

        # Select time parts from dropdowns (hour, minute, AM/PM)
        for selector, value in time_selectors:
            await page.select_option(selector, value)
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 3: Satisfaction feedback
        # Click the 5-star satisfaction label
        await page.click("#QID18-22-label")
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 4: Text feedback
        await page.fill("#QR\\~QID120", satisfaction_feedback)
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 5 to 7
        for selector in STAGE_5_7_SELECTORS:
            await page.click(selector)
            await page.click(NEXT_BTN_SELECTOR)

        # Stage 8: Customer rituals
        for selector in ["#QID123-3-label", "#QID124-3-label"]:
            await page.click(selector)
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 9: Category satisfaction
        for item_id in ["11", "1", "13", "7", "16", "4", "9", "2"]:
            await page.click(f"#QR\\~QID21\\~{item_id}\\~12")
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 10: Return recommend
        for item_id in ["1", "2"]:
            await page.click(f"#QR\\~QID41\\~{item_id}\\~6")
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 11: Problems
        await page.click("#QID38-2-label")
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 12: Order items
        for selector in ["#QID103-1-label", "#QID103-2-label", "#QID103-3-label"]:
            await page.click(selector)
        await page.click(NEXT_BTN_SELECTOR)

        # Stage 12a–c: Item-specific questions
        # Beef, Side, Drink
        for selector in ["#QID46-22-label", "#QID47-3-label", "#QID107-14-label"]:
            await page.click(selector)
            await page.click(NEXT_BTN_SELECTOR)

        # Stage 13 to 24: Dynamic questions
        await stage_13_24_dynamic(page)

        # Extract validation code
        await page.wait_for_selector("#EndOfSurvey")

        # Extract the validation code (always in bold text; after "Validation Code: ")
        final_text_blurb = (await page.inner_text("#EndOfSurvey strong")).split(": ")[1]
        print("Validation code:", final_text_blurb)

        # Close browser
        await browser.close()


# asyncio.run(run())


def benchmark_program(repeats=5):
    run_times = []  # To store the run times of each execution

    for _ in range(repeats):
        start_time = time.time()  # Start time
        asyncio.run(run())  # Run the program
        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        run_times.append(elapsed_time)  # Add the elapsed time to the list

    # Calculate basic statistics using the statistics module
    fastest_time = min(run_times)  # Fastest (minimum) run time
    slowest_time = max(run_times)  # Slowest (maximum) run time
    mean_time = statistics.mean(run_times)
    median_time = statistics.median(run_times)
    std_dev_time = statistics.stdev(run_times)

    # Print the statistics
    print(f"Benchmark Results ({repeats} Runs):")
    print(f"Fastest Run Time: {fastest_time:.4f} seconds")
    print(f"Slowest Run Time: {slowest_time:.4f} seconds")
    print(f"Mean Run Time: {mean_time:.4f} seconds")
    print(f"Median Run Time: {median_time:.4f} seconds")
    print(f"Standard Deviation of Run Times: {std_dev_time:.4f} seconds")


# Run the benchmark
benchmark_program()

#!/usr/bin/env python3

import asyncio
import random
import subprocess
import requests
import time 
from playwright.async_api import async_playwright

# Configuration for bot behavior
MAX_CONCURRENT_BOTS = 18  # Maximum number of bots at a time
BOT_CREATION_INTERVAL = (10, 45)  # Random interval between bot creations (in seconds)
AD_CLICK_PROBABILITY = random.uniform(0.5, 0.7)  # Probability range of clicking ads
ARTICLE_CLICK_PROBABILITY = 0.8  # Probability of clicking articles
PAGE_REFRESH_PROBABILITY = 0.3  # Probability of refreshing the page

# Website information
URL = "https://newswebsite-eov7.onrender.com/"
ARTICLE_CONTAINER_CLASS = "article-preview"
AD_CONTAINER_CLASS = "container-8822094742e0551294538b3f5a7c7268__bn"

#food page urls
#urls for the food site
food_url = "https://foodsite-bt45.onrender.com/"

foodpage_url = [
    "https://foodsite-bt45.onrender.com/meals_otd.html",
    "https://foodsite-bt45.onrender.com/random_recipe.html",
    "https://foodsite-bt45.onrender.com/search.html"
]





# List of user agents
USER_AGENTS = [
    # Desktop User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",  # Internet Explorer 11

    # Mobile User Agents
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; ARM; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.67 Safari/537.36 Mobile",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QC1A.200205.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",  # iOS Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/91.0.4472.120 Mobile Safari/537.36",

    # Additional Random User Agents
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/93.0.961.38",
    "Mozilla/5.0 (Linux; Android 10; Mi 9T Pro Build/PKQ1.190408.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]

async def simulate_bot(playwright, bot_id):

    user_agent = random.choice(USER_AGENTS)
    print(f"Bot {bot_id}: Using user Agent: {user_agent}")

    """Simulates a single bot's interaction with the website."""
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(user_agent=user_agent)
    page = await context.new_page()

    try:
        print(f"Bot {bot_id}: Navigating to the website.")
        await page.goto(URL)

        # Random delay to simulate reading or interaction
        await asyncio.sleep(random.uniform(3, 10))

        # Decide whether to refresh the page
        if random.random() < PAGE_REFRESH_PROBABILITY:
            print(f"Bot {bot_id}: Refreshing the page.")
            await page.reload()
            await asyncio.sleep(random.uniform(2, 5))  # Simulate time spent after refresh

        # Decide whether to click an article
        if random.random() < ARTICLE_CLICK_PROBABILITY:
            print(f"Bot {bot_id}: Searching for articles to click.")
            articles = await page.locator(f'.{ARTICLE_CONTAINER_CLASS}').all()
            if articles:
                article_to_click = random.choice(articles)
                print(f"Bot {bot_id}: Clicking on an article.")
                await article_to_click.click()
                await asyncio.sleep(random.uniform(5, 15))  # Simulate reading time
                await page.go_back()

        # Decide whether to click ads
        if random.random() < AD_CLICK_PROBABILITY:
            print(f"Bot {bot_id}: Searching for ads to click.")
            ads = await page.locator(f'.{AD_CONTAINER_CLASS}').all()
            if ads:
                ad_to_click = random.choice(ads)
                print(f"Bot {bot_id}: Clicking on an ad.")
                await ad_to_click.click()
                time.sleep(2)

                # Wait on the new tab for a random time before closing it
                await asyncio.sleep(random.uniform(5, 15))
                pages = context.pages
                if len(pages) > 1:  # Ensure there's a new tab
                    print(f"Bot {bot_id}: Closing the new ad tab.")
                    await pages[-1].close()
                    time.sleep(2)
                await asyncio.sleep(1)  # Brief pause before returning to main tab

        # Step 2: Interact with the food site
        print(f"Bot {bot_id}: Navigating to the food site.")
        for food_url in foodpage_url:
            print(f"Bot {bot_id}: Visiting {food_url}")
            await page.goto(food_url)
            await asyncio.sleep(random.uniform(5, 10))  # Simulate time spent on the page         

    except Exception as e:
        # Change: Catch the exception and continue to the food site
        print(f"Bot {bot_id}: Error on the news site: {e}. Continuing to the food site.")

    # Step 2: Interact with the food site
        print(f"Bot {bot_id}: Navigating to the food site.")
        for food_url in foodpage_url:
            try:
                print(f"Bot {bot_id}: Visiting {food_url}")
                await page.goto(food_url)
                await asyncio.sleep(random.uniform(5, 10))  # Simulate time spent on the page         
            except Exception as e:
                print(f"Bot {bot_id}: Error on the food site: {e}. Skipping this page.")

    finally:
        print(f"Bot {bot_id}: Closing the browser.")
        await browser.close()

   

async def manage_bots():
    """Manages the creation and execution of multiple bots."""
    async with async_playwright() as playwright:
        active_bots = []
        bot_counter = 0

        while True:
            # Randomize the number of bots to create (1 to MAX_CONCURRENT_BOTS)
            num_bots = random.randint(1, MAX_CONCURRENT_BOTS)

            for _ in range(num_bots):
                bot_counter += 1
                print(f"Starting Bot {bot_counter}")
                await simulate_bot(playwright, bot_counter)

                # Random staggered intervals for bot creation
                await asyncio.sleep(random.uniform(*BOT_CREATION_INTERVAL))

              

            # Wait briefly to avoid overloading the hosting service
            print(f"Waiting before the next burst................")
            await asyncio.sleep(random.uniform(5, 10))

if __name__ == "__main__":
    asyncio.run(manage_bots())

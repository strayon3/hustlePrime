#!/usr/bin/env python3

import asyncio
import random
import subprocess
import requests
import time 
from playwright.async_api import async_playwright
from info import serverFiles,pword,uname

# Configuration for bot behavior
MAX_CONCURRENT_BOTS = 6  # Maximum number of bots at a time
BOT_CREATION_INTERVAL = (5, 60)  # Random interval between bot creations (in seconds)
AD_CLICK_PROBABILITY = random.uniform(0.1, 0.3)  # Probability range of clicking ads
ARTICLE_CLICK_PROBABILITY = 0.8  # Probability of clicking articles
PAGE_REFRESH_PROBABILITY = 0.3  # Probability of refreshing the page

# Website information
URL = "https://newswebsite-eov7.onrender.com/"
ARTICLE_CONTAINER_CLASS = "article-preview"
AD_CONTAINER_CLASS = "container-8822094742e0551294538b3f5a7c7268__bn"

#vpn file and info
VPNBOOK_USERNAME = uname
VPNBOOK_PASSWORD = pword


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



#picks a server file
def get_server_file():
    """Picks a server file from the available files."""
    try:
        if not serverFiles:
            raise ValueError("No .ovpn files found in the provided list.")
        
        selected_server_file = random.choice(serverFiles)
        return selected_server_file
    
    except Exception as e:
        print(f"Error selecting server file: {e}")
        raise


def rotate_vpn():
    """Rotate the VPN connection using a server file."""
    try:
        print("Rotating VPN connection with VPNBook...")

        # Get a server file
        server_file = get_server_file()
        print(f"Selected server file: {server_file}")

        # Disconnect any existing OpenVPN connection
        disconnect_process = subprocess.run(
            ["sudo", "pkill", "openvpn"],
            check=False  # No error raised if OpenVPN isn't running
        )
        if disconnect_process.returncode == 0:
            print("Existing OpenVPN connection terminated.")
        else:
            print("No active OpenVPN connection to terminate.")

        # Connect to VPNBook server using Popen for interaction
        process = subprocess.Popen(
            ["sudo", "openvpn", "--config", server_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Enable text mode for easier string handling
        )

        # Wait a moment to ensure the process starts and prompts for username
        time.sleep(1)  # Adjust if needed

        # Send the username (simulating Enter after it)
        process.stdin.write(VPNBOOK_USERNAME + "\n")
        process.stdin.flush()

        # Wait for the password prompt to appear
        time.sleep(1)  # Adjust if needed

        # Send the password (simulating Enter after it)
        process.stdin.write(VPNBOOK_PASSWORD + "\n")
        process.stdin.flush()

        # Wait for the process to complete or get any relevant output
        stdout, stderr = process.communicate()

        # Check the result
        if process.returncode == 0:
            print("VPN connection established successfully.")
        else:
            print("Error connecting VPN.")
            print(stderr)  # Print any error message from stderr

        # Optionally, handle any output (stdout) here if you want to log it
        print(stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error during VPN rotation: {e}")
        raise RuntimeError("Failed to rotate VPN connection.")
    except Exception as e:
        print(f"Unexpected error: {e}")

#gets current ip address for the current bot 
def get_external_ip():
    """Get the external IP address using ipify API."""
    try:
        # Use ipify to get public IP address
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Error retrieving IP: {e}")
        return None
    


async def simulate_bot(playwright, bot_id):
    #rotate vpn before bot starts 
    rotate_vpn()

    external_ip = get_external_ip()
    #assign a random user agent for this bot
    user_agent = random.choice(USER_AGENTS)
    if external_ip:
        print(f"Bot {bot_id}: Using user agent: {user_agent}: With ip: {external_ip}")

    else:
        print(f"Bot {bot_id}: Using user agent: {user_agent}, but IP could not be retrieved")

    """Simulates a single bot's interaction with the website."""
    browser = await playwright.chromium.launch(headless=False) #change when ready to run headless
    context = await browser.new_context()
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

                # Wait on the new tab for a random time before closing it
                await asyncio.sleep(random.uniform(5, 15))
                pages = context.pages
                if len(pages) > 1:  # Ensure there's a new tab
                    print(f"Bot {bot_id}: Closing the new ad tab.")
                    await pages[-1].close()
                await asyncio.sleep(1)  # Brief pause before returning to main tab

    except Exception as e:
        print(f"Bot {bot_id}: Error during execution: {e}")

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
                bot_task = asyncio.create_task(simulate_bot(playwright, bot_counter))
                active_bots.append(bot_task)

                # Random staggered intervals for bot creation
                await asyncio.sleep(random.uniform(*BOT_CREATION_INTERVAL))

                # Remove completed bots from the active list
                active_bots = [bot for bot in active_bots if not bot.done()]

            # Wait briefly to avoid overloading the hosting service
            await asyncio.sleep(random.uniform(5, 10))

if __name__ == "__main__":
    asyncio.run(manage_bots())

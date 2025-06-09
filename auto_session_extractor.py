# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import asyncio
import json
from playwright.async_api import async_playwright

async def auto_extract_session(target: str, output_path: str):
    """
    Uses Playwright to open a headless Chromium,
    navigates to https://www.instagram.com/accounts/login/,
    prompts user to paste valid cookies JSON (ที่เก็บใน tools/session_alx_trading.json),
    verifies session by requesting https://www.instagram.com/,
    saves { "sessionid": "<value>", "user_agent": "<value>" } to output_path if valid.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(f"Navigating to {target} login page...")
            await page.goto(target, timeout = 60000) # Increased timeout for navigation

            # Prompt user for cookies
            cookies_json_path = "tools/session_alx_trading.json"
            print(f"Please paste your cookies JSON into '{cookies_json_path}' and press Enter to continue.")
            input("Press Enter after pasting cookies...")

            # Load cookies from file
            try:
                with open(cookies_json_path, 'r') as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
                print("Cookies loaded successfully.")
            except FileNotFoundError:
                print(f"Error: Cookie file '{cookies_json_path}' not found.")
                return
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in '{cookies_json_path}'.")
                return
            except Exception as e:
                print(f"Error loading cookies: {e}")
                return

            # Verify session by navigating to the main page
            print("Verifying session by navigating to Instagram main page...")
            await page.goto("https://www.instagram.com/", timeout = 60000) # Increased timeout

            # Check if login was successful (e.g., by looking for a specific element or URL)
            # A simple check here is to see if we are redirected back to login,
            # or if the page title indicates a successful login.
            if "instagram.com/accounts/login" in page.url:
                print("Session verification failed: Still on login page.")
                return

            print("Session verified successfully.")

            # Extract sessionid and user_agent
            all_cookies = await context.cookies()
            session_id_cookie = next((cookie for cookie in all_cookies if cookie['name'] == 'sessionid'), None)

            if session_id_cookie:
                session_id = session_id_cookie['value']
                user_agent = await page.evaluate("() => navigator.userAgent")

                session_data = {
                    "sessionid": session_id,
                    "user_agent": user_agent
                }

                with open(output_path, 'w') as f:
                    json.dump(session_data, f, indent = 4)
                print(f"Session data saved to '{output_path}'")
            else:
                print("Could not find 'sessionid' cookie after login.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    # Example usage:
    target_url = "https://www.instagram.com/accounts/login/"
    output_file = "config/extracted_alx_session.json"

    # Create dummy cookie file for testing if it doesn't exist
    # In a real scenario, the user would create this file.
    dummy_cookie_path = "tools/session_alx_trading.json"
    try:
        with open(dummy_cookie_path, 'x') as f: # 'x' creates file, fails if exists
            json.dump([{"name": "sessionid", "value": "YOUR_SESSION_ID_HERE", "domain": ".instagram.com", "path": "/"}], f)
            print(f"Created a dummy cookie file at '{dummy_cookie_path}'. Please edit it with your actual cookies.")
    except FileExistsError:
        pass # File already exists, no need to create a dummy one.

    asyncio.run(auto_extract_session(target_url, output_file))
    print(f"Please check '{output_file}' for the extracted session details.")
    print(f"Remember to have your valid cookies in 'tools/session_alx_trading.json' before running.")

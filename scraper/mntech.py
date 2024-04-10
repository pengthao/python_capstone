from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import urllib.parse
import asyncio
import json
import os
import re

async def scrape_jobs(search_term, search_location, search_radius):
    def load_auth():
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE = os.path.join(ROOT_DIR,"auth.json")
        with open(FILE, "r") as f:
            return json.load(f)

    cred = load_auth()
    auth = f'{cred["username"]}:{cred["password"]}'
    browser_url = f'wss://{auth}@{cred["host"]}'

    results_found = {}
    today = datetime.now().date()
    current_year = datetime.now().year  # Get the current year

    async with async_playwright() as pw:
        print('Connecting to browser.')
        browser = await pw.chromium.connect_over_cdp(browser_url) #my proxy
        page = await browser.new_page()
        pages = 2
        print("Connected.")

        for pageNumber in range(1, pages + 1, 1):
            url = f"https://careers.mntech.org/backfills/jobs?click_location=search&d={search_radius}&l={search_location}&pg={pageNumber}&q={search_term}"
            await page.goto(url, timeout=120000)
            print("Loaded initial page.")
            html = await page.content()
            
            doc = BeautifulSoup(html, "html.parser")
            li = doc.find_all(class_="job-listing")
            for job in li:
                try:
                    aTag = job.find("a", class_="jobList-title")
                    title = aTag.find("strong").string
                    href = aTag.get("href")
                    salary = job.find(class_="jobList-salary")
                    salaryText = ""  
                    if salary:
                        salaryText = salary.get_text()
                    description = job.find(class_="jobList-description")
                    descriptionText = "" 
                    if description:
                        descriptionText = description.get_text()
                    # Get the list date
                    list_date_str = job.find(class_="jobList-date").string.strip()
                    list_date = datetime.strptime(f"{list_date_str} {current_year}", '%d %b %Y').date()
                    
                    # Check if the list date is greater than today
                    if list_date > today:
                        # Subtract one year from the list date
                        list_date -= timedelta(days=365)
                    
                    short_date = list_date.strftime('%x')

                    company = job.find_next("li").get_text(strip=True)

                    results_found[href] = {"title" : title, "company" : company, "salary" : salaryText, "list date" : short_date, "description" : descriptionText, "url" : href, "search_term": search_term}
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                    pass
                
    return results_found

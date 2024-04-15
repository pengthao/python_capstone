from bs4 import BeautifulSoup
import requests

async def scrape_hireTech(search_term):

    results_found = {}

    print('Connecting to browser.')

    url = f"https://www.hiretechladies.com/jobs?*={search_term}"
    page = requests.get(url).text
    print("Connected.")

    doc = BeautifulSoup(page, "html.parser")
    li = doc.find_all("div", class_="job_card-item")
    for job in li:
        try:
            title = job.find(class_ = "job_card-head").string
            href = job.find("a", class_="job-item_link").get("href")
            full_url = "https://www.hiretechladies.com" + href
            salary = "None Listed"
            description = job.find("p").string
            company = job.find("div", class_="job_card-head").string

            results_found[full_url] = {"title" : title, "company" : company, "salary" : salary, "description" : description, "url" : full_url, "search_term": search_term}
            
        except Exception as e:
            print(f"An error occurred: {e}")
            pass

    return results_found
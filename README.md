# Project Information

This project provides a user interface to interact with a web scraper. Currently the tracker scrapes mnTech, but could be configured to scrape multiple sources.

## Libraries/Frameworks/Modules

This project uses:

- Flask
- Playwright
- Bright Data (Web Scraping Browser)
- Beautiful Soup
- FlaskForm~WTForms
- Jinja

## Using the Scraper

Install all dependencies, create the `auth.json` file, start the flask backend, run the react frontend and interact with the tool.

### auth.json

In the scraper directory fill in your [Bright Data Scraping Browser](https://brightdata.com/products/scraping-browser) credentials in a `backend/scraper/auth.json` file (see `auth_example.json`).

### Python Flask Backend

- `cd backend`
- `pip install -r requirements.txt`
- `playwright install`
- `python app.py` or `python3 app.py`

# Project Information

This project provides a user interface to interact with a web scraper. Currently the tracker scrapes mnTech, but could be configured to scrape multiple sources.

## Libraries/Frameworks/Modules

This project uses:

- Flask
- Flask - login_manager
- Flask - Blueprints
- FlaskForms
- Jinja
- Playwright
- Bright Data (Web Scraping Browser)
- Beautiful Soup
- Bcrypt
- Postgres
- SQLAlchemy


## Using the Scraper

Install all dependencies, create the `auth.json`and `config.json` file, start the flask app.

### auth.json

In the scraper directory fill in your [Bright Data Scraping Browser](https://brightdata.com/products/scraping-browser) credentials in a `backend/scraper/auth.json` file (see `auth_example.json`).

### Python Flask Backend

- `pip install -r requirements.txt`
- `playwright install`
- `python app.py` or `python3 app.py`

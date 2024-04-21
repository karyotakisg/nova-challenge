import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import  re

driver = None

def create_json(website):
    data = {
        "title": "",
        "body": ""
    }
    with open(website + '.json', 'w') as file:
        json.dump(data, file)
    return data


def add_to_json(website, title, body):
    # Create a dictionary with article data
    article_data = {
        "title": title,
        "body": body
    }
    try:
        with open(website + ".json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    data.append(article_data)
    with open(website + ".json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def scrape_article_keywords_and_title(soup):
    title_tag = soup.title
    if title_tag is not None:
        # Get the text of the title
        title = title_tag.get_text()
        return soup, title
    else:
        # Handle the case where the title element is not found
        return soup, "Title Not Found"


def scrape_article_text(soup):
    # Extract text within <p> tags
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def scrape_article_text_simple(soup):
    pure_text = soup.get_text()
    pure_text = re.sub(r'\s+', ' ', pure_text.strip())
    return pure_text


def scrape_article_urls(url, soup):
    article_urls = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[1]  # Extract the domain name
    # Find all article links
    unique_links = set()
    links = soup.select('a[href^="https"]')
    for link in links:
        unique_links.add(link['href'])
    for link in unique_links:

        parsed_link = urlparse(link)
        try:
            link_domain = parsed_link.netloc.split('.')[1]  # Extract the domain name from the link
        except IndexError:
            continue
        link_path_components = parsed_link.path.split('/')  # Split path using forward slash
        # Check if the link starts with the same domain and has at least 4 subdomains
        if link_domain == domain and len(link_path_components) >= 3:
            article_urls.append(link)
    return article_urls

def connect_with_selenium(url):
    global driver
    try:
        if driver is None:
            driver = webdriver.Chrome()  # Εδώ μπορείς να επιλέξεις τον περιηγητή που θες
        driver.get(url)
        time.sleep(3)  # Δίνουμε λίγο χρόνο για να φορτώσει η σελίδα
        page_source = driver.page_source
        return page_source
    except WebDriverException as e:
        print(f"Failed to connect to {url} with Selenium: {e}")



def main():
    # List of example URLs for scraping
    urls = [
        "https://www.protothema.gr/",
        "https://www.kathimerini.gr/",
        "https://www.amna.gr/",
        "https://www.iefimerida.gr/",
        "https://www.newsit.gr/",
        "https://www.in.gr/",
        "https://www.newsbeast.gr/",
        "https://www.news247.gr/",
        "https://www.newsbomb.gr/",
        "https://www.skai.gr/",
        "https://www.tovima.gr/",
        "https://www.tanea.gr/",
        "https://www.parapolitika.gr/",
        "https://www.newmoney.gr/",
        "https://www.capital.gr/",
        "https://www.euro2day.gr/",
        "https://www.ot.gr/",
        "https://www.infocom.gr/",
        "https://www.powergame.gr/",
        "https://www.mononews.gr/",
        "https://www.liberal.gr/",
        "https://www.moneyreview.gr/",
        "https://www.zougla.gr/",
        "https://www.businessdaily.gr/",
        "https://www.insider.gr/",
        "https://www.businessnews.gr/",
        "https://netweek.gr/",
        "https://marketingweek.gr/",
        "https://www.ictplus.gr/",
        "http://typologies.gr/",
        "https://www.advertising.gr/",
        "https://www.documentonews.gr/",
        "https://www.efsyn.gr/"
    ]
    # Dictionary to store article URLs by website
    # take all newspapers
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_urls = scrape_article_urls(url, soup)

            website = url.split(".")[1].split(".")[0]
        else:
            page_source = connect_with_selenium(url)
            soup = BeautifulSoup(page_source, 'html.parser')
            article_urls = scrape_article_urls(url, soup)
            print(article_urls)
            website = url.split(".")[1].split(".")[0]

        for article_url in article_urls:
            response = requests.get(article_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                page_source = connect_with_selenium(article_url)
                soup = BeautifulSoup(page_source, 'html.parser')

            html_parser, title = scrape_article_keywords_and_title(soup)
            body = scrape_article_text(html_parser)
            add_to_json(website, title, body)
        print(f"Finished scraping {website}")
    if driver is not None:
        driver.quit()


if __name__ == "__main__":
    main()

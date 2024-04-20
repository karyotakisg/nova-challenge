import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
import json
import os
import re

def create_json(website):
    data = {
        "title": "",
        "keywords": "",
        "body": ""
    }
    with open(website+'.json', 'w') as file:
        json.dump(data, file)
    return data

def add_to_json(website, title, keywords, body):
    # Create a dictionary with article data
    article_data = {
        "title": title,
        "keywords": keywords,
        "body": body
    }
    try:
        with open(website+".json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
    except:
        data = []
    data.append(article_data)
    with open(website+".json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def scrape_article_keywords_and_title(soup):
    keywords = list(meta.attrs.get('content') for meta in soup.find_all('meta', attrs={'name': 'keywords'}))
    title_tag = soup.title
    if title_tag is not None:
        # Get the text of the title
        title = title_tag.get_text()
        return soup, keywords, title

def scrape_article_text(soup):
    pure_text = soup.get_text()
    pure_text = re.sub(r'\s+', ' ', pure_text.strip())
    return pure_text
    
def scrape_article_urls(url, soup):
    article_urls = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[1]  # Extract the domain name
    # Find all article links
    for link in soup.select('a[href^="http"]'):
        link_url = link['href']
        parsed_link = urlparse(link_url)
        link_domain = parsed_link.netloc.split('.')[1]  # Extract the domain name from the link
        link_path_components = parsed_link.path.split('/')  # Split path using forward slash
        # Check if the link starts with the same domain and has at least 4 subdomains
        if link_domain == domain and len(link_path_components) >= 5:
            article_urls.append(link_url)
    return article_urls
    


def main():
    # List of example URLs for scraping
    urls = [
    "https://www.tovima.gr/",
    "https://www.tanea.gr/",
    "https://www.newmoney.gr/",
    "https://www.capital.gr/",
    "https://www.euro2day.gr/",
]

    # Dictionary to store article URLs by website
    # take all newspapers
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_urls = scrape_article_urls(url, soup)
            website = url.split(".")[1].split(".")[0]
        for article_url in article_urls:
            html_parser, keywords, title = scrape_article_keywords_and_title(soup)
            body = scrape_article_text(html_parser)
            add_to_json(website, title, keywords, body)
           
if __name__ == "__main__":
    main()

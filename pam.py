import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import os
import re

def create_json():
    data = {
        "title": "",
        "keywords": "",
        "body": ""
    }
    with open('data.json', 'w') as file:
        json.dump(data, file)
    return data

def scrape_article_keywords(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        keywords = [meta.attrs.get('content') for meta in soup.find_all('meta', attrs={'name': 'keywords'})]
        return soup, keywords
    else:
        return None

def scrape_article_text(soup):
    pure_text = soup.get_text()
    pure_text = re.sub(r'\s+', ' ', pure_text.strip())
    return pure_text

def main():
    # List of example URLs for scraping
    urls = ["https://www.newsbomb.gr/"]

    # Dictionary to store article URLs by website
    article_urls_by_website = {}

    keywords_by_article = {}

    # Scrape article URLs for each website
    for url in urls:
        print("Scraping from:", url)
        article_urls = scrape_article_urls(url)
        if article_urls:
            article_urls_by_website[url] = article_urls
            print("Article URLs collected:", len(article_urls))
        else:
            print("Failed to scrape article URLs from website:", url)
    # Scrape keywords for each article URL
    for website, article_urls in article_urls_by_website.items():
        for article_url in article_urls:
            print("Scraping keywords from article:", article_url)
            html_parser, keywords = scrape_article_keywords(article_url)
            if keywords:
                keywords_by_article[article_url] = keywords
                title = article_url.split('/')[-1]  # Extract article title from URL
                body = scrape_article_text(html_parser)
                create_json_file(website, article_url, title, keywords, body)
            else:
                print("Failed to scrape keywords from article:", article_url)

    # Print keywords for each article URL
    print("\nKeywords by article:")
    for article_url, keywords in keywords_by_article.items():
        print("Article URL:", article_url)
        print("Keywords:", keywords)
        print()

def create_json_file(website, article_url, title, keywords, body):
    # Create a dictionary with article data
    article_data = {
        "title": title,
        "keywords": keywords,
        "body": body
    }
    # Create the folder if it doesn't exist
    folder_name = website.replace('https://www.', '')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Create the file name
    file_name = os.path.join(folder_name, f"{article_url.split('/')[-1]}.json")
    # Write the dictionary to a JSON file
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(article_data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON file created: {file_name}")
def scrape_article_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
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
    else:
        return None
def scrape_article_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
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
    else:
        return None
if __name__ == "__main__":
    main()

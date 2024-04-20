import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import re

def create_json(website):
    data = {
        "title": "",
        "body": ""
    }
    with open(website+'.json', 'w') as file:
        json.dump(data, file)
    return data

def add_to_json(website, title, body):
    # Create a dictionary with article data
    article_data = {
        "title": title,
        "body": body
    }
    try:
        with open(website+".json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    data.append(article_data)
    with open(website+".json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def scrape_article_keywords_and_title(soup):
    title_tag = soup.title
    if title_tag is not None:
        # Get the text of the title
        title = title_tag.get_text()
        return soup, title

def scrape_article_text(soup):
    pure_text = soup.get_text()
    pure_text = re.sub(r'\s+', ' ', pure_text.strip())
    return pure_text
    
def scrape_article_urls(url, soup):
    article_urls = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[1]  # Extract the domain name
    # Find all article links
    print(soup.select('a[href^="https"]'))
    for link in soup.select('a[href^="https"]'):
        link_url = link['href']
        parsed_link = urlparse(link_url)
        
        try:
            link_domain = parsed_link.netloc.split('.')[1]  # Extract the domain name from the link
        except IndexError:
            continue
        link_path_components = parsed_link.path.split('/')  # Split path using forward slash
        # Check if the link starts with the same domain and has at least 4 subdomains
        if link_domain == domain and len(link_path_components) >= 5:
            article_urls.append(link_url)
            print(link_url)
    return article_urls
    


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
        for article_url in article_urls:
            response = requests.get(article_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
            html_parser, title = scrape_article_keywords_and_title(soup)
            body = scrape_article_text(html_parser)
            add_to_json(website, title, body)
           
if __name__ == "__main__":
    main()


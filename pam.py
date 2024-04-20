import requests
from bs4 import BeautifulSoup

# Function to scrape article URLs from a website
def scrape_article_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_urls = []
        # Find all article links
        for link in soup.select('a[href^="http"]'):
            article_urls.append(link['href'])
        return article_urls
    else:
        return None

# Main function
def main():
    # List of example URLs for scraping
    urls = [
        'https://www.protothema.gr/',
        'https://www.kathimerini.gr/',
        'https://www.amna.gr/',
        'https://www.iefimerida.gr/',
        'https://www.newsit.gr/',
        'https://www.in.gr/',
        'https://www.newsbeast.gr/'
    ]

    # Dictionary to store article URLs by website
    article_urls_by_website = {}

    for url in urls:
        print("Scraping from:", url)
        # Scrape article URLs
        article_urls = scrape_article_urls(url)
        if article_urls:
            article_urls_by_website[url] = article_urls
            print("Article URLs collected:", len(article_urls))
        else:
            print("Failed to scrape article URLs from website:", url)

    print("\nArticle URLs by website:")
    for website, article_urls in article_urls_by_website.items():
        print(website)
        for idx, article_url in enumerate(article_urls, start=1):
            print(f"Article {idx}: {article_url}")
        print()

if __name__ == "__main__":
    main()

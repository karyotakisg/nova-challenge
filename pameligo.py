import requests
from bs4 import BeautifulSoup
import json

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

# Function to send URL to GPT-4 API and get analysis results
def analyze_article(url):
    api_endpoint = 'https://platform.openai.com/api-keys'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'sk-proj-5Ch4zJiP642RgT9E2BB1T3BlbkFJ0F9NVgsH6MkOMavvZY3q'
    }
    data = {
        'prompt': "Παρακαλώ αναλύστε το άρθρο στον ακόλουθο σύνδεσμο: " + url + "\n\nΣτοιχεία που χρειάζομαι:\n- Keywords\n- Meta Description\n- Category\n- Subcategories"
    }
    response = requests.post(api_endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main function
def main():
    # List of example URLs for scraping
    urls = ['https://www.newsbeast.gr/'
       'https://www.protothema.gr/',]
     #   'https://www.kathimerini.gr/',
     #   'https://www.amna.gr/',
    #    'https://www.iefimerida.gr/',
    #    'https://www.newsit.gr/',
    #    'https://www.in.gr/',
    #    'https://www.newsbeast.gr/'
   # ]

    # Dictionary to store article URLs by website
    article_urls_by_website = {}

    # Loop through each website and scrape article URLs
    for url in urls:
        print("Scraping article URLs from:", url)
        article_urls = scrape_article_urls(url)
        if article_urls:
            article_urls_by_website[url] = article_urls
            print("Article URLs collected:", len(article_urls))
        else:
            print("Failed to scrape article URLs from website:", url)

    # Loop through each website and its article URLs to analyze
    for website, article_urls in article_urls_by_website.items():
        print(f"Processing articles from {website}")
        for idx, article_url in enumerate(article_urls, start=1):
            print(f"Analyzing article {idx}...")
            analysis_result = analyze_article(article_url)
            if analysis_result:
                # Extract keywords, meta descriptions, category, and subcategories
                keywords = analysis_result.get('keywords', [])
                meta_description = analysis_result.get('meta_description', '')
                category = analysis_result.get('category', '')
                subcategories = analysis_result.get('subcategories', [])

                # Create a dictionary to hold the extracted information
                article_info = {
                    'keywords': keywords,
                    'meta_description': meta_description,
                    'category': category,
                    'subcategories': subcategories
                }

                # Write the article information to a JSON file
                filename = f"{website}_article_{idx}_info.json"
                with open(filename, 'w') as json_file:
                    json.dump(article_info, json_file, indent=4)
                print(f"Article information saved to {filename}")
            else:
                print("Failed to analyze article.")

if __name__ == "__main__":
    main()

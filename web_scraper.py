import requests
from bs4 import BeautifulSoup
import json
import csv

def scrape_quotes():
    url = "http://quotes.toscrape.com"
    print(f"Scraping from: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        data = []
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            
            data.append({
                "quote": text,
                "author": author,
                "tags": tags
            })
        
        # Save to JSON
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Save to CSV
        with open('quotes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "quote": item['quote'],
                    "author": item['author'],
                    "tags": ", ".join(item['tags'])
                })
        
        # Save to TXT
        with open('quotes.txt', 'w', encoding='utf-8') as f:
            for i, item in enumerate(data, 1):
                f.write(f"{i}. {item['quote']} - {item['author']}\n")

        print(f"\nSuccess! Scraped {len(data)} quotes")
        print("Files saved: quotes.json, quotes.csv, quotes.txt")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_quotes()
from bs4 import BeautifulSoup
import requests

# Fetch HTML content from a URL
url = "http://example.com"  # Replace with a target URL
response = requests.get(url)
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links in the document
links = soup.find_all('a')

# Print the text and href attribute of each link
for link in links:
    print(f"Text: {link.get_text()}, URL: {link.get('href')}")

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

def extract_data_from_xml(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')  # Use 'xml' parser for XML content

    items = soup.find_all('item')
    data = []

    for item in items:
        title = item.find('title').text if item.find('title') else None
        description = item.find('description').text if item.find('description') else None

        # Extract link and pubDate directly from the item element
        link_element = item.find('link')
        link = link_element.text if link_element else None

        pubDate_element = item.find('pubDate')
        pubDate = pubDate_element.text if pubDate_element else None

        # Handle namespaces for elements with prefixes (e.g., media:thumbnail)
        media_thumbnail = item.find('media:thumbnail')
        thumbnail_url = media_thumbnail['url'] if media_thumbnail and 'url' in media_thumbnail.attrs else None

        # Decode HTML entities in the link
        link = html.unescape(link) if link else None

        item_data = {
            'title': title,
            'description': description,
            'link': link,
            'pubDate': pubDate,
            'thumbnail_url': thumbnail_url,
        }

        data.append(item_data)

    return data

@app.route('/')
def main():
    # Default XML URL
    default_xml_url = "https://www.newscientist.com/section/features/feed/"

    # Get the selected XML URL from the query parameters
    selected_xml_url = request.args.get('xml_url', default_xml_url)

    # Fetch data from the selected XML URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Make a request to the XML URL
        response = requests.get(selected_xml_url, headers=headers, allow_redirects=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract data from the XML content
            extracted_data = extract_data_from_xml(response.content)
            
            # Render the template with the extracted data and available XML URLs
            return render_template('index.html', data=extracted_data, xml_urls=get_available_xml_urls(), selected_xml_url=selected_xml_url)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except Exception as e:
        # Print any exceptions that occur during the request
        print(f"An error occurred during the request: {str(e)}")

def get_available_xml_urls():
    # Define the available XML URLs and their corresponding labels
    xml_urls = {
        "New Scientist": "https://www.newscientist.com/section/features/feed/",
        "Phys.org": "https://phys.org/rss-feed/",
        "Scientific American": "http://rss.sciam.com/ScientificAmerican-Global",
        "NASA Image Details": "https://www.nasa.gov/feeds/iotd-feed/",
        "Science News": "https://www.sciencenews.org/feed",
        "Science Daily": "https://www.sciencedaily.com/rss/all.xml",
        # Add more sources as needed
    }
    return xml_urls

if __name__ == '__main__':
    app.run(debug=True)

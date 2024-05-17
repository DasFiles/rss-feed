from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import html
import random

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
      # Get the available XML URLs
    xml_urls = get_available_xml_urls()

    # Randomly select a default XML URL
    default_xml_url = random.choice(list(xml_urls.values()))

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
"General | NBC News Top Stories": "http://feeds.nbcnews.com/feeds/topstories",
"General | NBC News World News": "http://feeds.nbcnews.com/feeds/worldnews",
"General | ABC News": "http://feeds.abcnews.com/abcnews/usheadlines",
"General | CNN Top Stories": "http://rss.cnn.com/rss/cnn_topstories.rss",
"General | CBS News": "http://www.cbsnews.com/latest/rss/main",
"General | Quartz": "http://qz.com/feed",
"General | The Guardian USA": "http://www.theguardian.com/world/usa/rss",
"Politics | CNN All Politics": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
"Politics | NBC News Politics": "http://feeds.nbcnews.com/feeds/nbcpolitics",
"Politics | NPR Politics Podcast": "http://www.npr.org/rss/rss.php?id=1014",
"Politics | NPR Politics": "http://www.npr.org/rss/rss.php?id=5",
"Business | CNN Business": "http://rss.cnn.com/rss/edition_business.rss",
"US tech | CNN Tech": "http://rss.cnn.com/rss/cnn_tech.rss",
"US tech | New York Times Technology": "http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
"US tech | Fox News Tech": "http://feeds.foxnews.com/foxnews/tech",
"US tech | TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
"US tech | Wired": "http://feeds.wired.com/wired/index",
"US tech | CNET News": "http://www.cnet.com/rss/news/",
"US tech | CNET iPhone Update": "http://www.cnet.com/rss/iphone-update/",
"US tech | CNET Android Update": "http://www.cnet.com/rss/android-update/",
"Health | The Guardian Society Health": "http://www.theguardian.com/society/health/rss",
"Health | Men's Health": "http://www.menshealth.com/events-promotions/washpofeed",
"Health | Glamour Health & Fitness": "http://feeds.glamour.com/glamour/health_fitness",
"Health | New Scientist Health": "http://feeds.newscientist.com/health",
"Health | Time Health": "http://time.com/health/feed/",
"Entertainment | The New Yorker Culture": "http://www.newyorker.com/feed/culture",
"Entertainment | BuzzFeed TV and Movies": "http://www.buzzfeed.com/tvandmovies.xml",
"Entertainment | TMZ": "http://www.tmz.com/rss.xml",
"Entertainment | CBS News Entertainment": "http://www.cbsnews.com/latest/rss/entertainment",
"Entertainment | ABC News Entertainment Headlines": "http://feeds.abcnews.com/abcnews/entertainmentheadlines",
"ABC News | US Headline":"http://feeds.abcnews.com/abcnews/usheadlines",
"Gaming | GamesRadar": "http://www.gamesradar.com/all-platforms/news/rss/",
"Gaming | TechCrunch Gaming": "http://feeds.feedburner.com/TechCrunch/gaming",
"Gaming | CNET Gaming": "http://www.cnet.com/rss/gaming/",
"Gaming | Ars Technica Gaming": "http://feeds.arstechnica.com/arstechnica/gaming",
"Times Of India | Top Stories": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
"Times Of India | India":"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
"Times Of India | World":"https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
"The Hindu | News":"https://www.thehindu.com/news/feeder/default.rss",
"The Hindu | Opinion":"https://www.thehindu.com/opinion/feeder/default.rss",
"LiveMint | News":"https://www.livemint.com/rss/news",
"LiveMint | Opinion":"https://www.livemint.com/rss/opinion",
"India Today | Home":"https://www.indiatoday.in/rss/home",
"India Today | The Big Story":"https://www.indiatoday.in/rss/1206614",
"The New York Time | World":"https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
"The New York Time | U.S.":"https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
"The New York Time | Science":"https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
"DW News | English":"http://rss.dw.com/xml/rss-en-all",
"NDTV | Top stories":"https://feeds.feedburner.com/ndtvnews-top-stories",
"NDTV | World News":"https://feeds.feedburner.com/ndtvnews-world-news",
"NDTV | Offbeat":"https://feeds.feedburner.com/ndtvnews-offbeat-news",
"Google News | World":"https://news.google.com/rss",
"Google News | India":"https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",   
"Futurism":"https://futurism.com/feed",
"CNN | Money":"http://rss.cnn.com/rss/money_topstories.rss",
"Yahoo News":"http://news.yahoo.com/rss",
"China Daily | World News":"http://www.chinadaily.com.cn/rss/world_rss.xml",
"Variety":"http://variety.com/feed/",
"Fox News | Latest":"http://feeds.foxnews.com/foxnews/latest",        
# "Science Daily | All": "https://www.sciencedaily.com/rss/all.xml",
# "Science Daily | Top Science": "https://www.sciencedaily.com/rss/top/science.xml",
# "Science Daily | Health": "https://www.sciencedaily.com/rss/top/health.xml",

"BBC | World News":"http://feeds.bbci.co.uk/news/rss.xml",
"The Guardian | Business":"https://www.theguardian.com/business/economics/rss",
"India Times | Economic Times":"https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
"Investopedia | Investing Finance":"https://www.investopedia.com/feedbuilder/feed/getfeed/?feedName=rss_headline",
"Market Watch | Top Stories":"http://feeds.marketwatch.com/marketwatch/topstories/",
 "The Economist | Finace and Economics":"http://www.economist.com/sections/economics/rss.xml",       
"Entrepreneur":"https://www.entrepreneur.com/latest.rss",
"Financial Times":"https://www.ft.com/?format=rss",
"Fortune":"http://fortune.com/feed/",
"BBC | Science Focus":"https://feeds.purplemanager.com/193c804a-a673-47bd-b09b-11baf4822a17/complete-rss-feed-for-science-focus",
"Cosmos Magazine": "https://cosmosmagazine.com/feed/",
"Space News":"https://spacenews.com/feed/",

"New Scientist | Features": "https://www.newscientist.com/section/features/feed/",
"New Scientist | All Articles": "https://www.newscientist.com/feed/home/",
"New Scientist | News": "https://www.newscientist.com/section/news/feed/",
"Phys.org ": "https://phys.org/rss-feed/",
"MIT | Latest News":"https://news.mit.edu/rss/feed",
"MIT | Research News":"https://news.mit.edu/rss/research",
"Scientific American | Global": "http://rss.sciam.com/ScientificAmerican-Global",
"NASA | Image Details": "https://www.nasa.gov/feeds/iotd-feed/",
"NASA | News Release":"https://www.nasa.gov/news-release/feed/",
"NASA | Resently Published":"https://www.nasa.gov/feed/",
"NASA | Technology":"https://www.nasa.gov/technology/feed/",
"NASA | Aeronautics":"https://www.nasa.gov/aeronautics/feed/",
"NASA | Curious Universe":"https://www.nasa.gov/feeds/podcasts/curious-universe",
"Smithsonian Magazine | Latest Articles":"https://www.smithsonianmag.com/rss/latest_articles/",
"Smithsonian Magazine | Science and Nature":"https://www.smithsonianmag.com/rss/science-nature/",
"US National Science Foundation | Research News":"https://new.nsf.gov/rss/rss_www_news.xml",
        
"Science Alert | Science News":"https://www.sciencealert.com/feed",
"MIT Technology Review":"https://www.technologyreview.com/stories.rss",
"Sci.News":"http://www.sci-news.com/feed",
"Science News": "https://www.sciencenews.org/feed",   

        
        # "":"",
        # Add more sources as needed
    }
    return xml_urls

if __name__ == '__main__':
    app.run(debug=True)

#install{ pip install flask requests beautifulsoup4 lxml}

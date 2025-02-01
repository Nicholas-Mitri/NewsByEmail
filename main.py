import requests
import send_email, os
from datetime import datetime, timedelta
import time
import argparse

# Set up argument parser for command line interface
parser = argparse.ArgumentParser(description="News API article fetcher")
parser.add_argument(
    "--scheduled", type=bool, default=False, help="Enable scheduled sending at 9 AM"
)
parser.add_argument(
    "--articles", type=int, default=50, help="Number of articles to display"
)
parser.add_argument(
    "--country", default="us", type=str, help="Country to search for news."
)
parser.add_argument(
    "--query", default="", type=str, help="Custom query to limit search."
)

# Parse command line arguments
args = parser.parse_args()
print(args)

# Update program variables based on command line arguments
is_scheduled = args.scheduled
num_articles_to_display = args.articles
country = args.country
query = args.query

# If scheduled mode is enabled, wait until designated send time
if is_scheduled:
    # Set scheduled time (9 AM)
    SCHEDULED_TIME = "09:00"

    def check_send_time():
        """Check if current time matches scheduled send time"""
        current_time = datetime.now().strftime("%H:%M")
        return current_time == SCHEDULED_TIME

    # Continuously check if it's time to send email
    while True:
        if check_send_time():
            print(f"Initiating email send at {datetime.now().strftime('%H:%M')}")
            break
        else:
            print(
                f"Waiting... Current time: {datetime.now().strftime('%H:%M')}. Scheduled for: {SCHEDULED_TIME}"
            )
            time.sleep(60)  # Check every minute


# Get API key from environment variables
key = os.getenv("NEWS_KEY")


# Set up News API endpoint and parameters
base_url = "https://newsapi.org/v2/top-headlines"
num_articles_to_display = 50

# Dictionary for top-headlines endpoint parameters
params = {
    "apiKey": key,  # Your API key; required.
    # Use either 'country' and/or 'category' OR 'sources' (do not combine them).
    "country": country,  # The 2-letter ISO 3166-1 country code (e.g., 'us', 'gb', 'de').
    # "category": "general",  # The category of news (options: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology').
    # "sources": "",  # Comma-separated string of news source identifiers (e.g., 'bbc-news,cnn'). Leave empty if using 'country' or 'category'.
    "q": query,  # Keywords or a phrase to search for in the article titles and content.
    "pageSize": num_articles_to_display,  # The number of results per page (default is 20, maximum is 100).
}


# Make API request and parse response
request = requests.get(base_url, params=params)
content = request.json()
articles = content["articles"]
num_articles_to_display = len(articles)

# Create base HTML template for email with two-column layout
msg = """<html><body>
<h1 style='text-align: center;'>Daily News Brief</h1>
<div style='display: flex; justify-content: space-between;'>
<div style='width: 48%; padding: 20px;'>  <!-- Left column -->
<h2 style='text-align: center;'>Column 1</h2>
</div>
<div style='width: 48%; padding: 20px;'>  <!-- Right column -->
<h2 style='text-align: center;'>Column 2</h2>
</div>
</div>
</body></html>"""


# Create column content by splitting articles between left and right columns
left_column = ""
right_column = ""
for i, article in enumerate(articles):
    # Create HTML for each article with title, image, description and link
    article_html = f"""
        <h2>{article['title']}</h2>
        <img src={article['urlToImage']} style="width: 75%; display: block; margin: 0 auto;">
        <p>{article['description']}</p>
        <p><a href="{article['url']}" style="color: #0066cc; text-decoration: none;">Read more...</a></p>
    """
    # Add article to left column if in first half, right column if in second half
    if i < num_articles_to_display // 2:
        left_column += article_html
    else:
        right_column += article_html

# Insert column content into base HTML template
msg = msg.replace(
    "<h2 style='text-align: center;'>Column 1</h2>",
    left_column,
)
msg = msg.replace(
    "<h2 style='text-align: center;'>Column 2</h2>",
    right_column,
)


# Send email with formatted news content
send_email.send(
    receiver="ngmitri04@gmail.com",
    subject=f"Daily News Brief for {datetime.now().strftime('%a %d, %Y')}",
    message=msg,
    MIME="html",
)

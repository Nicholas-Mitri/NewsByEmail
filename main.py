import requests
import send_email, os, sys
from datetime import datetime
import time
import argparse, gpt_fn
import logging

# Add this near the top of your script
logging.basicConfig(
    filename="/tmp/newsfetcher.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("Script started")


# Set up argument parser for command line interface
parser = argparse.ArgumentParser(description="News API article fetcher")
parser.add_argument(
    "--scheduled", type=bool, default=False, help="Enable scheduled sending at 9 AM"
)
parser.add_argument(
    "--articles", type=int, default=10, help="Number of articles to display"
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

# After getting the API key
if not key:
    logging.error("NEWS_KEY environment variable not found")
    sys.exit(1)

print(key)
# Set up News API endpoint and parameters
base_url = "https://newsapi.org/v2/top-headlines"

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
system_prompt = """
Your are an AI assistant playing the role of news editor. When given a news article and its title, /
return a 150 word or less summary that includes the major points from the article that a reader would /
need to stay up to date.
"""
print(len(articles))
for i, article in enumerate(articles):
    summary = gpt_fn.send_system_and_user_prompts(
        system_prompt, f"Title:{article['title']}\n\nArticle:\n{article['content']}"
    )
    print(f"Summary for article {i+1} is ready...")
    title, source = article["title"].split(" - ")
    title = title.title()
    # Create HTML for each article with title, image, description and link
    article_html = f"""
        <h2>{title}</h2>
        <h4>Source: {source}</h4>
        <img src={article['urlToImage']} style="width: 100%; display: block; margin: 0 auto;">
        <p>{summary}</p>
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

import requests
import send_email, os
from datetime import datetime, timedelta
import time

is_scheduled = False
if is_scheduled:
    # Set scheduled time (9 AM)
    SCHEDULED_TIME = "09:00"

    def check_send_time():
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


key = os.getenv("NEWS_KEY")
base_url = "https://newsapi.org/v2/everything"
num_articles_to_display = 30

# [ ] Create filters for language, source, and blacklisted words
params = {
    "apiKey": key,  # Required: Your News API key.
    "q": "canada AND ontario AND Trump NOT Elon",  # Keywords or phrases to search for in the article title and body.
    # "searchIn": "title,description",  # (Optional) Fields to search in. Options: "title", "description", "content".
    # "sources": "bbc-news,the-verge",  # (Optional) Comma-separated list of news source identifiers.
    # "domains": "bbc.co.uk,techcrunch.com",  # (Optional) Comma-separated list of domains to restrict the search.
    # "excludeDomains": "example.com",  # (Optional) Comma-separated list of domains to remove from the results.
    "from": (datetime.now() - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    ),  # (Optional) ISO 8601 date (or date-time) for the oldest article allowed.
    "to": datetime.now().strftime(
        "%Y-%m-%d"
    ),  # (Optional) ISO 8601 date (or date-time) for the newest article allowed.
    "language": "en",  # (Optional) 2-letter ISO-639-1 code of the language to get headlines for.
    "sortBy": "publishedAt",  # (Optional) Sort order: "relevancy", "popularity", or "publishedAt".
    "pageSize": num_articles_to_display,  # (Optional) Number of results per page (default is 100, maximum is 100).
    # "page": 1,  # (Optional) Page number for pagination (default is 1).
}

request = requests.get(base_url, params=params)
content = request.json()
articles = content["articles"]
num_articles_to_display = len(articles)

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


# Create column content
left_column = ""
right_column = ""
for i, article in enumerate(articles):
    article_html = f"""
        <h2>{article['title']}</h2>
        <img src={article['urlToImage']} style="width: 75%; display: block; margin: 0 auto;">
        <p>{article['description']}</p>
        <p><a href="{article['url']}" style="color: #0066cc; text-decoration: none;">Read more...</a></p>
    """
    if i < num_articles_to_display // 2:
        left_column += article_html
    else:
        right_column += article_html

# Insert column content
msg = msg.replace(
    "<h2 style='text-align: center;'>Column 1</h2>",
    left_column,
)
msg = msg.replace(
    "<h2 style='text-align: center;'>Column 2</h2>",
    right_column,
)


send_email.send(
    receiver="ngmitri04@gmail.com",
    subject=f"Daily News Brief for {datetime.now().strftime('%a %d, %Y')}",
    message=msg,
    MIME="html",
)

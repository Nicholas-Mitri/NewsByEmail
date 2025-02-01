import requests
import send_email, os
from langdetect import detect
from datetime import datetime
import time

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
url = (
    "https://newsapi.org/v2/everything?q=tesla&from=2025-01-01&sortBy=publishedAt&apiKey="
    + str(key)
)

request = requests.get(url)
content = request.json()
articles = content["articles"]


# Counter for non-English or invalid articles removed
popped_count = 0
i = 0
# Iterate through articles using while loop since we're modifying the list
while i < len(articles):
    try:
        # Check if article title is not in English using langdetect
        if detect(articles[i]["title"]) != "en":
            # Remove non-English article and increment counter
            articles.pop(i)
            popped_count += 1
        else:
            # Only increment index for English articles we keep
            i += 1
    except:
        # Handle any errors (e.g. missing title, detection fails)
        # Remove problematic article and increment counter
        articles.pop(i)
        popped_count += 1

print(f"Removed {popped_count} non-English articles")


msg = "<html><body>"
msg += "<h1 style='text-align: center;'>Daily News Brief</h1>"
msg += "<div style='display: flex; justify-content: space-between;'>"
msg += "<div style='width: 48%; padding: 20px;'>"  # Left column
msg += "<h2 style='text-align: center;'>Column 1</h2>"
msg += "</div>"
msg += "<div style='width: 48%; padding: 20px;'>"  # Right column
msg += "<h2 style='text-align: center;'>Column 2</h2>"
msg += "</div>"
msg += "</div>"

num_articles_to_display = 10
# Create column content
left_column = ""
right_column = ""
for i, article in enumerate(articles[:num_articles_to_display]):
    article_html = f"""
        <h2>{article['title']}</h2>
        <img src={article['urlToImage']} style="width: 75%; display: block; margin: 0 auto;">
        <p>{article['description']}</p>
        <p><a href="{article['url']}" style="color: #0066cc; text-decoration: none;">Read more...</a></p>
    """
    if i < 5:
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
    receiver="ngmitri04@gmail.com", subject="Daily News Brief", message=msg, MIME="html"
)

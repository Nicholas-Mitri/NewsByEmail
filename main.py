import requests
import send_email, os
from langdetect import detect


key = os.getenv("NEWS_KEY")
url = (
    "https://newsapi.org/v2/everything?q=tesla&from=2025-01-01&sortBy=publishedAt&apiKey="
    + str(key)
)

request = requests.get(url)
content = request.json()
articles = content["articles"]

# [x] TODO filter for english only
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


# [x] TODO add html layout and populate
# [x] TODO add images
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


# [x] TODO change formatting to html
send_email.send(
    receiver="ngmitri04@gmail.com", subject="Daily News Brief", message=msg, MIME="html"
)

# [ ] TODO add scheduled emails

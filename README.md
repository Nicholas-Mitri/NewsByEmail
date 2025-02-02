# News Aggregator Email Service

This application aggregates news articles and sends them as a formatted email digest.

## Dependencies

The project requires the following Python packages:

- openai==1.61.0
- requests==2.32.3

## Installation

1. Clone this repository
2. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
3. Add your API keys to your environment:

   ```bash
   # Open .zshrc in your preferred text editor
   nano ~/.zshrc

   # Add the following lines to the file
   export GMAIL_PASSWORD="your_gmail_app_password"
   export OPENAI_API_KEY="your_openai_api_key"
   export NEWS_API_KEY="your_newsapi_key"

   # Save and exit the editor
   # Then reload your .zshrc
   source ~/.zshrc
   ```

   Note:

   - For Gmail, you'll need to use an App Password rather than your regular account password. You can generate one in your Google Account settings under Security > 2-Step Verification > App passwords.
   - You can get your News API key by signing up at https://newsapi.org
   - Get your OpenAI API key from https://platform.openai.com/api-keys

## Usage

Run the script from the command line using:

```bash
python main.py [options]
```

### Command Line Arguments

- `--email`: Gmail Email address to send the digest to (required)

  ```bash
  python main.py --email "user@gmail.com"
  ```

- `--scheduled`: Enable scheduled sending at 9 AM daily (default: False)

  ```bash
  python main.py --scheduled True
  ```

- `--articles`: Number of articles to display in the digest (default: 10)

  ```bash
  python main.py --articles 20
  ```

- `--country`: Two-letter country code to search for news (default: "us")

  ```bash
  python main.py --country gb  # for UK news
  ```

- `--query`: Custom search query to filter articles (default: "")
  ```bash
  python main.py --query "technology"
  ```

### Examples

Fetch 15 technology-related articles from the UK:

```bash
python main.py --email "user@gmail.com" --articles 15 --country gb --query "technology"
```

Schedule daily digest of 20 US news articles at 9 AM:

```bash
python main.py --email "user@gmail.com" --scheduled True --articles 20 --country us
```

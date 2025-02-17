# X.com (Twitter) Feed Connection

This project provides functionality to connect to X.com (formerly Twitter) and fetch user feeds using the Twitter API v2.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Twitter Developer account and get your API credentials:
   - Go to https://developer.twitter.com/
   - Create a new project and app
   - Generate API keys and tokens (you'll need both API keys and Access tokens)

3. Create a `.env` file:
   - Copy `.env.template` to `.env`
   - Fill in your Twitter API credentials

## Usage

The main functionality is in `twitter_client.py`. Here's how to use it:

```python
from twitter_client import connect_to_twitter, get_user_feed

# Connect to Twitter
client = connect_to_twitter()

# Get tweets from a specific user
tweets = get_user_feed(client, "username", max_results=10)

# Process the tweets
for tweet in tweets:
    print(f"Tweet at {tweet.created_at}:")
    print(tweet.text)
```

## Functions

- `connect_to_twitter()`: Establishes connection to Twitter API using credentials from `.env` file
- `get_user_feed(client, username, max_results=10)`: Fetches tweets from a specified user

## Error Handling

The code includes error handling for:
- Missing API credentials
- User not found
- API request failures

## Security Note

Never commit your `.env` file with real credentials to version control. The `.env` file is included in `.gitignore` by default. 
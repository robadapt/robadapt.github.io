import os
import logging
import tweepy
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

def connect_to_twitter():
    """
    Connects to Twitter/X.com API and returns a client instance.
    Requires the following environment variables:
    - TWITTER_API_KEY
    - TWITTER_API_SECRET
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_TOKEN_SECRET
    - TWITTER_BEARER_TOKEN (optional, but recommended)
    
    Returns:
        tweepy.Client: Authenticated Twitter API client
    """
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')  # Added bearer token support
    
    # Log credential status (without revealing actual credentials)
    logger.debug("Checking Twitter credentials...")
    logger.debug(f"API Key present: {bool(api_key)}")
    logger.debug(f"API Secret present: {bool(api_secret)}")
    logger.debug(f"Access Token present: {bool(access_token)}")
    logger.debug(f"Access Token Secret present: {bool(access_token_secret)}")
    logger.debug(f"Bearer Token present: {bool(bearer_token)}")
    
    # Verify all credentials are present
    if not all([api_key, api_secret]):
        raise ValueError("Missing required Twitter API credentials (API Key and Secret)")
    
    try:
        # Create client with bearer token if available, otherwise use OAuth 1.0a
        if bearer_token:
            logger.info("Using Bearer Token authentication")
            client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
        else:
            logger.info("Using OAuth 1.0a authentication")
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
        
        # Test the connection
        logger.debug("Testing Twitter API connection...")
        me = client.get_me()
        if me:
            logger.info(f"Successfully connected to Twitter API as user ID: {me.data.id}")
        
        return client
        
    except tweepy.errors.Unauthorized as e:
        logger.error("Twitter API authentication failed!")
        logger.error(f"Error details: {str(e)}")
        raise ValueError(
            "Twitter API authentication failed. Please check your credentials. "
            "Make sure you have the correct API keys and tokens, and that they haven't been revoked."
        )
    except Exception as e:
        logger.error(f"Error creating Twitter client: {str(e)}")
        raise

def get_user_feed(client, username, max_results=10):
    """
    Retrieves tweets from a user's feed.
    
    Args:
        client (tweepy.Client): Authenticated Twitter API client
        username (str): Twitter username to fetch tweets from
        max_results (int): Maximum number of tweets to retrieve (default: 10)
        
    Returns:
        list: List of tweets
    """
    try:
        logger.info(f"Attempting to fetch tweets for user: {username}")
        
        # Get user ID from username
        user_response = client.get_user(username=username)
        if not user_response or not user_response.data:
            logger.error(f"User not found: {username}")
            raise ValueError(f"User {username} not found")
            
        user_id = user_response.data.id
        logger.debug(f"Found user ID: {user_id}")
        
        # Get user's tweets with expanded tweet fields
        tweets_response = client.get_users_tweets(
            user_id,
            max_results=max_results,
            tweet_fields=['created_at', 'text', 'public_metrics'],
            expansions=['author_id'],
            user_fields=['username', 'name']
        )
        
        if not tweets_response.data:
            logger.info(f"No tweets found for user: {username}")
            return []
            
        logger.info(f"Successfully fetched {len(tweets_response.data)} tweets")
        return tweets_response.data
        
    except tweepy.errors.Unauthorized as e:
        logger.error("Twitter API authentication failed while fetching tweets!")
        logger.error(f"Error details: {str(e)}")
        raise ValueError(
            "Failed to fetch tweets due to authentication error. "
            "Please check your Twitter API credentials."
        )
    except tweepy.errors.TweepyException as e:
        logger.error(f"Twitter API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching tweets: {str(e)}")
        raise

if __name__ == '__main__':
    # Example usage
    try:
        client = connect_to_twitter()
        # Replace 'username' with the Twitter handle you want to fetch tweets from
        tweets = get_user_feed(client, 'username')
        
        for tweet in tweets:
            print(f"Tweet at {tweet.created_at}:")
            print(tweet.text)
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {str(e)}") 
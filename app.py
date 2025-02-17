import logging
import signal
import sys
from flask import Flask, render_template, request, jsonify
from twitter_client import connect_to_twitter, get_user_feed

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def signal_handler(sig, frame):
    print('\nShutting down gracefully...')
    sys.exit(0)

@app.route('/')
def index():
    logger.debug("Attempting to serve index page")
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return str(e), 500

@app.route('/fetch-tweets', methods=['POST'])
def fetch_tweets():
    logger.info("Received request to fetch tweets")
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        client = connect_to_twitter()
        tweets = get_user_feed(client, username)
        
        formatted_tweets = []
        for tweet in tweets:
            formatted_tweets.append({
                'text': tweet.text,
                'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'tweets': formatted_tweets})
    except Exception as e:
        logger.error(f"Error fetching tweets: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Starting server at http://localhost:5050")
    print("Press Ctrl+C to stop the server")
    
    # Run with threaded=True for better handling of connections
    app.run(
        host='127.0.0.1',
        port=5050,
        threaded=True,
        use_reloader=False  # Disable reloader to prevent duplicate processes
    ) 
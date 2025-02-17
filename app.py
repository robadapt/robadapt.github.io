import logging
import socket
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Add CORS support
from twitter_client import connect_to_twitter, get_user_feed

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more verbose logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add security headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def check_port(port):
    """Check if a port is available."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("127.0.0.1", port))
        result = True
    except socket.error:
        logger.error(f"Port {port} is already in use")
    finally:
        sock.close()
    return result

def find_available_port(start_port=5000, max_port=9000):
    """Find first available port in range."""
    for port in range(start_port, max_port):
        if check_port(port):
            return port
    return None

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
        
        # Format tweets for display
        formatted_tweets = []
        for tweet in tweets:
            formatted_tweets.append({
                'text': tweet.text,
                'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        logger.info(f"Successfully fetched {len(formatted_tweets)} tweets")
        return jsonify({'tweets': formatted_tweets})
    except Exception as e:
        logger.error(f"Error fetching tweets: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Find an available port
    port = find_available_port()
    if not port:
        logger.error("No available ports found")
        exit(1)
        
    logger.info(f"Found available port: {port}")
    
    try:
        # Test the port one final time
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(("127.0.0.1", port))
        test_socket.close()
        
        logger.info(f"Starting Flask application on port {port}...")
        # Use the simplest possible configuration
        app.run(
            host="127.0.0.1",
            port=port,
            debug=False  # Disable debug mode to prevent reloader
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1) 
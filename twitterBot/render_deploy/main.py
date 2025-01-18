import tweepy
import subprocess
import os
from dotenv import load_dotenv
import logging
import time
import threading
from flask import Flask

# Create Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/twitter_bot.log'),
        logging.StreamHandler()
    ]
)

# Get credentials from environment variables
bearer_token = os.getenv('BEARER_TOKEN')
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Initialize Twitter client
client = tweepy.Client(
    bearer_token, 
    api_key, 
    api_secret, 
    access_token, 
    access_token_secret
)
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_fortune():
    """Execute fortune command and return its output"""
    try:
        cmd = "/usr/games/fortune"
        p1 = subprocess.Popen(
            [cmd], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        output, error = p1.communicate()
        if p1.returncode == 0:
            return output.decode("utf-8")
        else:
            logging.error(f"Fortune command error: {error.decode('utf-8')}")
            return None
    except Exception as e:
        logging.error(f"Error executing fortune command: {str(e)}")
        return None

def post_tweet():
    """Post a fortune tweet if it meets the character limit"""
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        text = get_fortune()
        if text and len(text) < 280:
            try:
                tweet = client.create_tweet(text=text)
                logging.info(f"Successfully posted tweet: {text[:50]}...")
                return True
            except Exception as e:
                logging.error(f"Error posting tweet: {str(e)}")
                return False
        attempt += 1
    
    logging.warning("Could not find suitable fortune after maximum attempts")
    return False

def bot_thread():
    """Background thread for the bot"""
    logging.info("Bot thread started")
    while True:
        try:
            # Post tweet immediately when starting
            logging.info("Attempting to post tweet...")
            post_tweet()
            logging.info("Sleeping for 24 hours...")
            time.sleep(86400)  # 24 hours
        except Exception as e:
            logging.error(f"Bot thread error: {str(e)}")
            time.sleep(300)  # 5 minutes before retry

@app.route('/')
def home():
    return 'Twitter Fortune Bot is running!'

@app.route('/health')
def health():
    return 'OK'

@app.route('/trigger')
def trigger_tweet():
    """Endpoint to manually trigger a tweet"""
    try:
        result = post_tweet()
        if result:
            return 'Tweet posted successfully!'
        return 'Failed to post tweet', 500
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == "__main__":
    logging.info("Starting Twitter Fortune Bot...")
    
    # Start bot in a separate thread
    bot = threading.Thread(target=bot_thread)
    bot.daemon = True
    bot.start()
    
    # Start web server
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 
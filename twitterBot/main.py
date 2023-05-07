import tweepy
import subprocess
from keys.keys import bearer_token
from keys.keys import api_key
from keys.keys import api_secret
from keys.keys import access_token
from keys.keys import access_token_secret

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuthHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def terminal():
    cmd = "fortune"
    p1 = subprocess.Popen(cmd.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p1.communicate()
    if p1.returncode == 0:
        return output.decode("utf-8")
    else:
        return "Error: " + error.decode("utf-8")


if __name__ == "__main__":
    while True:
        text = terminal()
        if len(text) < 280:
            client.create_tweet(text = text)
            break
        else:
            continue
    


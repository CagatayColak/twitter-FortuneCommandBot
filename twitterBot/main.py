import tweepy
import subprocess
from keys import keys


def api():
    auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return tweepy.API(auth)


def tweet(api: tweepy.API, text: str):
    api.update_status(text)


def terminal():
    cmd = "fortune"
    p1 = subprocess.Popen(cmd.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p1.communicate()
    if p1.returncode == 0:
        return output.decode("utf-8")
    else:
        return "Error: " + error.decode("utf-8")


if __name__ == "__main__":
    api = api()
    text = terminal()
    if text.split()[0] != "Error:":
        for i in range(0, len(text), 280):
            tweet(api, text[i:i+280])
    else:
        pass



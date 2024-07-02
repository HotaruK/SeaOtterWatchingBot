import os

# ----------------
# FireStore
# ----------------
firestore_project_id = os.getenv("FIRESTORE_PROJECT_ID")
firestore_collection_name = os.getenv("FIRESTORE_COLLECTION_NAME")

montereybay_sea_otter_url = os.getenv("MB_YOUTUBE_URL")
vancouver_sea_otter_url = os.getenv("VC_YOUTUBE_URL")
seattle_sea_otter_url = os.getenv("SEATTLE_YOUTUBE_URL")
toba_sea_otter_url = os.getenv("TOBA_YOUTUBE_URL")

# ----------------
# Twitter
# ----------------
twitter_tweet_post_url = "https://api.twitter.com/2/tweets"

twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
twitter_token = os.getenv("TWITTER_TOKEN")
twitter_token_secret = os.getenv("TWITTER_TOKEN_SECRET")

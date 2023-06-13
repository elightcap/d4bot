from twitter_scraper_selenium import scrape_profile
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os
import schedule
import time
import json

load_dotenv()

# Discord webhook URL
discord_webhook_url = os.getenv("DISCORD_WEBHOOK")

# Twitter user whose tweets you want to scrape
twitter_username = 'game8_d4boss'

# Variable to store the ID of the latest processed tweet
latest_tweet_id = None

def scrape_and_post_tweet():
    global latest_tweet_id

    # Scrape the latest tweet from the specified user
    tweets = scrape_profile(twitter_username=f"{twitter_username}",output_format="json",browser="firefox",tweets_count=2,headless="true")

    if tweets:
        json_object = json.loads(tweets)
        tweet_id = list(json_object.keys())[1]

        # Check if it's a new tweet
        if tweet_id != latest_tweet_id:
            latest_tweet_id = tweet_id
            tweet_content = json_object[tweet_id]['content']
            if("spawn" not in tweet_content):
                print("dont care")
                return
            # Post the tweet content to Discord
            split = tweet_content.split(' ')
            boss_name = split[0]
            spawntime = (f"{split[-3]} {split[-2]} {split[-1]}").strip("(")
            embed = DiscordEmbed(title='World Boss Spawning!', color='03b2f8')
            embed.set_thumbnail(url=json_object[tweet_id]['images'][0])
            embed.set_image(url=json_object[tweet_id]['images'][1])
            embed.add_embed_field(name="Boss", value=boss_name)
            embed.add_embed_field(name="Spawn Time", value=spawntime)
            embed.set_footer(text="https://github.com/elightcap/d4bot")
            embed.set_timestamp()
            webhook = DiscordWebhook(url=discord_webhook_url, content="@here")
            webhook.add_embed(embed)
            response = webhook.execute()
            print("New tweet posted to Discord.")
        else:
            print("No new tweets.")
    else:
        print("No tweets found for the specified user.")

# Schedule the job to run every minute
schedule.every(1).minutes.do(scrape_and_post_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)

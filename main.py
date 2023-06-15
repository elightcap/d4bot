from twitter_scraper_selenium import scrape_profile
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import dateutil.parser as parser
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
        #get the id of the second tweet bc they have one pinned. thisll change if they unpin it
        tweet_id = list(json_object.keys())[1]

        # Check if it's a new tweet
        if tweet_id != latest_tweet_id:
            now = datetime.now(timezone.utc)
            now_est = datetime.now()
            then = now + timedelta(minutes=-5)
            post_time = json_object[tweet_id]['posted_time']
            post_dto = parser.parse(post_time)
            if then > post_dto:
                print("too old")
                return
            latest_tweet_id = tweet_id
            #get content of tweet and check if it contains spawn.
            tweet_content = json_object[tweet_id]['content']
            if("spawn" not in tweet_content):
                print("dont care")
                return
            # spit the tweet into individual words. use this to get the boss name and spawn time. thinking about location
            split = tweet_content.split(' ')
            if split[1]!="will" and "spawn" not in split[1]:
                boss_name = f"{split[0]} {split[1]}"
            else:
                boss_name = split[0]
            #gotta prepend a 0 to the time to make it 24 hour bc
            if len(split[-3]) < 6:
                shittytime = split[-3].strip("(")
                split[-3] = ("0{}".format(shittytime))
            #split[-3] is the hours and minutes, split[-2] is AM or PM. theres a parenthesis in the way, so we gotta strip those out.
            spawntime = (f"{split[-3]}:00 {split[-2]}").strip("(").strip(")")
            spawntimelong = timeconvert(spawntime)
            spawntimesplit = spawntimelong.split(":")
            #to unix timestamp. its split at "." to strip milliseconds out.
            spawntimeobject = datetime(now_est.year,now_est.month,now_est.day,int(spawntimesplit[0]),int(spawntimesplit[1]),int(spawntimesplit[2]))
            spawngmt = spawntimeobject + timedelta(hours=4)
            unixtime = str((time.mktime(spawngmt.timetuple()))).split(".")[0]
            #send the discord message
            embed = DiscordEmbed(title='World Boss Spawning!', color='03b2f8')
            embed.set_thumbnail(url=json_object[tweet_id]['images'][0])
            embed.set_image(url=json_object[tweet_id]['images'][1])
            embed.add_embed_field(name="Boss", value=boss_name)
            embed.add_embed_field(name="Spawn Countdown", value=f"<t:{unixtime}:R>")
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

def timeconvert(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
    elif str1[-2:] == "AM":
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]

# Schedule the job to run every minute
print("Start!")
schedule.every(5).minutes.do(scrape_and_post_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)

from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import dateutil.parser as parser
import os
import schedule
import time
import json
import requests
import pytz

load_dotenv()

# Discord webhook URL
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# Nitter user whose tweets you want to scrape
NITTER_URL = "https://nitter.1d4.us/game8_d4boss"
UTC=pytz.UTC

def scrape_and_post_tweet():
    try:
        response = requests.get(NITTER_URL)
    except:
        print("maybe site is dead, will try again later")
    soup = BeautifulSoup(response.content, "html.parser")
    timeline_container = soup.find("div", class_="timeline-container")
    tweet_elements = timeline_container.find_all("div", class_="timeline-item")
    tweet = tweet_elements[1]

    now_utc = datetime.now(timezone.utc)
    oldtweettime = now_utc + timedelta(minutes=-5)
    tweet_timestamp = tweet.find("span", class_="tweet-date")
    thetime = (tweet_timestamp.find("a"))["title"]
    utctweettime = datetime.strptime(thetime, '%b %d, %Y · %I:%M %p %Z')
    utctweettime = utctweettime.replace(tzinfo=UTC)

    if oldtweettime > utctweettime:
        print("too old")
        return

    tweet_content = tweet.find("div", class_="tweet-content media-body").text.strip()
    if "spawn" not in tweet_content.lower():
        print("dont care")
        return
    if "predict" in tweet_content.lower():
        print("dont care")
        return
    split = tweet_content.split(" ")
    if split[1]!="will" and "spawn" not in split[1]:
        boss_name = f"{split[0]} {split[1]}"
    else:
        boss_name = split[0]
    tweet_img = tweet.find_all('a', class_="still-image", href=True)
    thumbnail = f"https://nitter.1d4.us{tweet_img[0]['href']}"
    image = f"https://nitter.1d4.us{tweet_img[1]['href']}"

    current_date_str = datetime.now().strftime('%Y-%m-%d')
    spawn_time_string = (f"{split[-3]} {split[-2]} {split[-1]}").strip("()-")
    spawn_dt_string = f"{current_date_str} {spawn_time_string}"
    spawn_timestamp_obj = datetime.strptime(spawn_dt_string, '%Y-%m-%d %I:%M %p %Z')
    unix_timestamp = int(spawn_timestamp_obj.timestamp())
    spawn_countdown = f"<t:{unix_timestamp}:R>"

    embed = DiscordEmbed(title='World Boss Spawning!', color='03b2f8')
    embed.set_thumbnail(url=thumbnail)
    embed.set_image(url=image)
    embed.add_embed_field(name="Boss", value=boss_name)
    embed.add_embed_field(name="Spawn Countdown", value=spawn_countdown)
    embed.set_footer(text="https://github.com/elightcap/d4bot")
    embed.set_timestamp()
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content="@here")
    webhook.add_embed(embed)
    response = webhook.execute()

print("start")
schedule.every(5).minutes.do(scrape_and_post_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)
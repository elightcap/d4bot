# DIABLO 4 WORLD BOSS BOT

## Description
This is a discord bot to notify when a World Boss is going to spawn.  It scrapes the twitter account game8_d4boss for new boss events, and posts when it sees one. The twitter check runs every 5 minutes, but this can be adjusted in line 51 of `main.py`, however I wouldn't go too much lower, as twitter does not seem to like this method.

## Installation

### Docker (PREFERRED)
NOTE: First run might take a little while because we need to install Firefox inside the container
1. Install [Docker](https://docs.docker.com/get-docker/)
2. Clone this repo. `git clone https://github.com/elightcap/d4bot`
3. Move the sample.env and add your discord webhook to it. `cp sample.env .env && nano.env`
4. Start the container. `docker compose up -d` or for older docker installs `docker-compose up -d`

### Manually
1. Clone this repo. `git clone https://github.com/elightcap/d4bot`
2. Install dependencies. `pip install -r requirements.txt`
3. Install firefox.  This is OS/distro dependant.
4. Move the sample.env and add your discord webhook to it. `cp sample.env .env && nano.env`
5. Run bot. `python3 main.py`

Recommend using something like tmux when building manually.

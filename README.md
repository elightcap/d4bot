#DIABLO 4 WORLD BOSS BOT

##Description
This is a discord bot to notify when a World Boss is going to spawn.  It scrapes the twitter account game8_d4boss for new boss events, and posts when it sees one. The discord check runs every 5 minutes, but this can be adjusted in line 51 of `main.py`, however I wouldn't go too much lower, as twitter does not seem to like this method.

##Installation

1. Clone this repo. `git clone https://github.com/elightcap/d4bot`
2. Install dependencies. `pip install -r requirements.txt`
3. Mov the sample.env and add your discord webhook to it. `cp sample.env .env && nano.env`
4. Run bot. `python3 main.py`

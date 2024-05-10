# Berlin Ausländerbehörde Termin Bot

This is a fork of [this repository](https://github.com/capital-G/berlin-auslanderbehorde-termin-bot) by [capital-G](https://github.com/capital-G).

A [Selenium](https://www.selenium.dev/) bot for obtaining an appointment at the [Landesamt für Einwanderung](https://otv.verwalt-berlin.de/ams/TerminBuchen) aka Ausänderbehörde in Berlin. It will notify the user if new appointments are available via a Telegram bot (setup below).

I did not want to open source this as this makes it harder for the people without IT knowledge to obtain an appointment, but as there are already people who make a benefit of this (50 euro per appointment!) I thought it would be a good thing to make the tools available to everyone. This project is therefore a counter measurement against those people as well as the inability of the Ausländerbehörde to provide sufficient appointments.

Take a look at the video [Hinter verschlossenen Türen – Mysterium Ausländerbehörde - ZDF Magazin Royale](https://www.youtube.com/watch?v=s7HrAGlni50) to find out more about the bad shape of this agency.

## Setup

* `git clone https://github.com/bleykauf/berlin-auslanderbehorde-termin-bot.git`
* Setup a virtualenv via `virtualenv venv` and activate it
* Install dependencies via `pip3 install -r requirements.txt`
* Put a `chromedriver` binary from <https://chromedriver.chromium.org/downloads> into the directory
* Configure `berlin_bot.py` according to your needs (see below)
* Create a Telegram bot by messaging `@botfather` and following the instructions in the Telegram app 
* Take note of the bot's token
* Start a chat with the bot and message something to it
* Check `https://api.telegram.org/bot{TOKEN}/getUpdates` and get the chat ID (`result.0.message.chat.id`)
* Create a file `.env` in the cloned repository directory with the following content:

```
TELEGRAM_KEY={TOKEN}
CHAT_ID={CHAT ID}
```

* Start the bot via `python3 berlin_bot.py`

## Configuration and Support

I do not give any kind of support and/or advice on how to configure this bot as I wrote this for a friend of mine and thankfully she was able to get an appointment with this bot.
You can read the [selenium docs](https://selenium-python.readthedocs.io/locating-elements.html#) and adjust `berlin_bot.py` in order to configure it according to your needs.

## License

AGPL-3.0

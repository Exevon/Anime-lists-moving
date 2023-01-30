# Anime lists moving
App moves every anime from Shikimori lists to MyAnimeList.

I've been using [Shikimori](https://shikimori.one/) to save animes that I'm planning to watch, watched already and ones I'm currentry watching. But then I found [MyAnimeList](https://myanimelist.net/), and it seems more comfortable to use for me. I wanted to move every single anime from my Shikimori lists to MyAnimeList but doing it manualy would take about 6 hours. So I made this script in couple days to save some time and move all titles automaticaly.

## Required modules:
* Selenium
* Beautiful Soup
* Requests
* Lxml
* Colorama

## How to use
Run `main.py` in your console. Then you will need to enter a link to [Shikimori](https://shikimori.one/) account.
Then type your username and password from [MyAnimeList](https://myanimelist.net/) account.
You can choose if you want to display a browser or not. (Type "+" if yes, otherwise "-")

## Structure
* `list_parser.py` gets data about all lists of anime from Shikimori account and writes everything into `to-move.txt` file.
* `logger.py` logging successful and failed additions from `to-move.txt` into your MyAnimeList profile. Saves logs into `successful.txt` and `failed.txt` files.
* `main.py` Uses entered username and password to log into MyAnimeList account. Then uses `list_parser.py` to recive anime lists from Shikimori and `logger.py` to start logging. Reads every line from `to-move.txt` and searches for current anime by title. Adds anime to appropriate list and selects score.

## Fixes needed:
1. There's no checking if current anime already in your MyAnimeList profile and adds it anyways.
2. While searching title, sometimes first result isn't what we need.

Example:
When searching for "One Piece", first result is "One Piece Film: Gold". So wrong anime will be added to profile.

## Future features:
1. Adding anime to "Favorites" list.
2. Print to console total amount of successful and failed additions.

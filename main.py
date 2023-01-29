# Required modules:
# selenium, requests, bs4, lxml, colorama

import time
from colorama import Fore

from selenium import webdriver
from selenium.webdriver.common.by import By

import logger
import list_parser

class ListMover():
    def __init__(self, show_window) -> None:
        # Options for browser
        option = webdriver.FirefoxOptions()
        option.headless = True # Hides window
        if show_window == "+":
            option.headless = False
        # Creating browser driver
        self.__browser = webdriver.Firefox(options=option)
        try:
            self.__browser.get("https://myanimelist.net/login.php?from=%2F")
        except Exception:
            print(Fore.LIGHTRED_EX + "[X]" + Fore.RESET + f" Can't get https://myanimelist.net/login.php?from=%2F page.")
            return
        self.__log = logger.Logger()


    def login_into_account(self, username, password):
        """ Login into MyAnimeList account with given username and password """
        print(Fore.LIGHTGREEN_EX +"[INFO]" +Fore.RESET + " Logging into your MyAnimeList account.")
        username_field = self.__browser.find_element(By.XPATH, '//*[@id="loginUserName"]')
        username_field.send_keys(username)
        password_field = self.__browser.find_element(By.XPATH, '//*[@id="login-password"]')
        password_field.send_keys(password)
        login_button = self.__browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td/form/div/p[6]/input')
        login_button.click()
        self.__logedIn = False 
        time.sleep(5) # Wait for page to load
        # If liging into MyAnimeList account failed
        try:
            self.__browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td/form/div/p[6]/input')
        except Exception:
            self.__logedIn = True


    def find_anime_by_name(self, title):
        """ Find an anime page on MyAnimeList by given title """
        print(Fore.YELLOW + "[SEARCH] " + Fore.RESET + title)
        self.__browser.get(f"https://myanimelist.net/search/all?q={title}&cat=anime")
        # Parsing link to current anime add-page
        add_anime_link = self.__browser.find_element(By.CLASS_NAME, "Lightbox_AddEdit").get_attribute("href")
        self.__browser.get(add_anime_link)


    def select_by_value(self, webElement, value):
        """ Selects an item given by the argument 'value' within the 'WebElement' object """
        options = webElement.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.get_attribute("value") == value:
                option.click()


    def add_anime_to_list(self, title, score, list_type):
        """ Adds current anime to given list by type """
        # Get add-page of current anime
        self.find_anime_by_name(title)

        if score.isdigit():
            print(f"[ADDING] {title} [{score}] -> {list_type}")
        else:
            print(f"[ADDING] {title} [-] -> {list_type}")

        # Selector of list types
        select = self.__browser.find_element(By.ID, "add_anime_status")
        select.click()

        # Selecting type of list based on given value "list_type"
        match list_type:
            case "Watching":
                self.select_by_value(select, "1")
            case "Completed":
                self.select_by_value(select, "2")
            case "Planned":
                self.select_by_value(select, "6")
            case "Dropped":
                self.select_by_value(select, "4")
        
        # Selecting score to current anime
        if score.isdigit():
            select_score = self.__browser.find_element(By.ID, "add_anime_score")
            self.select_by_value(select_score, score)
        time.sleep(0.5)
        # Submiting
        self.__browser.execute_script("document.getElementsByClassName('inputButton main_submit')[1].click()")
        time.sleep(1)


    def start_moving(self, shikimori_profile_link):
        # Checking if user is logged in MyAnimeList
        if not self.__logedIn:
            print(Fore.LIGHTRED_EX + "[X]" + Fore.RESET + " Can't login into your MyAnimeList account.")
            return

        # Parsing data from shikimori profile
        self.__parser = list_parser.Shikimori_parser(shikimori_profile_link)
        self.__parser.make_tomove_lists_file()

        # Opening file with recieved data
        tmFile = open("to-move.txt", "r")
        titles = tmFile.readlines()
        list_type = None

        failed_count = 0
        for line in titles:
            # If current line is list type header or total score
            if line.startswith("== "):
                list_type = line[3:len(line)-1]
                continue
            if line.startswith("TOTAL: ") or line == "\n":
                continue

            # Separating score from title
            title, score = line.split(" -> ")[0], line.split(" -> ")[1]
            score = score[:len(score)-1] # Removing "\n" symbol in the end of the line

            try:
                self.add_anime_to_list(title, score, list_type)
            except Exception:
                failed_count += 1
                self.__log.add_failed({
                    "title": title, "link": f"https://myanimelist.net/search/all?q={title}&cat=anime"
                })
                # In case MyAnimeList wants to vericy that you are not a robot
                if failed_count >= 3:
                    failed_count = 0
                    print(Fore.YELLOW + "[WARNING] " + Fore.RESET + "More than 3 failed in a row. "
                    + "MyAnimeList may verify that you are not a robot."
                    + " Submit on MyAnimeList and then press ENTER to countinue.")
                    input()
            else:
                failed_count = 0
                self.__log.add_successful({
                    "title": title, "link": f"https://myanimelist.net/search/all?q={title}&cat=anime"
                })
        self.__log.end_logging()
        print(Fore.LIGHTGREEN_EX + "Done!")


if __name__ == "__main__":
    # Inputing data
    shikimori_link = input("Enter your Shikimori profile link: ")
    username = input("Enter MyAnimeList username: ")
    password = input("Enter MyAnimeList password: ")
    show_window = input("Do you want to display browser window? (+/-): ")

    mover = ListMover(show_window)
    mover.login_into_account(username, password)
    mover.start_moving(shikimori_link)

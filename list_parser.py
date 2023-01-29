import requests
from bs4 import BeautifulSoup
from colorama import Fore

class Shikimori_parser():
    def __init__(self, profile_link) -> None:
        print(Fore.LIGHTGREEN_EX + "[INFO] " + Fore.RESET + f"Started parsing anime lists from: {profile_link}")
        # Setting valid useragent
        self.__header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"}
        # Getting the user page
        link = profile_link
        self.__is_link_valid = True
        try:
            recponce = requests.get(link, headers=self.__header).text
        except Exception:
            self.__is_link_valid = False
            print(Fore.LIGHTRED_EX + "[X]" + Fore.RESET + f" Cant send request to link: {profile_link}")
            return
        self.__page = BeautifulSoup(recponce,"lxml")

        # Finding block with anime lsists
        anime_lists_block = self.__page.find_all("div", class_="stat_name")
        # Finding link to page of every anime list
        self.__lst_links = []
        for _list in anime_lists_block:
            self.__lst_links.append(_list.find("a").get("href"))


    def get_anime_list_content(self, link):
        """ Gets names of all animes of current list """
        # Requesting page
        lst_recponce = requests.get(link, headers=self.__header).text
        list_page = BeautifulSoup(lst_recponce, "lxml")
        # Finding all list elements
        list_block = list_page.find("tbody", class_="entries")
        list_block.find_all("tr", class_="user_rate")

        list_content = [] # Anime stats
        for target in list_block:
            # Adding stats of element (data-target_name and current-value) to list content
            list_content.append( [target.get("data-target_name"), target.find("span", class_="current-value").text] )
        return list_content


    def make_tomove_lists_file(self):
        """ Writes content of all lists into file """
        # If link is invalid
        if not self.__is_link_valid:
            print(Fore.LIGHTRED_EX + "[X]" + Fore.RESET + f" Cant make file. Link is invalid.")
            return

        print(Fore.LIGHTGREEN_EX + "[INFO] " + Fore.RESET + "Making to-move file")
        # For deviding lists to categories in to-move file
        headers = ["== Planned", "== Watching", "== Completed", "== Dropped"]
        failed = [] # Failed while writing into file

        with open("to-move.txt", "w") as tm_file:
            for i in range(len(self.__lst_links)):
                total = 0 # Count total elements in current list
                # Writing current category
                tm_file.write(f"{headers[i]}\n")

                # Current list content
                current_list = self.get_anime_list_content(self.__lst_links[i])
                for elem in current_list:
                    try:
                        tm_file.write(f"{elem[0]} -> {elem[1]}\n")
                        total += 1
                    except UnicodeEncodeError:
                        # If impossible to write into file
                        failed.append(elem)

                # Devide categories with total score and empty line
                tm_file.write(f"TOTAL: {total}\n\n")

            # Printing failed list into console
            if failed:
                print(Fore.LIGHTRED_EX + "[X]" + Fore.RESET + f" Failed to write into file:")
                for i in failed:
                    print(">", *i)


if __name__ == "__main__":
    link = input("Enter shikimori profile link: ")
    parser = Shikimori_parser(link)
    parser.make_tomove_lists_file()
    print(Fore.LIGHTGREEN_EX + "Done")

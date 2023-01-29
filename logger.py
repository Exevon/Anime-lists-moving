from colorama import Fore

class Logger():
    def __init__(self) -> None:
        # Count of successful and failed operations
        self.successful_count = 0
        self.failed_count = 0
        # Opening files for logging
        self.successful_file = open("lst_logs\\successful.txt", "w")
        self.failed_file = open("lst_logs\\failed.txt", "w")

    
    def add_successful(self, item):
        """ Adds log into successful.txt """
        self.successful_count += 1
        # I just like colored logging :)
        print(Fore.LIGHTGREEN_EX + "[SUCCESS]" + Fore.RESET + f" {item['title']}.\n")
        self.successful_file.write(f"{item['title']} - {item['link']}\n")


    def add_failed(self, item):
        """ Adds log into failed.txt """
        self.failed_count += 1
        # I really like colors
        print(Fore.LIGHTRED_EX + "[FAILED]" + Fore.RESET + f"  {item['title']}.\n")
        self.failed_file.write(f"{item['title']} - {item['link']}\n")


    def end_logging(self):
        """ Adds total count of successful and failed operations and closes files """
        self.successful_file.write(f"TOTAL: {self.successful_count}")
        self.successful_file.close()
        self.failed_file.write(f"TOTAL: {self.failed_count}")
        self.failed_file.close()



if __name__ == "__main__":
    # Testing work of code
    logger = Logger()
    test_data_s = [
        {"title": "Babylon", "link": "https://shikimori.one/animes/37525-babylon"},
        {"title": "Dr. Stone", "link": "https://shikimori.one/animes/z38691-dr-stone"},
        {"title": "Clannad ", "link": "https://shikimori.one/animes/z2167-clannad"},
    ]
    for i in test_data_s:
        logger.add_successful(i)

    test_data_f = [
        {"title": "Kimetsu no Yaiba", "link": "https://shikimori.one/animes/z38000-kimetsu-no-yaiba"},
        {"title": "Gabriel DropOut", "link": "https://shikimori.one/animes/z33731-gabriel-dropout"},
        {"title": "Sword Art Online: Alicization", "link": "https://shikimori.one/animes/z36474-sword-art-online-alicization"},
        {"title": "Date A Live", "link": "https://shikimori.one/animes/15583-date-a-live"}
    ]
    for i in test_data_f:
        logger.add_failed(i)

    logger.end_logging()

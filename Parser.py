from urllib.parse import urldefrag, urljoin
from bs4 import BeautifulSoup
import requests
import os
import random
import curses
import sys


def main():
    game = ParserGame()

class Parser:

    def __init__(self, url):
        # todo try-except
        self.url = url.decode("utf-8")
        result = requests.get(url)
        if result.status_code == 200:
            self.html = result.content
            self.soup = BeautifulSoup(self.html, "lxml")
        else:
            self.html = ""

    def get_links(self):
        links = set()
        for link in self.soup.find_all("a"):
            try:
                defragged_url = urldefrag(urljoin(self.url, link.get("href")))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            links.add(defragged_url[0])
        return links

class ParserGame:

    random_links = []
    stdscr = 0

    def __init__(self):
        # curses init
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.game_loop()

    def __del__(self):
        # curses deinit
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def game_loop(self):
        self.stdscr.clear()
        while True:
            if self.random_links:
                self.format_game()
            else:
                url = self.__input(5, 5, "Give me a site!")
                # todo error handling not a site
                parser = Parser(url)
                self.random_links = random.sample(parser.get_links(), 4)
                # todo error handling valuerror
                self.format_game()
                input()

    def format_game(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 10, self.random_links[0] + "\n")
        self.stdscr.addstr(5, 15, self.random_links[1] + "\n")
        self.stdscr.addstr(10, 10, self.random_links[2] + "\n")
        self.stdscr.addstr(5, 0, self.random_links[3] + "\n")
        self.stdscr.refresh()

    def __input(self, row, col, prompt_string):
        curses.echo()
        self.stdscr.addstr(row, col, prompt_string)
        self.stdscr.refresh()
        input_var = self.stdscr.getstr(row + 1, col, 100)
        return input_var


if __name__ == "__main__":
    main()

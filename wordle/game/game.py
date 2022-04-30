import curses
import random
from turtle import st

from .board import Board
from ..config import DATA_PATH, COLOR_NUMBERS


class Game:
    def __init__(self) -> None:
        self.board = Board()

    def play(self):
        self.word_list = self.__load_word_list()
        self.word = random.choice(self.word_list)

        curses.wrapper(self.__loop)

    def __loop(self, stdscr):
        curses.init_pair(
            COLOR_NUMBERS.incorrect, curses.COLOR_WHITE, curses.COLOR_BLACK
        )
        curses.init_pair(
            COLOR_NUMBERS.semi_correct, curses.COLOR_WHITE, curses.COLOR_YELLOW
        )
        curses.init_pair(
            COLOR_NUMBERS.correct, curses.COLOR_WHITE, curses.COLOR_GREEN
        )

        self.__draw(stdscr)
        while self.board.curr_line < self.board.num_lines:
            line = self.board.lines[self.board.curr_line]
            char = chr(stdscr.getch())
            if not char.isalpha():  # Will not allow backspace
                continue
            line.enter_letter(char)
            if line.curr_pos == line.length:
                self.board.enter_word()
            self.__draw(stdscr)

    def __draw(self, stdscr):
        stdscr.clear()
        for line in self.board.lines:
            for letter in line.values:
                stdscr.addstr(
                    f" {letter.value or '_'} ",
                    curses.color_pair(letter.bg_color)
                )
                stdscr.addstr(' ')
            stdscr.addstr('\n\r')
        stdscr.refresh()

    @staticmethod
    def __load_word_list() -> str:
        with open(f'{DATA_PATH}/wordle_list.txt', 'r') as word_file:
            return [word.strip() for word in word_file]

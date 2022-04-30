import curses
import random
from turtle import st

from .board import Board
from ..config import DATA_PATH, COLOR_NUMBERS, GAME_KEYS


def init_colors():
    curses.init_pair(
        COLOR_NUMBERS.incorrect, curses.COLOR_WHITE, curses.COLOR_BLACK
    )
    curses.init_pair(
        COLOR_NUMBERS.semi_correct, curses.COLOR_WHITE, curses.COLOR_YELLOW
    )
    curses.init_pair(
        COLOR_NUMBERS.correct, curses.COLOR_WHITE, curses.COLOR_GREEN
    )


class Game:
    def play(self):
        self.__init_board()

        self.word_list = self.__load_word_list()
        self.word = random.choice(self.word_list)
        self.solved = False

        curses.wrapper(self.__loop)

    def __loop(self, stdscr) -> None:
        init_colors()

        self.__draw(stdscr)
        while (self.board.curr_line < self.board.num_lines
                and not self.solved):
            ch = stdscr.getch()
            if self.__update_board(ch):  # Only draw when update occurs
                self.__draw(stdscr)

        self.__post_game(stdscr)

    def __draw(self, stdscr):
        stdscr.clear()
        for line in self.board.lines:
            for letter in line.values:
                stdscr.addstr(
                    f" {letter.value or '_'}  ",
                    curses.color_pair(letter.bg_color)
                )
            stdscr.addstr('\n\r')
        stdscr.refresh()

    def __init_board(self):
        self.board = Board()

    def __update_board(self, char: int) -> bool:
        line = self.board.lines[self.board.curr_line]

        if chr(char).isalpha():
            line.enter_letter(chr(char))
        elif char == GAME_KEYS.backspace:
            line.delete_letter()
        elif char == GAME_KEYS.enter:
            if line.curr_pos == line.length - 1:
                self.board.enter_word()
                self.solved = self.__check_entered_word()
        else:
            return False  # invalid input
        return True  # Board updated

    def __check_entered_word(self):
        line = self.board.lines[self.board.curr_line - 1]
        word = ''.join([letter.value for letter in line.values
                        if letter.value])
        return True if word == self.word else False

    def __post_game(self, stdscr):
        if self.solved:
            stdscr.addstr('Congratulations!\n')
        else:
            stdscr.addstr(f'The word was "{self.word}!"\n')
        stdscr.addstr('\nPress Enter to play again.\n')
        stdscr.addstr('Press any other key to quit.\n')
        stdscr.refresh()

        ch = stdscr.getch()  # Halts until key press
        if ch == GAME_KEYS.enter:
            self.play()

    @staticmethod
    def __load_word_list() -> str:
        with open(f'{DATA_PATH}/wordle_list.txt', 'r') as word_file:
            return [word.strip() for word in word_file]

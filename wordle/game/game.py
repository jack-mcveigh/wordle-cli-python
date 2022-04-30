import time
import curses
import random
import collections

from .board import Board, LetterState
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
        self.word = 'APPLE' or random.choice(self.word_list)
        self.word_letter_counts = collections.Counter(self.word)

        self.solved = False
        self.stdscr = None

        curses.wrapper(self.__loop)

    def __loop(self, stdscr) -> None:
        self.stdscr = stdscr
        init_colors()

        self.__draw()
        while (self.board.curr_line < self.board.num_lines
                and not self.solved):
            ch = stdscr.getch()
            if self.__update_board(ch):  # Only draw when update occurs
                self.__draw()

        self.__post_game()

    def __draw(self):
        self.stdscr.clear()
        for line in self.board.lines:
            for letter in line.values:
                self.stdscr.addstr(
                    f" {letter.value or '_'}  ",
                    curses.color_pair(letter.bg_color)
                )
            self.stdscr.addstr('\n\r')
        self.stdscr.refresh()

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
        entered_word = str(line)

        test_letter_counts = self.word_letter_counts.copy()

        # Find green letters
        for correct_letter, entered_letter in zip(self.word, line.values):
            if correct_letter == entered_letter.value:
                test_letter_counts[entered_letter.value] -= 1
                entered_letter.state = LetterState.correct

        # Find yellow letters
        for entered_letter in line.values:
            if test_letter_counts[entered_letter.value]:
                test_letter_counts[entered_letter.value] -= 1
                entered_letter.state = LetterState.semi_correct

        self.__draw_result()

        return True if entered_word == self.word else False

    def __draw_result(self):
        self.stdscr.move(self.board.curr_line - 1, 0)

        line = self.board.lines[self.board.curr_line - 1]
        for letter in line.values:
            time.sleep(0.25)
            self.stdscr.addstr(
                f" {letter.value}  ",
                curses.color_pair(letter.bg_color)
            )
            self.stdscr.refresh()
        self.stdscr.addstr('\n\r')

    def __post_game(self):
        if self.solved:
            self.stdscr.addstr('Congratulations!\n')
        else:
            self.stdscr.addstr(f'The word was "{self.word}!"\n')
        self.stdscr.addstr('\nPress Enter to play again.\n')
        self.stdscr.addstr('Press any other key to quit.\n')
        self.stdscr.refresh()

        ch = self.stdscr.getch()  # Halts until key press
        if ch == GAME_KEYS.enter:
            self.play()

    @staticmethod
    def __load_word_list() -> str:
        with open(f'{DATA_PATH}/wordle_list.txt', 'r') as word_file:
            return [word.strip() for word in word_file]

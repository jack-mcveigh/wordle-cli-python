import curses
from enum import auto, Enum
from typing import List, Optional

from ..config import COLOR_NUMBERS

WORD_LIST = ['crate', 'crane', 'train', 'smart']
NUMBER_OF_LINES = 6
LINE_LENGTH = 5


class LetterState(Enum):
    incorrect = COLOR_NUMBERS.incorrect
    semi_correct = COLOR_NUMBERS.incorrect
    correct = COLOR_NUMBERS.correct


class Letter:
    value: Optional[str] = None
    state: Optional[LetterState] = None

    @property
    def bg_color(self) -> int:
        if self.state is None:
            return LetterState.incorrect.value
        return self.state.value


class Line:
    values: List[Letter]
    is_word: Optional[bool]
    length = LINE_LENGTH
    curr_pos = 0

    def __init__(self):
        self.values = [Letter() for _ in range(self.length)]

    def enter_letter(self, letter: str) -> None:
        if self.curr_pos == self.length:
            return
        self.values[self.curr_pos].value = letter.upper()
        self.curr_pos += 1

    def delete_letter(self) -> None:
        if self.curr_pos == 0:
            return
        self.values[self.curr_pos].value = None
        self.curr_pos -= 1


class Board:
    lines: List[Line]
    result: Optional[bool] = None
    num_lines = NUMBER_OF_LINES
    curr_line = 0

    def __init__(self):
        self.lines = [Line() for _ in range(self.num_lines)]

    def enter_word(self) -> None:
        line = self.lines[self.curr_line]
        word = ''.join([letter.value for letter in line.values])
        self.check_word(word)
        self.curr_line += 1

    @staticmethod
    def check_word(word) -> bool:
        print('Is it a word?')
        return True if word in WORD_LIST else False


if __name__ == '__main__':
    board = Board()

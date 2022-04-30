import os
from dataclasses import dataclass

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, 'data')


@dataclass
class COLOR_NUMBERS:
    incorrect = 1
    semi_correct = 2
    correct = 3

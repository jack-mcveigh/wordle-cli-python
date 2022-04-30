import argparse

from .game import Game
from . import __version__


def _get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A Wordle Clone for your Terminal, written in Python.'
    )
    parser.add_argument(
        '-H', '--hard',
        action='store_true', default=False,
        help='Force hard mode. (NOT YET IMPLEMENTED)'
    )
    parser.add_argument(
        '-v', '--version',
        action='version', version=f'%(prog)s {__version__}',
        help='Show the version number and exit'
    )
    return parser.parse_args()


def entry_point() -> None:
    _ = _get_arguments()

    game = Game()
    game.play()


if __name__ == '__main__':
    entry_point()

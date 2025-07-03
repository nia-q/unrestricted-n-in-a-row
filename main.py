from game import Game, GameExit
from color_printer import ColorPrinter
import sys


def main():
    printer = ColorPrinter()
    try:
        printer.print_colored("Enter name for Player 1: ")
        name1 = input().strip()
        printer.print_colored("Enter name for Player 2: ")
        name2 = input().strip()
        game = Game(name1, name2)
        game.play()
    except GameExit:
        printer.print_colored("Game exited. Thanks for playing!")
        sys.exit(0)
    except KeyboardInterrupt:
        printer.print_colored("\nGame interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
from game import Game, GameExit
import sys


def main():
    try:
        name1 = input("Enter name for Player 1: ").strip()
        name2 = input("Enter name for Player 2: ").strip()
        game = Game(name1, name2)
        game.play()
    except GameExit:
        print("Game exited. Thanks for playing!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
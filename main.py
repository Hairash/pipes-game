from game import Game

balls = [
    [0, (0, 0)],
    [0, (4, 1)],
    [1, (7, 9)],
    [1, (8, 6)],
]


def main():
    game = Game(600, 10, balls=balls)
    game.start()


if __name__ == '__main__':
    main()

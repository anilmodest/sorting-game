from SortingGame import SortingGame;


def main():
    gameSorter = SortingGame(3);
    path = gameSorter.solve_game();
    print('print')
    print(*path, sep=", ")


if __name__ == '__main__':
    main()
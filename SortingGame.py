import math;
from MinHeap import MinHeap;
import numpy as np;



class SortingGame:
    def __init__(self, dimension):
        self.board = [];
        self.path = [];
        self.dimension = dimension;
        self.lastMove = None;
        self.Direction = {
            "LEFT": "left",
            "RIGHT": "right",
            "UP": "up",
            "DOWN": "down"
        }
        self.puzzle_init();

    def print(self, board):
        for i in range(len(board)):
            print(*board[i])
        print('-----------')
        print('\n')


    def puzzle_init(self):
        self.randomize_board();
        #self.board = np.random.randint(self.dimension*self.dimension -1, size=(self.dimension, self.dimension))
        # for i in range(0, self.dimension):
        #     self.board.append([]);
        #     for j in range(0, self.dimension):
        #         if i == self.dimension - 1 and j == self.dimension - 1:
        #             self.board[i].append(0);
        #         else:
        #             self.board[i].append(self.dimension * i + j + 1)
        #self.print();

    def randomize_board(self):
        maxNum = self.dimension * self.dimension;
        minNum = 0;
        nums = [];
        while len(nums) < maxNum:
            randonNum = np.random.randint(minNum, maxNum);
            if nums.__contains__(randonNum) == False:
                nums.append(randonNum);
        counter = 0;
        for i in range(0, self.dimension):
            self.board.append([]);
            for j in range(0, self.dimension):
                self.board[i].append(nums[counter]);
                counter = counter + 1;



    def get_blankspace_position(self):
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if self.board[i][j] == 0:
                    return [i, j];

    def swap_numbers(self, i1, j1, i2, j2):
        temp = self.board[i1][j1];
        self.board[i1][j1] = self.board[i2][j2];
        self.board[i2][j2] = temp;

    def get_move(self, number):
        blankSpacePosition = self.get_blankspace_position();
        line = blankSpacePosition[0];
        column = blankSpacePosition[1];
        if line > 0 and number == self.board[line -1][column] :
            return self.Direction["DOWN"];
        elif line < self.dimension - 1 and number == self.board[line + 1][column] :
            return self.Direction["UP"];
        elif column > 0 and  number == self.board[line][column -1] :
            return self.Direction["RIGHT"];
        elif column < self.dimension -1 and number == self.board[line][column + 1] :
            return self.Direction["LEFT"];
        return None;

    def move(self, number):
        move = self.get_move(number);
        if move is not None:
            blankSpacePosition = self.get_blankspace_position();
            line = blankSpacePosition[0];
            column = blankSpacePosition[1];
            if move == self.Direction["LEFT"] :
                self.swap_numbers(line, column, line, column + 1);
            elif move == self.Direction["RIGHT"]:
                self.swap_numbers(line, column, line, column - 1);
            elif move == self.Direction["UP"]:
                self.swap_numbers(line, column, line + 1, column);
            elif move == self.Direction["DOWN"]:
                self.swap_numbers(line, column, line -1, column);

            self.lastMove = number;
            return move;
    def is_goal_state(self):
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                number = self.board[i][j];
                if number is not 0:
                    originalLine = math.floor((number -1) / self.dimension);
                    originalColumn = (number - 1) % self.dimension;
                    if i != originalLine or j != originalColumn :
                        return False;
        return True;

    def get_copy(self):
        newGame = SortingGame(self.dimension);
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                newGame.board[i][j] = self.board[i][j];

        for i in range(0, len(self.path)):
             newGame.path.append(self.path[i]);
        return newGame;

    def get_allowed_moves(self):
        allowedMoves = [];
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                number = self.board[i][j];
                if self.get_move(number) is not None:
                    allowedMoves.append(number)
        return allowedMoves;

    def visit(self):
        children = [];
        allowedMoves = self.get_allowed_moves();
        for i in range(0, len(allowedMoves)):
            move = allowedMoves[i];
            if move is not self.lastMove:
                newInstance = self.get_copy();
                newInstance.move(move);
                newInstance.path.append(move);
                children.append(newInstance);
                self.print(newInstance.board);
        return children

    def g_func(self):
        return len(self.path);

    def get_distance(self):
        distance = 0;
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                number = self.board[i][j];
                if number is not 0:
                    originalLine = math.floor((number - 1) / self.dimension);
                    originalColumn = (number - 1) % self.dimension;
                    distance += abs(1 - originalLine) + abs(j - originalColumn);

        return distance;


    def h_func(self):
        return self.get_distance();

    def __lt__(self, other):
        return self.g_func() + self.h_func() < other.g_func() + other.h_func();

    def solve_game(self):
        states = MinHeap();
        self.path = [];
        states.push(0, self);
        while len(states) > 0 :
            state = states.pop();
            if state.is_goal_state():
                return state.path;
            children = state.visit();
            for i in range(0, len(children)):
                child = children[i];
                f = child.g_func() + child.h_func();
                states.push(f, child);
        self.print((self.board))

import os
import random

class Board:
    def __init__(self):
        self.board = [
            [
                str(3 * row + column + 1)  # Calculate the position number
                for column in range(3)      # Iterate over columns
            ]
            for row in range(3)             # Iterate over rows
        ]

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear') # Clears the screen in every print

        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def update_board(self, position, player):
        row, column = divmod(position - 1, 3)
        if self.board[row][column] not in ["X", "O"]:
            self.board[row][column] = player.symbol
            return True
        else:
            print("This position is already occupied. Choose another one.")
            return False

    def check_winner(self, player):
        symbol = player.symbol

        # Check rows
        for row in self.board:
            if all([cell == symbol for cell in row]): # Checks each cell in row
                return True

        # Check columns
        for col in range(3):
            if all([self.board[row][col] == symbol for row in range(3)]): # Checks each row in column
                return True

        # Check diagonals
        if all([self.board[i][i] == symbol for i in range(3)]) or all([self.board[i][2 - i] == symbol for i in range(3)]):
            return True

        return False

    def check_full(self):
        return all([cell in ["X", "O"] for row in self.board for cell in row])

    def reset_board(self):
        self.board = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def make_move(self, board, position):
        if board.update_board(position, self):
            print(f"{self.name} placed {self.symbol} at position {position}")
            return True
        else:
            print(f"{self.name}, that move was invalid. Try again.")
            return False

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = None
        self.player2 = None
        self.current_player = None

    def setup_players(self):
        name1 = input("Enter name for Player 1 (X): ")
        name2 = input("Enter name for Player 2 (O): ")

        self.player1 = Player(name1, "X")
        self.player2 = Player(name2, "O")

        self.current_player = random.choice([self.player1, self.player2])
        print(f"{self.current_player.name} will start first!")

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def play(self):
        self.setup_players()

        while True:
            self.board.print_board()
            position = self.get_player_input()
            if self.current_player.make_move(self.board, position):
                if self.board.check_winner(self.current_player):
                    self.board.print_board()
                    print(f"{self.current_player.name} wins!")
                    break

                if self.board.check_full():
                    self.board.print_board()
                    print("It's a draw!")
                    break

                self.switch_player()

    def get_player_input(self):
        while True:
            try:
                position = int(input(f"{self.current_player.name}, enter a position (1-9): "))
                if position in range(1, 10):
                    return position
                else:
                    print("Invalid input. Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
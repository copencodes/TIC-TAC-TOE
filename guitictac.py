import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.bot_player = "O"
        self.buttons = []

        self.create_board()

    def create_board(self):
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.master, text=" ", font=("Helvetica", 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.update_board(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def update_board(self, row, col):
        if self.board[row * 3 + col] == " ":
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED)
            self.board[row * 3 + col] = self.current_player

            if self.check_winner(self.current_player):
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_board_full():
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == self.bot_player:
                    self.bot_move()

    def bot_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.bot_player
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        row, col = divmod(best_move, 3)
        self.buttons[row][col].config(text=self.bot_player, state=tk.DISABLED)
        self.board[best_move] = self.bot_player

        if self.check_winner(self.bot_player):
            messagebox.showinfo("Winner", f"Player {self.bot_player} wins!")
            self.reset_game()
        elif self.is_board_full():
            messagebox.showinfo("Draw", "It's a draw!")
            self.reset_game()
        else:
            self.current_player = "X"

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("X"):
            return -1
        elif self.check_winner("O"):
            return 1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self):
        return all(cell != " " for cell in self.board)

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state=tk.NORMAL)
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        if self.bot_player == "X":
            self.bot_move()


def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
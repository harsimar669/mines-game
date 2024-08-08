import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, rows=10, cols=10, num_mines=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.mines = set()
        self.flags = set()
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.root, width=3, height=2, command=lambda r=row, c=col: self.reveal(r, c))
                button.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))
                button.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = button

    def place_mines(self):
        while len(self.mines) < self.num_mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) not in self.mines:
                self.mines.add((r, c))

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mines:
                    count += 1
        return count

    def reveal(self, row, col):
        if (row, col) in self.flags or self.buttons[row][col]['state'] == 'disabled':
            return
        if (row, col) in self.mines:
            self.show_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            return

        self.buttons[row][col]['state'] = 'disabled'
        mine_count = self.count_adjacent_mines(row, col)
        if mine_count > 0:
            self.buttons[row][col]['text'] = str(mine_count)
        else:
            self.buttons[row][col]['text'] = ''
            for r in range(max(0, row - 1), min(self.rows, row + 2)):
                for c in range(max(0, col - 1), min(self.cols, col + 2)):
                    if (r, c) != (row, col):
                        self.reveal(r, c)
        if self.check_win():
            messagebox.showinfo("Congratulations", "You won!")

    def toggle_flag(self, row, col):
        if self.buttons[row][col]['state'] == 'disabled':
            return
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            self.buttons[row][col]['text'] = ''
        else:
            self.flags.add((row, col))
            self.buttons[row][col]['text'] = 'F'

    def show_mines(self):
        for r, c in self.mines:
            self.buttons[r][c]['text'] = '*'
            self.buttons[r][c]['bg'] = 'red'
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col]['state'] = 'disabled'

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.mines and self.buttons[row][col]['state'] != 'disabled':
                    return False
        return True

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()


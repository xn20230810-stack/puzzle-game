import tkinter as tk
from tkinter import messagebox
import random

class PuzzleGame:
    def __init__(self, master, size=3):
        self.master = master
        self.master.title("拼圖小遊戲")
        self.size = size
        self.tiles = []
        self.buttons = []
        self.empty_tile = (self.size - 1, self.size - 1)
        self.colors = ["#EEE4DA", "#EDE0C8", "#F2B179", "#F59563",
                       "#F67C5F", "#F65E3B", "#EDCF72", "#EDCC61",
                       "#F9F6F2", "#E0B9A4", "#D2B48C", "#BDB76B"]
        self.create_tiles()
        self.create_ui()
        self.shuffle_tiles()

    def create_tiles(self):
        self.tiles = [[self.size * r + c + 1 for c in range(self.size)] for r in range(self.size)]
        self.tiles[self.size-1][self.size-1] = None

    def create_ui(self):
        for r in range(self.size):
            row = []
            for c in range(self.size):
                btn = tk.Button(self.master, font=("Arial", 24), width=4, height=2,
                                command=lambda row=r, col=c: self.move_tile(row, col))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)
        self.update_ui()

    def update_ui(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.tiles[r][c]
                if val is None:
                    self.buttons[r][c]["text"] = ""
                    self.buttons[r][c]["bg"] = "black"
                else:
                    self.buttons[r][c]["text"] = str(val)
                    color_index = (val - 1) % len(self.colors)
                    self.buttons[r][c]["bg"] = self.colors[color_index]
                    self.buttons[r][c]["fg"] = "white"

    def move_tile(self, r, c):
        er, ec = self.empty_tile
        if abs(er - r) + abs(ec - c) == 1:
            self.tiles[er][ec], self.tiles[r][c] = self.tiles[r][c], self.tiles[er][ec]
            self.empty_tile = (r, c)
            self.update_ui()
            if self.check_win():
                self.master.after(100, self.handle_win)

    def handle_win(self):
        messagebox.showinfo("恭喜", "你完成拼圖了！")
        if messagebox.askyesno("下一關", f"要挑戰 {self.size + 1}x{self.size + 1} 的拼圖嗎？"):
            self.master.destroy()
            root = tk.Tk()
            game = PuzzleGame(root, size=self.size + 1)
            root.mainloop()
        else:
            self.master.destroy()

    def shuffle_tiles(self):
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        for _ in range(self.size * self.size * 10):
            er, ec = self.empty_tile
            possible = []
            for dr, dc in moves:
                nr, nc = er+dr, ec+dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    possible.append((nr, nc))
            if possible:
                nr, nc = random.choice(possible)
                self.tiles[er][ec], self.tiles[nr][nc] = self.tiles[nr][nc], self.tiles[er][ec]
                self.empty_tile = (nr, nc)
        self.update_ui()

    def check_win(self):
        num = 1
        for r in range(self.size):
            for c in range(self.size):
                if r == self.size-1 and c == self.size-1:
                    return self.tiles[r][c] is None
                if self.tiles[r][c] != num:
                    return False
                num += 1
        return True

if _name_ == "_main_":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
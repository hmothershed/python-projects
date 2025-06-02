import os
import time
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

class MemoryMatchGame:
    def __init__(self, master, image_folder):
        self.master = master
        self.master.title("Memory Match Game")
        
        self.image_folder = Path(image_folder)
        self.image_size = (100, 100)

        self.load_images()
        self.create_board()
        self.create_controls()
        self.start_time = None
        self.timer_running = False
        self.first_click = None
        self.lock = False
        self.moves = 0

    def load_images(self):
        # load all images from the folder except the back image
        image_paths = [p for p in self.image_folder.glob("*") if p.suffix.lower() in [".png", ".jpg", ".jpeg"] and p.name != "back.png"]
        if len(image_paths) < 2:
            raise ValueError("Need at least two images to play the game.")
        if len(image_paths) % 2 != 0:
            image_paths = image_paths[:-1]  # Ensure even number of images

        # duplicate images and shuffle
        self.pairs = []
        for path in image_paths:
            img = Image.open(path).resize(self.image_size)
            img_tk = ImageTk.PhotoImage(img)
            self.pairs.append(img_tk)
            self.pairs.append(img_tk)  # Duplicate for matching
        random.shuffle(self.pairs)

        # load the back image
        back_path = self.image_folder / "back.png"
        if not back_path.exists():
            raise FileNotFoundError("You need a 'back.png' image in the image folder.")
        self.card_back = ImageTk.PhotoImage(Image.open(back_path).resize(self.image_size))


    def create_controls(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)
        self.start_button = tk.Button(self.top_frame, text="Start", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5)
        self.reset_button = tk.Button(self.top_frame, text="Reset", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=1, padx=5)
        self.move_label = tk.Label(self.top_frame, text="Moves: 0")
        self.move_label.grid(row=0, column=2, padx=5)
        self.timer_label = tk.Label(self.top_frame, text="Time: 0 seconds")
        self.timer_label.grid(row=0, column=3, padx=5)

    def create_board(self):
        self.buttons = []
        self.matched = set()
        self.currently_flipped = {}
        
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(padx=10, pady=10)

        # force even layout: 6x4 grid for 24 cards
        self.rows, self.cols = 4, 6

        for idx in range(len(self.pairs)):
            row, col = divmod(idx, self.cols)
            btn = tk.Button(self.board_frame, image=self.card_back, command=lambda i=idx: self.on_click(i))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
    
    def start_game(self):
        random.shuffle(self.pairs)
        self.matched.clear()
        self.currently_flipped.clear()
        self.moves = 0
        self.update_move_label()
        self.first_click = None
        self.lock = False

        for i, btn in enumerate(self.buttons):
            btn.config(image=self.card_back, state=tk.NORMAL)

        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

    def reset_game(self):
        self.start_game()
    
    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.moves}")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed} seconds")
            self.master.after(1000, self.update_timer)
    
    def on_click(self, index):
        if self.lock or index in self.matched or index in self.currently_flipped:
            return
        
        # show the image
        self.buttons[index].config(image=self.pairs[index])
        self.currently_flipped[index] = self.pairs[index]

        if len(self.currently_flipped) == 2:
            self.lock = True
            self.moves += 1
            self.update_move_label()
            self.master.after(1000, self.check_match)

    def check_match(self):
        indices = list(self.currently_flipped.keys())
        if self.pairs[indices[0]] == self.pairs[indices[1]]:
            self.matched.update(indices)
        else:
            for i in indices:
                self.buttons[i].config(image=self.card_back)
        
        self.currently_flipped.clear()
        self.lock = False

        if len(self.matched) == len(self.pairs):
            self.timer_running = False
            elapsed = int(time.time() - self.start_time)
            messagebox.showinfo("You win!", f"You've matched all pairs in {self.moves} moves and {elapsed} seconds!")
            self.start_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)

# run the game
if __name__ == "__main__":
    IMAGE_DIR = "images"
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Put at least two image files (plus back.png) into the folder: {IMAGE_DIR}")

    root = tk.Tk()
    try:
        game = MemoryMatchGame(root, IMAGE_DIR)
        root.mainloop()
    except Exception as e:
        print(f"Error:", e)
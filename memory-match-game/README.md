# 🧠 Memory Match Game
A desktop memory matching game built with Python's `tkinter` GUI toolkit and the `Pillow` library. Flip over pairs of cards to find matching images. Tracks your moves and time as you try to beat your own best performance!

## Features
- Use your own hand-drawn or custom images for the game.
- Card flip animations with a matching system.
- 6x4 game board of 12 image pairs (24 cards).
- **Start** and **Reset** buttons for flexible gameplay.
- Tracks the number of **moves**.
- Displays an in-game **timer**.
- End-of-game summary with performance stats.

## Image Requirements
Before playing, ensure you have the correct image setup:
1. Create a folder named `images` in the project root
2. Add at least **two** image files (`.png`, `.jpg`, or `.jpeg`)
   - For best results, use an **even number** of images
   - Each image will apppear **twice** in the game for pairing
4. Add a `back.png` file, which will be shown as the back of all cards

> 💡 All images will be resized ot 100x100 pixels. You can customize the size fo card images by modifying the line:
> ```python
> self.image_size = (100, 100)
> ```

## How To Run
### 1. Install Dependencies
```bash
pip install pillow
```
### 2. Run the Game
```bash
python main.py
```

## Gameplay Instructions
1. Click **Start** to begin the game.
2. Click two cards to flip them and try to find a match
3. Continue flipping until all pairs are matched
4. Your total moves and time will be displayed
5. Click **Reset** to reshuffle and try again

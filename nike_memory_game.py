import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random
import os

root = tk.Tk()
root.title("Nike Memory Game")
root.configure(bg="#f3eaff")
root.resizable(False, False)

ROWS, COLS = 5, 6
TIMER_SECONDS = 60
tile_size = 90
padding = 8
game_frame_width = (tile_size + padding) * COLS
game_frame_height = (tile_size + padding) * ROWS

top_frame = tk.Frame(root, bg="#f3eaff")
top_frame.pack(fill="x", padx=20, pady=(10, 0))

title_label = tk.Label(top_frame, text="Nike Memory Game", font=("Arial", 22, "bold"), bg="#f3eaff", fg="#4b007d")
title_label.pack(side="left")

time_left_label = tk.Label(top_frame, text=f"Time Left: {TIMER_SECONDS}s", font=("Arial", 16, "bold"), bg="#f3eaff", fg="#4b007d")
time_left_label.pack(side="right")

game_frame = tk.Frame(root, bg="#f3eaff", width=game_frame_width, height=game_frame_height)
game_frame.pack(padx=20, pady=20)

image_folder = os.getcwd()
image_files = [
    "air_force_1.png", "air_huarache.png", "air_max.png", "air_zoom_terra.png", "dunk_low.png",
    "go_flyease.png", "infinityrn_4.png", "jordan_1.png", "lebron_20.png", "metcon_9.png",
    "nike_waffle.png", "pegasus_40.png", "react_infinity.png", "space_hippie.png", "structure_25.png",
    "superrep_go.png", "zoomx_vaporfly.png"
]

remove_models = ["blazer_mid.png"]
image_files = [img for img in image_files if img not in remove_models]
image_files = random.sample(image_files, 15)
image_files *= 2
random.shuffle(image_files)

def resize_image(img_path, size):
    img = Image.open(img_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

images = [resize_image(os.path.join(image_folder, f), (tile_size, tile_size)) for f in image_files]
flipped_tiles = []
matched_indices = []
buttons = []
score = 0
time_left = TIMER_SECONDS

def on_tile_click(index):
    global flipped_tiles, score
    if index in matched_indices or index in flipped_tiles or len(flipped_tiles) == 2:
        return
    buttons[index].config(image=images[index])
    flipped_tiles.append(index)
    if len(flipped_tiles) == 2:
        root.after(500, check_match)

def check_match():
    global flipped_tiles, matched_indices, score
    i1, i2 = flipped_tiles
    if image_files[i1] == image_files[i2]:
        matched_indices.extend(flipped_tiles)
        for idx in flipped_tiles:
            buttons[idx].config(image=white_tile, bg="white")
        score += 10
    else:
        for idx in flipped_tiles:
            buttons[idx].config(image=blank_tile, bg="#d3c2ff")
    flipped_tiles = []
    if len(matched_indices) == len(image_files):
        show_result_screen()

def show_result_screen():
    result_window = tk.Toplevel(root)
    result_window.title("Game Over - Results")
    result_window.geometry("1000x700")
    result_window.resizable(False, False)

    # Gradient background
    canvas = tk.Canvas(result_window, width=1000, height=700)
    canvas.pack(fill="both", expand=True)

    gradient = Image.new("RGB", (1000, 700), "#f3eaff")
    draw = ImageDraw.Draw(gradient)
    for y in range(700):
        color = int(255 - (y / 700) * 50)
        draw.line([(0, y), (1000, y)], fill=(color, color, 255))
    bg_image = ImageTk.PhotoImage(gradient)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    canvas.create_text(500, 40, text="🎉 Game Over 🎉", font=("Arial", 30, "bold"), fill="#4b007d")
    canvas.create_text(500, 90, text=f"Your Score: {score}", font=("Arial", 20), fill="#4b007d")

    matched_pairs = matched_indices[::2]
    image_refs = []  # Store references so images don't vanish

    x_start, y_start = 100, 130
    img_size = 100
    col_count = 4

    for idx, match_idx in enumerate(matched_pairs):
        img_path = os.path.join(image_folder, image_files[match_idx])
        shoe_img = Image.open(img_path).resize((img_size, img_size), Image.Resampling.LANCZOS)
        shoe_img_tk = ImageTk.PhotoImage(shoe_img)
        x_pos = x_start + (idx % col_count) * 220
        y_pos = y_start + (idx // col_count) * 170
        canvas.create_image(x_pos, y_pos, anchor="nw", image=shoe_img_tk)
        image_refs.append(shoe_img_tk)
        shoe_name = image_files[match_idx].replace(".png", "").replace("_", " ").title()
        canvas.create_text(x_pos + img_size // 2, y_pos + img_size + 20, text=shoe_name, font=("Arial", 13), fill="#4b007d")

    play_btn = tk.Button(result_window, text="Play Again", font=("Arial", 14, "bold"), bg="#d3c2ff",
                         command=lambda: restart_game(result_window))
    exit_btn = tk.Button(result_window, text="Exit", font=("Arial", 14, "bold"), bg="#d3c2ff",
                         command=root.quit)

    canvas.create_window(400, 640, window=play_btn)
    canvas.create_window(600, 640, window=exit_btn)

    result_window.mainloop()

def restart_game(win):
    win.destroy()
    root.destroy()
    os.system("python nike_memory_game.py")

def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        time_left_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, countdown)
    else:
        messagebox.showinfo("Time's Up!", "Game Over!")
        show_result_screen()

blank_tile_img = Image.new("RGBA", (tile_size, tile_size), (211, 194, 255, 255))
blank_tile = ImageTk.PhotoImage(blank_tile_img)

white_tile_img = Image.new("RGBA", (tile_size, tile_size), (255, 255, 255, 255))
white_tile = ImageTk.PhotoImage(white_tile_img)

for i in range(ROWS * COLS):
    btn = tk.Button(game_frame, image=blank_tile, bg="#d3c2ff", command=lambda i=i: on_tile_click(i))
    btn.grid(row=i // COLS, column=i % COLS, padx=padding // 2, pady=padding // 2)
    buttons.append(btn)

countdown()
root.mainloop()

import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import simpledialog, messagebox

# Initialize the main window
window = tk.Tk()
window.title("Map Coordinates")
window.geometry("700x600")

# Load and resize the image
original_image = Image.open("STATE_IDENTIFIER/Map.png").resize((700, 600))
photo_image = ImageTk.PhotoImage(original_image)

# Load state names and coordinates
state_file = pd.read_csv("STATE_IDENTIFIER/state_name.csv")
all_state = state_file['state'].tolist()
state_coords = {row['state']: (row['x'], row['y']) for _, row in state_file.iterrows()}

# Create Canvas widget
canvas = tk.Canvas(window, width=700, height=600)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

# Initialize variables
guessed_state = []
marked_image = original_image.copy()
draw = ImageDraw.Draw(marked_image)

# Load default PIL font
font = ImageFont.load_default()

# Label for showing the status
status_label = tk.Label(window, text="", font=("Helvetica", 14))
status_label.pack(pady=10)

def update_status():
    """Update the status label with the number of states identified and remaining."""
    num_identified = len(guessed_state)
    num_remaining = len(all_state) - num_identified
    status_label.config(text=f"States Identified: {num_identified} | States Remaining: {num_remaining}")

# Main loop
while len(guessed_state) < 29:
    update_status()  # Update status before each user input
    answer_state = simpledialog.askstring("Guess the State", "Enter the name of the state:")
    if answer_state is None:
        continue

    answer_state = answer_state.title()

    if answer_state == "Exit":
        missing_states = [state for state in all_state if state not in guessed_state]
        pd.DataFrame(missing_states, columns=["State"]).to_csv("state_to_learn.csv", index=False)
        window.destroy()
        break

    if answer_state in all_state:
        if answer_state not in guessed_state:
            guessed_state.append(answer_state)
            if answer_state in state_coords:
                x, y = state_coords[answer_state]
                draw.ellipse((x-5, y-5, x+5, y+5), fill='black', outline='black')
                # Use default font
                draw.text((x+10, y-5), answer_state, fill='black', font=font)
                updated_photo_image = ImageTk.PhotoImage(marked_image)
                canvas.create_image(0, 0, anchor=tk.NW, image=updated_photo_image)
                canvas.image = updated_photo_image
        else:
            messagebox.showinfo("Already Guessed", "You've already guessed this state.")
    else:
        messagebox.showwarning("Incorrect Guess", "The state name is incorrect. Please try again.")

window.mainloop()

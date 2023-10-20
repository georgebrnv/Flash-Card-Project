from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
data_dic = {}

# CSV file read
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    data_dic = original_data.to_dict(orient="records")
else:
    data_dic = data.to_dict(orient="records")



def is_known():
    data_dic.remove(current_card)
    next_card()
    words_data = pandas.DataFrame(data_dic)
    words_data.to_csv("data/words_to_learn.csv", index=False)


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_image, image=card_front_png)
    canvas.itemconfig(language_text, text="French", fill="black")
    current_card = random.choice(data_dic)
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back_png)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# Windows setup
window = Tk()
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
window.title("Flash Cards")

# Canvas and card's images
canvas = Canvas(width=810, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_png = PhotoImage(file="./images/card_front.png")
card_back_png = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(405, 265, image=card_front_png)
canvas.grid(row=0, column=0, columnspan=2)
# Canvas text
language_text = canvas.create_text(405, 150, text="Flash Card", font=("Arial", 40, "italic"))
word_text = canvas.create_text(405, 265, text="Press green button!", font=("Arial", 60, "bold"))

# Buttons
right_button_png = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_png, bg=BACKGROUND_COLOR,
                      highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)
wrong_button_png = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_png, bg=BACKGROUND_COLOR,
                      highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

flip_timer = window.after(3000, flip_card)
window.after_cancel(flip_timer)

next_card()

window.mainloop()

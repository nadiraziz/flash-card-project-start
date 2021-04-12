import pandas
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"


current_card = {}
to_learn = {}

try:
    data = pandas.read_csv('data/word_to_learn.csv')
except FileNotFoundError:
    orginal_data = pandas.read_csv('data/french_words.csv')
    to_learn = orginal_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_word():
    global current_card, flip_timer
    flip_timer = window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text='French', fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text='english', fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")
    canvas.itemconfig(card_background, image=back_image)


def is_known():
    to_learn.remove(current_card)
    learn_data = pandas.DataFrame(to_learn)
    learn_data.to_csv('data/word_to_learn.csv', index=False)
    next_word()


# UI SETUP
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file='images/card_front.png')
back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, text='', font=('Arial', 60, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Arial', 40, 'italic'))
canvas.grid(column=0, row=0, columnspan=2)

flip_timer = window.after(3000, func=flip_card)
# buttons
right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

# buttons
wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_word)
wrong_button.grid(column=1, row=1)
next_word()

window.mainloop()

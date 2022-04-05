from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "cyan"
carta_actual = {}
por_aprender = {}

try:
    data = pandas.read_csv("datos/palabras_por_aprender.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("datos/data_es_en.csv")
    por_aprender = original_data.to_dict(orient="records")
else:
    por_aprender = data.to_dict(orient="records")



def next_card():
    global carta_actual, tiempo_de_giro
    ventana.after_cancel(tiempo_de_giro)
    carta_actual = random.choice(por_aprender)
    canvas.itemconfig(carta_titulo, text="Inglés", fill="black")
    canvas.itemconfig(carta_palabra, text=carta_actual["Inglés"], fill="black")
    canvas.itemconfig(carta, image=flashcard_img_front)
    tiempo_de_giro = ventana.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(carta_titulo, text="Español", fill="white")
    canvas.itemconfig(carta_palabra, text=carta_actual["Espanol"], fill="white")
    canvas.itemconfig(carta, image=flashcard_img_back)


def conocida():
    por_aprender.remove(carta_actual)
    data = pandas.DataFrame(por_aprender)
    data.to_csv("datos/palabras_por_aprender.csv", index=False)
    next_card()


ventana = Tk()
ventana.title("Flash cards")
ventana.config(pady=20, padx=20, bg=BACKGROUND_COLOR)

tiempo_de_giro = ventana.after(3000, func=flip_card)

canvas = Canvas(width=568, height=514, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_img_front = PhotoImage(file="images/flashcards_front.png")
flashcard_img_back = PhotoImage(file="images/flashcards_back.png")
carta = canvas.create_image(284, 257, image=flashcard_img_front)
carta_titulo = canvas.create_text(284, 130, text="", font=("Ariel", 35, "italic"))
carta_palabra = canvas.create_text(284, 285, text="", font=("Ariel", 45, "bold"))
canvas.grid(column=0, row=0, columnspan=4, rowspan=4)

wrong_img = PhotoImage(file="images/wrong.png")
boton_desconocido = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
boton_desconocido.grid(column=1, row=4)

right_img = PhotoImage(file="images/right.png")
boton_conocido = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=conocida)
boton_conocido.grid(column=2, row=4)

ventana.mainloop()

import pickle
import tkinter as tk
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
from tkinter import ttk

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Erstelle das Hauptfenster
root = tk.Tk()

# Verhindere das Resizen des Hauptfensters
root.resizable(False, False)

# Erstelle ein Frame im Hauptfenster
my_frame = tk.Frame(root)
my_frame.pack()

# Teile das Frame in drei Bereiche auf
left_frame = tk.Frame(my_frame)
left_frame.pack(side=tk.LEFT)

middle_frame = tk.Frame(my_frame)
middle_frame.pack(side=tk.LEFT)

right_frame = tk.Frame(my_frame)
right_frame.pack(side=tk.LEFT)

def claer_text_function():
    global wordCreation
    wordCreation="Ausgabe: "


#Füge Buttons in den neuen Button Frame hinzu
my_button1 = tk.Button(left_frame, text="Take Image", font=("Helvetica", 14), bg="#ff0000", fg="#ffffff",width=15, height=4)
my_button1.pack(padx=1, pady=1)

my_button2 = tk.Button(left_frame, text="Clear Image", font=("Helvetica", 14), bg="#ff0000", fg="#ffffff",width=15, height=4)
my_button2.pack(padx=1, pady=1)

my_button3 = tk.Button(left_frame, text="Quit", font=("Helvetica", 14), bg="#ff0000", fg="#ffffff", command=root.destroy,width=15, height=4)
my_button3.pack(padx=1, pady=1)

my_button4 = tk.Button(left_frame, text="Clear Text", font=("Helvetica", 14),bg="#ff0000", fg="#ffffff",width=15, height=4)
my_button4.pack(padx=1, pady=1)


# Erstelle ein OpenCV VideoCapture-Objekt
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'A', 1: 'B', 2: 'C',6:' '}

# wort Bildung
word_creation="Ausgabe: "

# Erstelle ein Label-Widget für den Livestream
my_video_stream = tk.Label(middle_frame)
my_video_stream.pack()

# Erstelle ein Label-Widget für die Bildausgabe
my_image_output = tk.Label(right_frame)
my_image_output.pack()

# Funktion zum Aktualisieren des Livestream-Labels
def update_video_stream():

    _, frame = cap.read()
    H, W, _ = frame.shape
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

    # Konvertiert das empfangene Video-Frame in ein PIL-Bild
    img = Image.fromarray(frame)

    # Konvertiert das PIL-Bild in ein tkinter-Image
    imgtk = ImageTk.PhotoImage(image=img)
    # Setzt das Attribut des tkinter-Image des Video-Streams auf das aktualisierte Bild
    my_video_stream.imgtk = imgtk
    # Konfiguriert das tkinter-Image des Video-Streams mit dem aktualisierten Bild
    my_video_stream.configure(image=imgtk)
    # Plant die Funktion "update_video_stream" erneut in 8ms
    my_video_stream.after(8, update_video_stream)


# Funktion zum Aufnehmen eines Screenshots und Anzeigen des Texts
def take_screenshot():
    data_aux = []
    x_ = []
    y_ = []
    global word_creation

    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))


        prediction = model.predict([np.asarray(data_aux)])

        predicted_character = labels_dict[int(prediction[0])]
        word_creation +=str(predicted_character)

        #schreiben
        cv2.putText(frame, word_creation, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame,"Current Letter: "+ predicted_character, (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (25, 223,23), 2)


    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    my_image_output.imgtk = imgtk
    my_image_output.configure(image=imgtk)





# Verknüpfe die Funktionen mit den Buttons
my_button1.configure(command=take_screenshot)
my_button2.configure(command=lambda: my_image_output.configure(image=""))
my_button4.configure(command=claer_text_function)

#Aktualisieren des Livestreams
update_video_stream()

#Starte das Hauptfenster
root.mainloop()

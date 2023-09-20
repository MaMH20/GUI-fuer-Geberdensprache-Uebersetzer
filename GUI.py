import pickle
import threading
import tkinter as tk
import cv2
import imutils
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
import sklearn

# Laden der trainierten Modelle für linke und rechte Hand
model_dict_left = pickle.load(open('./model_left.p', 'rb'))
model_left = model_dict_left['model']

model_dict_right = pickle.load(open('./model_right.p', 'rb'))
model_right = model_dict_right['model']

# Initialisierung globaler Variablen
predicted_text = ""
last_stable_time = 0
counter = 0
previous_predicted_character = ""

# Initialisierung von Mediapipe für die Handerkennung
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

# Funktion zur Bestimmung der Handorientierung (Links, Rechts, Oben, Unten)
def hand_orientation(landmark_0, landmark_9):
    x0, y0 = landmark_0.x, landmark_0.y
    x9, y9 = landmark_9.x, landmark_9.y

    if abs(x9 - x0) < 0.05:  # da tan(0) --> ∞
        m = 1000000000
    else:
        m = abs((y9 - y0) / (x9 - x0))

    if m >= 0 and m <= 1:
        if x9 > x0:
            return "Right"
        else:
            return "Left"
    if m > 1:
        if y9 < y0:
            return "Up"
        else:
            return "Down"

# Funktion zur Berechnung des Rotationswinkels
def angle_of_rotation(hand_orientation,angle_0_13):
    if hand_orientation == "Up":
        if hand_landmarks.landmark[9].x > hand_landmarks.landmark[0].x:
            angle = abs(angle_0_13) - 90
            return angle
        else:
            angle = 90 - abs(angle_0_13)
            return angle

    elif hand_orientation == "Down":
        if hand_landmarks.landmark[9].x > hand_landmarks.landmark[0].x:
            angle = 270 - abs(angle_0_13)
            return angle
        else:
            angle = 90 + abs(angle_0_13)
            return angle

    elif hand_orientation == "Right":
        if hand_landmarks.landmark[0].y > hand_landmarks.landmark[9].y:
            angle = abs(angle_0_13) + 270
            return angle
        else:
            angle = 270 - abs(angle_0_13)
            return angle

    elif hand_orientation == "Left":
        if hand_landmarks.landmark[0].y > hand_landmarks.landmark[9].y:
            angle = 90 - abs(angle_0_13)
            return angle
        else:
            angle = abs(angle_0_13) + 90
            return angle
    else:
        print("Default case")

# Funktion zur Berechnung des Winkels zwischen Ringfinger und Kleiner Finger
def angle():
    kleiner_finger_punkt = hand_landmarks.landmark[0]
    ringfinger_punkt = hand_landmarks.landmark[13]
    angle = np.arctan((ringfinger_punkt.y - kleiner_finger_punkt.y) /
                      (ringfinger_punkt.x - kleiner_finger_punkt.x)) * 180 / np.pi
    return angle


def update_textbox():
    global predicted_text
    gui.text_view.delete(1.0, tk.END)

    if len(predicted_text) >= 2:
        last_two_characters = predicted_text[-2:]

        # Überprüfen, ob die letzten 2 Zeichen '  ' sind
        if last_two_characters == "  ":
            predicted_text = predicted_text[:-2] + " "

        gui.text_view.insert(tk.END, predicted_text)
    else:

        gui.text_view.insert(tk.END, predicted_text)

####standard Auflösung 1920*1080
# Klasse für die Benutzeroberfläche (GUI)
class GUI:

    def display_about_window(self):
        if hasattr(self, 'about_window') and self.about_window.winfo_exists():
            # Wenn das Fenster bereits existiert und sichtbar ist, nichts weiter tun.
            return

        # Wenn das Fenster noch nicht geöffnet ist, öffne es.
        self.about_window = tk.Toplevel(self.root)
        self.about_window.title("Über")
        self.about_window.geometry("800x600")

        # Laden und Anzeigen des About-Bildes im neuen Fenster
        self.about_image = Image.open("about_image.png")
        about_image_tk = ImageTk.PhotoImage(self.about_image)
        about_label = tk.Label(self.about_window, image=about_image_tk)
        about_label.image = about_image_tk  # Behalte eine Referenz zum Bild
        about_label.pack()

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Gebärdensprache App")

        self.root.resizable(True, True)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size to fill the screen
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Setze die Hintergrundfarbe des Hauptfensters fest
        self.root.configure(background="#001C30")

        self.root.protocol("WM_DELETE_WINDOW", self.stop_stream_and_quit)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Erstelle  "About" button
        self.about_button = tk.Button(self.root, text="Über", font=("Helvetica", 14), bg="#8EAC50", fg="#ffffff",
                                      command=self.display_about_window)
        self.about_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        self.my_frame = tk.Frame(self.root, background="#1D5B79")
        self.my_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.my_frame.columnconfigure(0, weight=1)
        self.my_frame.columnconfigure(1, weight=1)
        self.my_frame.rowconfigure(0, weight=1)
        self.my_frame.rowconfigure(1, weight=1)

        self.image_frame = tk.Frame(self.my_frame, background="#1D5B79")
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        self.video_frame = tk.Frame(self.my_frame,  background="#1D5B79")
        self.video_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NE)

        self.text_frame = tk.Frame(self.my_frame)
        self.text_frame.grid(row=1, column=0,  padx=10, pady=10, sticky=tk.SW)

        self.button_frame = tk.Frame(self.my_frame, background="#1D5B79")
        self.button_frame.grid(row=1, column=1, padx=200, pady=20, sticky=tk.SE)

        # Hintergrundbild laden
        self.bg_image_left = ImageTk.PhotoImage(Image.open("alphabet.png"))

        # Display the background images on the canvases
        self.my_image_output = tk.Canvas(self.image_frame, width=900, height=600)#####
        self.my_image_output.grid(row=0, column=0)
        self.my_image_output.create_image(0, 0, image=self.bg_image_left, anchor=tk.NW)

        self.cap = cv2.VideoCapture(0)
        self.my_video_stream = tk.Canvas(self.video_frame, width=900, height=600)##
        self.my_video_stream.grid(row=0, column=1)

        self.text_view = tk.Text(self.text_frame, font=("Helvetica", 49), width=25, height=4, bg="#27374D", fg="#ffffff")###
        self.text_view.grid(row=1, column=0, sticky=tk.SW)

        self.button_frame = tk.Frame(self.my_frame, background="#1D5B79")
        self.button_frame.grid(row=1, column=1, padx=200, pady=20, sticky=tk.SE)

        self.delete_text_button = tk.Button(self.button_frame, text="Text Löschen", font=("Helvetica", 15), bg="#FED049",
                                    fg="#000000",
                                    width=30, height=1, command=self.delete_text)
        self.delete_text_button.pack(pady=10)

        self.delete_the_last_character_button = tk.Button(self.button_frame, text="Letzte Zeichen Löschen", font=("Helvetica", 15),
                                    bg="#FED049",
                                    fg="#000000",
                                    width=30, height=1, command=self.delete_last_character)
        self.delete_the_last_character_button .pack(pady=10)

        self.quit_button = tk.Button(self.button_frame, text="Beenden", font=("Helvetica", 15), bg="#FED049",
                                    fg="#000000",
                                    width=30, height=1, command=self.stop_stream_and_quit)
        self.quit_button.pack(pady=10)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

        self.is_streaming = False
        self.thread = None
        self.toggle_stream()


    def stop_stream_and_quit(self):
        self.toggle_stream()
        # die verzögerung ist die Lösung, dass das Thread ausgemacht wird un keine
        # probleme auftauchen
        self.root.after(400, self.root.destroy)


    def toggle_stream(self):
        if self.is_streaming:
            self.is_streaming = False
        else:
            self.is_streaming = True
            self.thread = threading.Thread(target=self.update_video_stream)
            self.thread.start()

    def delete_text(self):
        global predicted_text
        predicted_text = " "
        self.text_view.delete(1.0, tk.END)

    def delete_last_character(self):
        global predicted_text
        predicted_text = predicted_text[:-1]
        update_textbox()

    def update_video_stream(self):
        while self.is_streaming:
            global predicted_text,previous_predicted_character,counter

            global hand_landmarks,left_hand,right_hand

            data_aux = []
            x_ = []
            y_ = []
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for i in results.multi_handedness:
                    label = str(i.classification[0].label)
                    if label == 'Left':
                        left_hand = True
                    if label == 'Right':
                        left_hand = False

            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                # Schleife, um jedes gefundene Handmerkmal durchzulaufen

                for hand_landmarks in results.multi_hand_landmarks:
                    pass

                # Berechnung des Drehwinkels (in Grad)
                orientation_of_hand = hand_orientation(hand_landmarks.landmark[0],
                                                       hand_landmarks.landmark[9])
                angle_0_13 = angle()
                angle_to_rotate = angle_of_rotation(orientation_of_hand, angle_0_13)

                # Rotiere das Bild um den berechneten Drehwinkel
                rotated_img = imutils.rotate_bound(frame_rgb, angle_to_rotate)

                # Verwenden des Handdetektionsmodells, um die Handmerkmale zu extrahieren
                results = hands.process(rotated_img)

                if results.multi_hand_landmarks:
                    # Schleife, um jedes gefundene Handmerkmal durchzulaufen
                    for hand_landmarks in results.multi_hand_landmarks:

                        for i in range(len(hand_landmarks.landmark)):
                            # Speichern der X- und Y-Koordinaten der aktuellen Handpunkt-Koordinate
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            # Speichern der X- und Y-Koordinaten in separaten Listen
                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            # Speichern der normalisierten X- und Y-Koordinaten in der Merkmalsliste
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x = (x - min(x_)) / (max(x_) - min(x_))
                            y = (y - min(y_)) / (max(y_) - min(y_))
                            data_aux.append(x)
                            data_aux.append(y)

                if len(data_aux) == 42:

                    if left_hand:
                        prediction = model_left.predict([np.asarray(data_aux)])
                        predicted_character = prediction[0]
                    else:
                        prediction = model_right.predict([np.asarray(data_aux)])
                        predicted_character = prediction[0]

                    if predicted_character == "Blank":
                        predicted_character = " "


                    cv2.putText(frame, predicted_character, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3,
                                cv2.LINE_AA)

                    if predicted_character == previous_predicted_character:
                        counter += 1
                        if counter >= 7:
                            # Aktualisiere die globale Variable mit dem vorhergesagten Buchstaben
                            predicted_text += predicted_character
                            # Rufe die Methode auf, um das Textfeld zu aktualisieren
                            update_textbox()
                            counter = 0
                    else:
                        previous_predicted_character = predicted_character
                        counter = 0

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Passe die Größe des Rahmens an die 800x600-Leinwand an und behalten Sie dabei das Seitenverhältnis bei
            img = img.resize((900, 600), Image.LANCZOS)

            # Berechne Sie den Zentrierungsversatz, um den Videorahmen innerhalb der Leinwand zu zentrieren
            offset_x = max((900 - img.width) // 2, 0)
            offset_y = max((600 - img.height) // 2, 0)

            imgtk = ImageTk.PhotoImage(image=img)
            self.my_video_stream.create_image(offset_x, offset_y, image=imgtk, anchor=tk.NW)
            self.my_video_stream.imgtk = imgtk
            self.root.update()

        self.cap.release()

    def run(self):
        self.root.mainloop()


gui = GUI()
gui.run()
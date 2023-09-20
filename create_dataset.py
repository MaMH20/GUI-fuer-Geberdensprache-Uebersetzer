import os
import pickle
import cv2
import mediapipe as mp
import numpy as np
import imutils

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


# Initialisieren der Mediapipe-Bibliothek
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialisieren des Handdetektionsmodells
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Pfad zum Verzeichnis mit den Trainingsdaten
DATA_DIR = './data'

# Liste zum Speichern der Handmerkmale und der jeweiligen Labels (Handzeichen)
data = []
labels = []

count = 0

# Schleife, um jedes Verzeichnis in DATA_DIR zu durchlaufen
for dir_ in os.listdir(DATA_DIR):
    # Schleife, um jedes Bild in einem Verzeichnis zu durchlaufen
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        # Liste zum Speichern der Merkmale einer Hand
        data_aux = []

        # Leere Listen zum Speichern der X- und Y-Koordinaten von Handpunkten
        x_ = []
        y_ = []

        # Lesen des Bilds
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))

        # Konvertieren des Bilds von BGR zu RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Verwenden des Handdetektionsmodells, um die Handmerkmale zu extrahieren
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            # Schleife, um jedes gefundene Handmerkmal durchzulaufen

            for hand_landmarks in results.multi_hand_landmarks:
                pass

            # Berechnung des Drehwinkels (in Grad)
            orientation_of_hand = hand_orientation(hand_landmarks.landmark[0],
                                           hand_landmarks.landmark[9])
            angle_0_13=angle()
            angle_to_rotate = angle_of_rotation(orientation_of_hand,angle_0_13)

            # Rotiere das Bild um den berechneten Drehwinkel
            rotated_img = imutils.rotate_bound(img_rgb, angle_to_rotate)

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

            # Hinzufügen der Handmerkmale und des Labels zur Gesamtliste
            if len(data_aux) == 42:
                data.append(data_aux)
                labels.append(dir_)
                print(data_aux)

# Speichern der Handmerkmale und Labels in einer Pickle-Datei
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

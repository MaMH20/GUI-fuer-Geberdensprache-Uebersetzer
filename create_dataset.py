import os
import pickle

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

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
                # Schleife, um jede Koordinate eines Handmerkmals durchzulaufen
                for i in range(len(hand_landmarks.landmark)):
                    # Speichern der X- und Y-Koordinaten der aktuellen Handpunkt-Koordinate
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    # Speichern der X- und Y-Koordinaten in separaten Listen
                    x_.append(x)
                    y_.append(y)

                # Schleife, um jede Koordinate eines Handmerkmals durchzulaufen
                for i in range(len(hand_landmarks.landmark)):
                    # Speichern der normalisierten X- und Y-Koordinaten in der Merkmalsliste
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            # Hinzufügen der Handmerkmale und des Labels zur Gesamtliste
            data.append(data_aux)
            labels.append(dir_)

# Speichern der Handmerkmale und Labels in einer Pickle-Datei
f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
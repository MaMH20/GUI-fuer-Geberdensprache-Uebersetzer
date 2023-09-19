#FreeCodeCamp

import cv2
import os
import string

# Erstellt die Verzeichnisstruktur
if not os.path.exists("data"):
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Erstelle Ordner von A bis Z
    for alphabet in alphabets:
        folder_path = os.path.join("data", alphabet)
        os.makedirs(folder_path)

directory = 'data/'

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # Spiegelt das Bild horizontal, um das Erscheinungsbild eines Spiegels zu simulieren
    frame = cv2.flip(frame, 1)

    # Buchstaben A bis Z
    letters = string.ascii_uppercase
    count = {}

    # Zähle die Anzahl der Bilder in jedem Verzeichnis
    for letter in letters:
        count[letter.lower()] = len(os.listdir(directory + letter))

    y_coordinate = 20
    for i, letter in enumerate(letters):
        # Zeilenwechsel alle 7 Buchstaben
        if i % 7 == 0 and i != 0:
            y_coordinate += 20
        x_coordinate = 10 + (i % 7) * 100
        if letter in ['F', 'M', 'T', 'G', 'N', 'U']:
            x_coordinate -= 30  # Verschiebe den Text um 30 Pixel nach links
        text = f"{letter} : {count.get(letter.lower(), 0)}"
        cv2.putText(frame, text, (x_coordinate, y_coordinate), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

    cv2.imshow("Frame", frame)

    interrupt = cv2.waitKey(10)
    valid_keys = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    for letter in valid_keys:
        if interrupt & 0xFF == ord(letter):
            # Speichere das Bild im entsprechenden Verzeichnis
            cv2.imwrite(directory + letter.upper() + '/' + str(count[letter]) + '.jpg', frame)

    if interrupt & 0xFF == 27:  # esc key
        break

cap.release()
cv2.destroyAllWindows()

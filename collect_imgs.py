import cv2
import numpy as np
import os

# Create the directory structure
if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/0")
    os.makedirs("data/1")
    os.makedirs("data/2")
    os.makedirs("data/3")
    os.makedirs("data/4")
    os.makedirs("data/5")
    os.makedirs("data/6")


directory = 'data/'

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)

    # Getting count of existing images
    count = {'a': len(os.listdir(directory + "0")),
             'b': len(os.listdir(directory + "1")),
             'c': len(os.listdir(directory + "2")),
            'd': len(os.listdir(directory + "3")),
             'e': len(os.listdir(directory + "4")),
             'f': len(os.listdir(directory + "5")),
             'space': len(os.listdir(directory + "6"))}

    # Printing the count in each set to the screen
    cv2.putText(frame, "MODE : ", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "A : " + str(count['a']), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "B : " + str(count['b']), (10, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "C : " + str(count['c']), (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "D : " + str(count['d']), (10, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "E : " + str(count['e']), (10, 200), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "F : " + str(count['f']), (10, 220), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    cv2.putText(frame, "space : " + str(count['space']), (10, 240), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

    cv2.imshow("Frame", frame)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:  # esc key
        break

    if interrupt & 0xFF == ord('a'):
        cv2.imwrite(directory + '0/' + str(count['a']) + '.jpg', frame)

    if interrupt & 0xFF == ord('b'):
        cv2.imwrite(directory + '1/' + str(count['b']) + '.jpg', frame)

    if interrupt & 0xFF == ord('c'):
        cv2.imwrite(directory + '2/' + str(count['c']) + '.jpg', frame)

    if interrupt & 0xFF == ord('d'):
        cv2.imwrite(directory + '3/' + str(count['d']) + '.jpg', frame)

    if interrupt & 0xFF == ord('e'):
        cv2.imwrite(directory + '4/' + str(count['e']) + '.jpg', frame)

    if interrupt & 0xFF == ord('f'):
        cv2.imwrite(directory + '5/' + str(count['f']) + '.jpg', frame)
    if interrupt & 0xFF == ord('-'):
        cv2.imwrite(directory + '6/' + str(count['space']) + '.jpg', frame)


cap.release()
cv2.destroyAllWindows()
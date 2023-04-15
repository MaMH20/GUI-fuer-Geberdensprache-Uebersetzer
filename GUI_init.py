import tkinter as tk
import cv2
import datetime
import os

# Set up the window
root = tk.Tk()
root.title("Webcam Photo Capture")

# Set up the video capture
cap = cv2.VideoCapture(0)

# Set up the image label
img_label = tk.Label(root)
img_label.pack()

# Set up the timestamp label
time_label = tk.Label(root, text="Time: ")
time_label.pack()

# Set up the save button
counter = 0  # Initialize the counter variable
def save_image():
    global counter  # Use the global counter variable
    counter += 1  # Increment the counter
    # Get the current time
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Capture the image from the webcam
    ret, frame = cap.read()

    # Show the image on the label
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = tk.PhotoImage(data=cv2.imencode(".png", frame)[1].tobytes())
    img_label.configure(image=img)
    img_label.image = img

    # Update the timestamp label
    time_label.configure(text=f"Time: {timestamp}")


    # Save the image to a file
    folder = os.path.expanduser("~/Pictures")  # Change the folder name here
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"photo_{timestamp}.png")
    cv2.imwrite(filename, frame)

save_button = tk.Button(root, text="Save Photo", command=save_image)
save_button.pack()

# Start the window
root.mainloop()

# Release the video capture
cap.release()

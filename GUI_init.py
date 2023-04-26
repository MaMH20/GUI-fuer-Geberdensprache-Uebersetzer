import canvas as canvas
import cap as cap

import cv2
import datetime
import os
import tkinter as tk
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
from repoman import window


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg="DarkGoldenrod")

        # Create a toolbar
        self.toolbar = ttk.Frame(self.window, padding=5)
        self.toolbar.pack(side="top", fill="x")


        # Add a "Take Picture" button to the toolbar
        self.take_picture_button = ttk.Button(self.toolbar, text="Take Picture", command=self.take_picture)
        self.take_picture_button.pack(side="left")

        # Add a "Quit" button to the toolbar
        self.quit_button = ttk.Button(self.toolbar, text="Quit", command=self.window.quit)
        self.quit_button.pack(side="left")

        self.help_menu_var = tk.StringVar()
        self.help_menu_var.set("Help")

        self.help_menu = tk.OptionMenu(self.toolbar, self.help_menu_var, "Take Picture (S)", "Quit (Q)")
        self.help_menu.pack(side="left")

        # # Add a text box to the left side of the screen
        # self.text_box = tk.Text(self.window)
        # self.text_box.pack(side="right")

        # Add a button to add a space in the text box
        # self.space_button = ttk.Button(self.toolbar, text="Add Space", command=self.add_space)
        # self.space_button.pack(side="right")

        self.space_button = tk.Button(self.window, height=10, width=30, bg="LightSeaGreen", text="Add Space", command=self.add_space)
        # self.text_box.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        #self.space_button.pack(side="right", padx=10, pady=10)
        self.space_button.place(x=1700, y=500, width=200, height=30)


        # Add a text box to the left side of the screen
        self.text_box = tk.Text(self.window, height=10, width=30, bg="LightBlue")
        #self.text_box.pack(side="right", padx=10, pady=10, fill="both", expand=True)
       # self.text_box.pack(side="right", padx=10, pady=10)
        self.text_box.place(x=1700, y=550, width=500, height=200)





        # Create a label to display the video feed
        self.video_label = ttk.Label(self.window)
        self.video_label.pack()

        # Open the video capture device
        self.cap = cv2.VideoCapture(0)

        # Start the video feed
        self.update()

        # Bind the "S" key to take a picture and save it
        self.window.bind("s", self.take_picture)
        self.window.bind("q", self.window.quit)
        self.window.mainloop()

    def add_space(self):
        self.text_box.insert(tk.END, " ")

    def update(self):
        # Read a frame from the webcam
        ret, frame = self.cap.read()

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Get the current time and add it to the frame
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        cv2.putText(frame, f"Time: {timestamp}", (370, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame in the video label
        photo = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = cv2.resize(photo, (1400, 1000))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(photo))
        self.video_label.photo = photo
        self.video_label.config(image=photo)

        # Schedule the next update
        self.window.after(10, self.update)

    def take_picture(self, event=None):
        # Get the current time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Read a frame from the webcam
        ret, frame = self.cap.read()

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Save the image to a file
        folder = os.path.expanduser("~/Pictures")
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, f"photo_{timestamp}.png")
        cv2.imwrite(filename, frame)


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Create a PhotoImage object from the captured frame
    photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    from tkinter import NW
    canvas.create_image(0, 0, anchor=NW, image=photo)
    window.after(10, show_frame)


if __name__ == '__main__':
    app = App(tk.Tk(), "Tkinter OpenCV Webcam")

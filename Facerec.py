import cv2
import label_image
import time
import serial
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox
import pyglet

size = 4

root = Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=1)
root.title('Face Rec')
frame.config(background='light blue')
label = Label(frame, text="FaceRec", bg='light blue', font=('Times 35 bold'))
label.pack(side=TOP)
filename = ImageTk.PhotoImage(file="pemandangan.jpg")
background_label = Label(frame, image=filename)
background_label.pack(side=TOP)


def cont():
    tkinter.messagebox.showinfo("Contributor", "\n--Cef--")


def made():
    tkinter.messagebox.showinfo("About",'Thesis version v1.0\n Made Using: \n-Tensorflow\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')


menu = Menu(root)
root.config(menu=menu)

subm2 = Menu(menu)
menu.add_cascade(label="About", menu=subm2)
subm2.add_command(label="Cam", command=made)
subm2.add_command(label="Contributor", command=cont)


def exitt():
    exit()


def opencam():
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    webcam = cv2.VideoCapture(0)  # Using default WebCam connected to the PC.

    while True:
        (rval, im) = webcam.read()
        im = cv2.flip(im, 1, 0)  # Flip to act as a mirror

        # Resize the image to speed up detection
        mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))

        # detect MultiScale / faces
        faces = classifier.detectMultiScale(mini)

        key = cv2.waitKey(10)

        recognized = 0

        # Draw rectangles around each face
        for f in faces:
            (x, y, w, h) = [v * size for v in f]  # Scale the shapesize backup
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4)

            if key == ord('c'):
                # Save just the rectangle faces in SubRecFaces
                sub_face = im[y:y + h, x:x + w]

                FaceFileName = "test.jpg"  # Saving the current image from the webcam for testing.
                cv2.imwrite(FaceFileName, sub_face)

                text = label_image.test(
                    FaceFileName)  # Getting the Result from the label_image file, i.e., Classification Result.
                # text = text.title()# Title Case looks Stunning.
                font = cv2.FONT_HERSHEY_TRIPLEX
                # cv2.putText(im, text, (x + w, y), font, 1, (0, 0, 255), 2)

        if key == ord('q'):  # The Esc key
            break
        cv2.imshow("Capturing", im)
    webcam.release()
    cv2.destroyAllWindows()


def guideline():
    animation = pyglet.image.load_animation('gif.gif')
    animSprite = pyglet.sprite.Sprite(animation)

    w = animSprite.width
    h = animSprite.height

    window = pyglet.window.Window(width=w, height=h)

    r, g, b, alpha = 0.5, 0.5, 0.8, 0.5

    pyglet.gl.glClearColor(r, g, b, alpha)

    @window.event
    def on_draw():
        window.clear()
        animSprite.draw()

    pyglet.app.run()

def status():
    # Configure the serial port
    connection = serial.Serial('COM6', 9600)
    temp = 1 #code here


but1 = Button(frame, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=opencam, text='Open Cam',
              font=('helvetica 15 bold'))
but1.place(x=5, y=104)

but2 = Button(frame, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=status, text='Status',
              font=('helvetica 15 bold'))
but2.place(x=5, y=180)

but3 = Button(frame, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=guideline, text='Guideline',
              font=('helvetica 15 bold'))
but3.place(x=5, y=260)

but5 = Button(frame, padx=5, pady=5, width=5, bg='white', fg='black', relief=GROOVE, text='EXIT', command=exitt,
              font=('helvetica 15 bold'))
but5.place(x=210, y=478)

root.mainloop()
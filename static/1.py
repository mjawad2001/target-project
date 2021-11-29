import tkinter
from tkinter import *
from PIL import Image, ImageTk


main
root = Tk()

# Position text in frame
Label(root, text = 'Position image on button', font =('<font_name>', <font_size>)).pack(side = TOP, padx = <x_coordinate#>, pady = <y_coordinate#>)

# Create a photoimage object of the image in the path
photo = PhotoImage(file = "</path/image_name>")

# Resize image to fit on button
photoimage = photo.subsample(1, 2)

# Position image on button
Button(root, image = photoimage,).pack(side = BOTTOM, pady = <y_coordinate#>)
mainloop()

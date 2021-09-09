import PySimpleGUI as sg
from PIL import Image
import os
from sys import exit

images = []
first_image = ""
path = ""
output_name = ""

# PySimpleGUI setup
sg.theme('dark grey 13')
layout = [
    [sg.Text('Select a directory with input content')],
    [sg.Input(), sg.FolderBrowse()],
    [sg.Text('Output name')],
    [sg.Input(), sg.Text('.pdf')],
    [sg.OK(), sg.Cancel()]
]

window = sg.Window('Doujin to PDF', layout)

# Goes through each item in the directory.
# "opens" several images at a time. Creates a sort of collection of images in the elif branch.
# That collection of images is saved to a  pdf file, starting with the first image, which was opened separately.
def open_images(path):
    global first_image
    dir_list = os.listdir(path)
    dir_list = sorted(dir_list)

    for item in dir_list:
        full_path = path + os.path.sep + item
        # Check if it's the first item.
        if item == dir_list[0]:
            first_image = Image.open(full_path)
        elif item.endswith(('.jpg', '.jpeg', '.bmp')):
            print(full_path)
            im1 = Image.open(full_path)
            images.append(im1)
        # png files need their alpha channel removed before being saved to a pdf
        elif item.endswith(('.png')):
            png = Image.open(full_path)
            png.load() # loading it to be able to do png.split().
            background = Image.new('RGB', png.size, (255,255,255)) # Make another image that's all white.
            background.paste(png, mask=png.split()[3]) # place the background on the alpha channel of the png.
            images.append(background)

def create_pdf(path, output_name):
    global first_image
    pdf_path = path + os.path.sep + output_name + ".pdf"
    first_image.save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images)


# Running the window and getting user input.
while True:
    # values is a dictionary, not a list.
    event, values = window.read()

    # Close the window and quit when the Cancel button is clicked.
    if event in (sg.WIN_CLOSED, 'Cancel'):
        exit()
        break
    else:
        path = values[0]
        output_name = values[1]
        if os.path.isdir(path):
            open_images(path)
            create_pdf(path, output_name)
            break

exit()

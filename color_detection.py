import cv2
import numpy as np
import pandas as pd
import argparse

# Creating argument parser to take image path from command line
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-i', '--image', required=True, help="Image Path")
arguments = vars(arg_parser.parse_args())
image_path = arguments['image']

# Reading the image with OpenCV
image = cv2.imread(image_path)

# Declaring global variables (used later on)
clicked = False
r_value = g_value = b_value = x_pos = y_pos = 0

# Reading CSV file with Pandas and providing names to each column
column_names = ["color", "color_name", "hex_code", "Red", "Green", "Blue"]
color_data = pd.read_csv('colors.csv', names=column_names, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(red, green, blue):
    min_distance = 10000
    for i in range(len(color_data)):
        distance = abs(red - int(color_data.loc[i, "Red"])) + abs(green - int(color_data.loc[i, "Green"])) + abs(blue - int(color_data.loc[i, "Blue"]))
        if distance <= min_distance:
            min_distance = distance
            color_name = color_data.loc[i, "color_name"]
    return color_name

# Function to get x, y coordinates of mouse double click
def handle_mouse_event(event, x, y, flags, param):
    global b_value, g_value, r_value, x_pos, y_pos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        x_pos = x
        y_pos = y
        b_value, g_value, r_value = image[y, x]

cv2.namedWindow('image')
cv2.setMouseCallback('image', handle_mouse_event)

while True:
    cv2.imshow("image", image)
    if clicked:
        cv2.rectangle(image, (20, 20), (750, 60), (int(b_value), int(g_value), int(r_value)), -1)
        color_text = get_color_name(r_value, g_value, b_value) + ' R=' + str(r_value) + ' G=' + str(g_value) + ' B=' + str(b_value)
        cv2.putText(image, color_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r_value + g_value + b_value >= 600:
            cv2.putText(image, color_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

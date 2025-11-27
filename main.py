import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

sobel_operator_matrix = [
    [[1,2,1], [0,0,0], [-1,-2,-1]], 
    [[-1,0,1], [-2,0,2], [-1,0,1]]
]
prewitt_operator_matrix = [
    [[1,1,1], [0,0,0], [-1,-1,-1]],
    [[-1,0,1], [-1,0,1], [-1,0,1]]
]

titles = ["Original Image", "Combined", "X", "Y"]

def main():
    root = tk.Tk()
    root.withdraw()
    user_operator = input("Type \n1 for Sober Operator\n2 for Prewitt Operator\n0 to exit\n")
    
    if user_operator == "1":
        print(">> Sobel Operator selected.")
        [image, abs_x, abs_y, combined] = operateOnImage(sobel_operator_matrix)
    elif user_operator == "2":
        print(">> Prewitt Operator selected.")
        [image, abs_x, abs_y, combined] = operateOnImage(prewitt_operator_matrix)
    elif user_operator == "0":
        print(">> exiting...")
        exit()
    else:
        print("Error: operator checking went wrong!")

    images = [image, combined, abs_x, abs_y]
    plt.rcParams['tk.window_focus'] = False
    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

def operateOnImage(operator_matrix):
    image_path = filedialog.askopenfilename(
        title="Select an image file"
    )
    if not image_path:
        print("No file selected - exiting.")
        exit()

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    operator_x_matrix = np.array(operator_matrix[0], dtype=int)
    operator_y_matrix = np.array(operator_matrix[1], dtype=int)

    operator_x = cv2.filter2D(image, cv2.CV_64F, operator_x_matrix)
    operator_y = cv2.filter2D(image, cv2.CV_64F, operator_y_matrix)

    abs_operator_x = cv2.convertScaleAbs(operator_x)
    abs_operator_y = cv2.convertScaleAbs(operator_y)
    operator_combined = cv2.addWeighted(abs_operator_x, 0.5, abs_operator_y, 0.5, 0)

    return [image, abs_operator_x, abs_operator_y, operator_combined]

if __name__ == "__main__":
    main()

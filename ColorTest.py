import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def update_hsv():
    lower_blue = np.array([lower_hue.get(), lower_saturation.get(), lower_value.get()])
    upper_blue = np.array([upper_hue.get(), upper_saturation.get(), upper_value.get()])

    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Blue Object Detection", result)

    # 打印当前HSV值
    print(f"Lower HSV: ({lower_hue.get()}, {lower_saturation.get()}, {lower_value.get()})")
    print(f"Upper HSV: ({upper_hue.get()}, {upper_saturation.get()}, {upper_value.get()})")

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        global frame
        frame = image.copy()
        global hsv_frame
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        update_hsv()

def on_closing():
    cv2.destroyAllWindows()
    root.destroy()

root = tk.Tk()
root.title("Blue Object Detection")

lower_hue = tk.IntVar(value=90)
upper_hue = tk.IntVar(value=120)

lower_saturation = tk.IntVar(value=100)
upper_saturation = tk.IntVar(value=255)

lower_value = tk.IntVar(value=100)
upper_value = tk.IntVar(value=255)

hue_label = ttk.Label(root, text="Hue")
hue_label.grid(row=0, column=0)
hue_scale = ttk.Scale(root, from_=0, to=180, variable=lower_hue)
hue_scale.grid(row=0, column=1)
hue_scale_upper = ttk.Scale(root, from_=0, to=180, variable=upper_hue)
hue_scale_upper.grid(row=0, column=2)

saturation_label = ttk.Label(root, text="Saturation")
saturation_label.grid(row=1, column=0)
saturation_scale = ttk.Scale(root, from_=0, to=255, variable=lower_saturation)
saturation_scale.grid(row=1, column=1)
saturation_scale_upper = ttk.Scale(root, from_=0, to=255, variable=upper_saturation)
saturation_scale_upper.grid(row=1, column=2)

value_label = ttk.Label(root, text="Value")
value_label.grid(row=2, column=0)
value_scale = ttk.Scale(root, from_=0, to=255, variable=lower_value)
value_scale.grid(row=2, column=1)
value_scale_upper = ttk.Scale(root, from_=0, to=255, variable=upper_value)
value_scale_upper.grid(row=2, column=2)

load_button = ttk.Button(root, text="Load Image", command=load_image)
load_button.grid(row=3, column=0, columnspan=3)

update_button = ttk.Button(root, text="Update", command=update_hsv)
update_button.grid(row=4, column=0, columnspan=3)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

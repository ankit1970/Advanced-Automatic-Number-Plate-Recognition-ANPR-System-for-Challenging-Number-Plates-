import cv2
import pandas as pd
from ultralytics import YOLO
import numpy as np
import pytesseract
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk

#Loading
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Loading model weight
model = YOLO('best.pt')

# Taking Video/Image as Input
cap = cv2.VideoCapture('mycarplate.mp4')
#input_file = sys.argv[1]
#cap=cv2.imread('mycarplate1.jpg')


my_file = open("coco1.txt", "r")
data = my_file.read()
class_list = data.split("\n")
area = [(27, 417), (16, 456), (1015, 451), (992, 417)]

processed_numbers = set()

#GUI implementation code

root = Tk()
root.title("Advanced ANPR System")
video_paused = False

frame_label = Label(root)
log_label = Label(root, text="Detected Plates:")
list_box = Listbox(root, width=50)
crop_label = Label(root)
control_frame = Frame(root)

pause_button = Button(control_frame, text="Pause", command=lambda: set_video_paused(True))
pause_button.pack(side=LEFT, padx=5, pady=5)

resume_button = Button(control_frame, text="Resume", command=lambda: set_video_paused(False))
resume_button.pack(side=LEFT, padx=5, pady=5)

def set_video_paused(paused):
    global video_paused
    video_paused = paused

def update_gui(image, cropped_image, detections):
    img = Image.fromarray(image)
    img_tk = ImageTk.PhotoImage(image=img)
    frame_label.imgtk = img_tk
    frame_label.configure(image=img_tk)
    frame_label.update()

    if cropped_image is not None:
        crop_img = Image.fromarray(cropped_image)
        crop_img_tk = ImageTk.PhotoImage(image=crop_img)
        crop_label.imgtk = crop_img_tk
        crop_label.configure(image=crop_img_tk)
        crop_label.update()

    for det in detections:
        list_box.insert(END, det)
        list_box.update()

def show_main_window():
    start_frame.pack_forget()
    frame_label.pack()
    log_label.pack()
    list_box.pack()
    crop_label.pack()
    control_frame.pack()

def start_detection():
    show_main_window()
    main()

def main():
    while True:
        if not video_paused:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (1020, 500))
            results = model.predict(frame)
            px = pd.DataFrame(results[0].boxes.data).astype("float")

            detections = []
            cropped_img = None
            for index, row in px.iterrows():
                x1, y1, x2, y2, conf, d = map(float, row)
                c = class_list[int(d)]
                if cv2.pointPolygonTest(np.array(area, np.int32), ((x1 + x2) // 2, (y1 + y2) // 2), False) >= 0:
                    crop = frame[int(y1):int(y2), int(x1):int(x2)]
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    gray = cv2.bilateralFilter(gray, 10, 20, 20)
                    text = pytesseract.image_to_string(gray).strip()
                    text = text.replace('(', '').replace(')', '').replace(',', '').replace(']','')
                    if text not in processed_numbers:
                        processed_numbers.add(text)
                        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       
                        detection_info = f"{text} at {current_datetime})"
                        detections.append(detection_info)
                        cropped_img = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

            update_gui(frame, cropped_img, detections)
        root.update_idletasks()
        root.update()
        

    cap.release()
    cv2.destroyAllWindows()

# Welcome screen setup
start_frame = Frame(root)
start_frame.pack(expand=YES, fill=BOTH)

# Load, resize and display the project photo as background
project_image = Image.open("logo.jpg")
project_image = project_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
Project_photo = ImageTk.PhotoImage(project_image)
background_label = Label(start_frame, image=Project_photo)
background_label.place(relwidth=1, relheight=1)  # Make the background label fill the frame

# Overlay text and buttons on the background image
title_label = Label(start_frame, text="Advanced Automatic Number Plate Recognition (ANPR)", font=("Helvetica", 24, "bold"), bg='light blue', fg='black')
title_label.pack(pady=(20, 0))
title_label = Label(start_frame, text="System for Challenging Number Plates", font=("Helvetica", 24, "bold"), bg='light blue', fg='black')
title_label.pack(pady=(20, 0))



# Start detection button
start_button = Button(start_frame, text="Start Detection", font=("Helvetica", 12, "bold"), command=start_detection, bg='light blue', fg='black')
start_button.pack(pady=20, side=BOTTOM)

root.mainloop()

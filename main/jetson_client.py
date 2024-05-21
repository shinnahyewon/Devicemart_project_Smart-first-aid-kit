'''
Jetson Nano Client : 영상처리
작성일 : 2024.03.30
''' 
import cv2
import tkinter as tk
import socket
import threading
import sys
import time
import re

from tkinter import messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk

HOST = "10.10.14.70"
PORT = 5000
ADDR = (HOST,PORT)
CONFIDENCE_THRESHOLD = 0.4
recvId = "JETSON"
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[JETSON:PASSWD]'.encode()) 
		time.sleep(0.5)
		while True: 
			data = input() 
			data = bytes(data+'\n', "utf-8") 
			s.send(data) 
			s.close() 
	def gettingMsg(): 
		global rsplit
		global recvFlag
		while True: 
			data = s.recv(1024) 
			rstr = data.decode("utf-8")
			rsplit = re.split('[\]|\[@]|\n',rstr)  #'[',']','@' 분리
			recvFlag = True

		s.close() 
	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,()) 
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')
ledFlag = False

#모델 로드
model = YOLO('model/best_h3.pt')
class_names = ['bites', 'burns', 'cuts']

# 웹캠 설정
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    messagebox.showerror("Camera Error", "Could not open the camera.")
    sys.exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)


box_colors = {
    'bites': (0, 255, 0),   # Green
    'burns': (0, 0, 255),   # Red
    'cuts': (255, 0, 0)    # Blue
}

paused = True

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        Pause_button_text.set("Resume")
    else:
        Pause_button_text.set("Pause")
        detect_objects(panel)


def show_info():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)    
        detection = model(image)[0]
        
        class_detected = []
        for data in detection.boxes.data.tolist(): 
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            label = int(data[5])  
            class_name = class_names[label]  
            class_detected.append(class_name)
        
        if class_detected:
            info_label.config(text="Class Currently Recognized: " + ', '.join(class_detected))
            if class_name == 'bites':
                info_label.config(text="벌레 물린 상처 : 벌레 연고")
                data = "[BT]SERVO@ON"
                data = bytes(data+'\n', "utf-8") 
                s.send(data)
            
            elif class_name == 'burns':
                info_label.config(text="화상 상처 : 연고 및 화상 밴드")
                data = "[BT]MOTOR1@ON"
                data = bytes(data+'\n', "utf-8") 
                s.send(data)
                data = "[BT]MOTOR2@ON"
                data = bytes(data+'\n', "utf-8") 
                s.send(data)
            
            elif class_name == 'cuts':
                info_label.config(text="베임 상처 : 밴드")
                data = "[BT]MOTOR1@ON"
                data = bytes(data+'\n', "utf-8") 
                s.send(data)
 
            
            else:
                info_label.config(text="재감지 필요")
            
        else:
            info_label.config(text="No classes detected")


def detect_objects(panel):
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)    
        detection = model(image)[0]

        for data in detection.boxes.data.tolist(): 
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = map(int, data[:4])
            label = int(data[5])  
            class_name = class_names[label]  
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_colors[class_name], 2)
            cv2.putText(frame, f'{class_name}: {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_colors[class_name], 2)

        frame = cv2.resize(frame, (440, 440))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        panel.config(image=photo)
        panel.image = photo
        
    if not paused:
        panel.after(300, detect_objects, panel)

def send_command(command_str):
    """서버에 명령을 전송합니다. 문자열을 인코딩하여 바이트로 변환합니다."""
    command_bytes = command_str.encode()  # 문자열을 바이트로 인코딩
    s.send(command_bytes)
    
#GUI 설정
window = tk.Tk()
window.title("Injury Detection Application")

bin = tk.PhotoImage(file="data/hurtlogo3.png")
bin_label = tk.Label(window, image=bin)
bin_label.grid(row=0, column=2, padx=10, pady=10,  rowspan=6)

panel = tk.Label(window)
panel.grid(row=0, column=2, padx=10, pady=10,  rowspan=6)

logo = tk.PhotoImage(file="data/hurtlogo1.png")
logo_label = tk.Label(window, image=logo)
logo_label.grid(row=0, column=0, columnspan=2)

title_label = tk.Label(window, text="Please recognize the injury on camera", font=("Helvetica", 12))
title_label.grid(row=1, column=0, columnspan=2, pady=1)

Pause_button_text = tk.StringVar()
Pause_button_text.set("Resume")
Pause_button = tk.Button(window, textvariable=Pause_button_text, command=toggle_pause, width=10, height=1, font=("Helvetica", 15))
Pause_button.grid(row=2, column=0, padx=2, pady=1)

exit_button = tk.Button(window, text="Exit", command=window.quit, width=10, height=1, font=("Helvetica", 15))
exit_button.grid(row=2, column=1, padx=2, pady=1)

info_button = tk.Button(window, text="진단", command=show_info, width=24, height=2, font=("Helvetica", 15))
info_button.grid(row=3, column=0, columnspan=2, padx=2, pady=1,)

info_label = tk.Label(window, text="", font=("Helvetica", 12))
info_label.grid(row=4, column=0, columnspan=2, padx=2, pady=1)

window.mainloop()

cap.release()
s.close()
cv2.destroyAllWindows()

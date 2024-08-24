import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import serial
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

class SerialCommunicator:
    def __init__(self, serial_const, controller):
        self.serial_port = None
        self.serial_const = serial_const
        self.controller = controller
        self.open()
        self.data = [0] * 20
        self.last_data = [0] * 20 
        self.arduino_data = ""
        self.received_data_list = []

        self.read_thread = threading.Thread(target=self.read_from_arduino)
        self.read_thread.daemon = True
        self.read_thread.start()

    def open(self):
        for i in range(13):
            try:
                port_name = f"COM{i}"
                self.serial_port = serial.Serial(port_name, self.serial_const.speed, timeout=self.serial_const.timeout)
                print(f"Connected to {port_name}")
                return
            except serial.SerialException as e:
                print(f"Could not open {port_name}: {e}")
        
        raise Exception("No available COM port found")

    def communicate(self):
        new_data = self.controller.check_state()
        if new_data is None or not isinstance(new_data, list):
            return
        
        self.last_data = self.data
        self.data = new_data

        data_str = ','.join(map(str, self.data)) + '\n'

        try:
            self.serial_port.write(data_str.encode())
            print("Sent:", data_str.encode())
        except Exception as e:
            print("Error sending data:", e)

    def read_from_arduino(self):
        while True:
            try:
                if self.serial_port and self.serial_port.is_open:
                    if self.serial_port.in_waiting > 0:
                        received_line = self.serial_port.readline().decode().strip()
                        print("Received:", received_line)
                        
                        self.received_data_list.append(received_line)

                        data_parts = received_line.split(',')
                        if len(data_parts) == 7:
                            self.arduino_data = received_line
                        else:
                            print("Received incomplete or excess data. Length:", len(data_parts))
            except serial.SerialException as e:
                print(f"SerialException in read_from_arduino: {e}")
                break
            except Exception as e:
                print(f"Exception in read_from_arduino: {e}")

    def close(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                print("Serial port closed")
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")

class Application(tk.Tk):
    def __init__(self, serial_communicator, kanicam):
        super().__init__()
        self.serial_communicator = serial_communicator
        self.kanicam = kanicam
        self.title("Camera and Serial Communication")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.toggle_fullscreen)
        self.bind("<BackSpace>", self.on_closing)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.camera_width = int(1920 / 1.6)
        self.camera_height = int(1080 / 1.4)

        self.camera_frame = tk.Frame(self.main_frame, width=self.camera_width, height=self.camera_height)
        self.camera_frame.place(x=0, y=0)

        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=0, y=self.camera_height + 10) 

        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        self.sdata_label = Label(self.data_frame, text="Send Data: ", font=("Helvetica", 18), anchor='w', width=120, padx=10)
        self.sdata_label.pack()

        self.rdata_label = Label(self.data_frame, text="Received Data: ", font=("Helvetica", 18), anchor='w', width=120, padx=10)
        self.rdata_label.pack()

        self.update_frame()

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
        return "break"

    def format_data(self, data_list):
        formatted_data = []
        for i, value in enumerate(data_list):
            if i < 4:
                formatted_data.append(f"{int(value):04d}")
            else:
                formatted_data.append(str(int(value)))
        return ', '.join(formatted_data)

    def format_received_data(self, data_list):
        formatted_data = []
        for i, value in enumerate(data_list):
            try:
                if i < 6:
                    formatted_data.append(f"{int(value):05d}")
                else:
                    formatted_data.append(str(int(value)))
            except ValueError:
                formatted_data.append(value)
        return ', '.join(formatted_data)

    def update_frame(self):
        # Read image from camera
        ret, frame = self.kanicam.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # Resize image
            new_width = self.camera_width
            new_height = self.camera_height
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        # Communicate with the serial port
        self.serial_communicator.communicate()
        send_data = self.format_data(self.serial_communicator.last_data)
        self.sdata_label.config(text=f"Send data       : {send_data}")

        # Check if we need to save the image
        if self.serial_communicator.data[13] == 1:
            self.kanicam.save_img(frame)

        if self.serial_communicator.data[12] == 1:
            self.kanicam.clear_img()

        # Format and display received data
        received_data = self.serial_communicator.arduino_data.split(',')
        formatted_received_data = self.format_received_data(received_data)
        received_data_list = formatted_received_data.split(',')
        received_data_list = (received_data_list + [''] * 7)[:7]
        self.rdata_label.config(text=f"Actuator value : {', '.join(received_data_list)}")

        # Schedule the next update
        self.after(10, self.update_frame)


    def on_closing(self, event=None):
        self.kanicam.cap.release()
        self.serial_communicator.close()
        self.destroy()

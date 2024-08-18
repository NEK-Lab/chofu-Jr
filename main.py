import cv2
import serial
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from setting import serial_setting
from controller import logicool_controller
from kanicam import webcamcapture

serial_const = serial_setting()
controller = logicool_controller()
kanicam = webcamcapture()

class SerialCommunicator:
    def __init__(self):
        self.serial_port = None
        self.open()
        self.data = [0] * 20
        self.last_data = [0] * 20  # Store last valid data

    def open(self):
        for i in range(13):
            try:
                port_name = f"COM{i}"
                self.serial_port = serial.Serial(port_name, serial_const.speed, timeout=serial_const.timeout)
                print(f"Connected to {port_name}")
                return
            except serial.SerialException:
                print(f"Could not open {port_name}")
        
        raise Exception("No available COM port found")

    def communicate(self):
        new_data = controller.check_state()
        if new_data is None or not isinstance(new_data, list):
            return
        
        self.last_data = self.data  # Update last valid data only if new data is valid
        self.data = new_data

        data_str = ','.join(map(str, self.data)) + '\n'

        try:
            self.serial_port.write(data_str.encode())
            print("Sent:", data_str.encode())
        except Exception as e:
            print("Error sending data:", e)

    def read_from_arduino(self):
        if self.serial_port.in_waiting > 0:
            received_data = self.serial_port.read(self.serial_port.in_waiting)
            print("Received:", received_data.decode().strip())

    def close(self):
        if self.serial_port.is_open:
            self.serial_port.close()
            print("Serial port closed")

    def capture(self):
        if self.data:
            if self.data[12] == 1:
                kanicam.clear_img()
            if self.data[13] == 1:
                ret, frame = kanicam.cap.read()
                if ret:
                    kanicam.save_img(frame)

class Application(tk.Tk):
    def __init__(self, serial_communicator):
        super().__init__()
        self.serial_communicator = serial_communicator
        self.title("Camera and Serial Communication")
        self.attributes('-fullscreen', True)  # Set fullscreen mode
        self.bind("<Escape>", self.toggle_fullscreen)  # Press Escape to exit fullscreen

        # Create a main frame to hold everything
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the camera
        self.camera_frame = tk.Frame(self.main_frame)
        self.camera_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for the serial data
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Camera display label
        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Serial communication data display label
        self.data_label = Label(self.data_frame, text="Serial Data: ", font=("Helvetica", 14))
        self.data_label.pack(fill=tk.X)

        # Update the frame
        self.update_frame()

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
        return "break"

    def update_frame(self):
        ret, frame = kanicam.cap.read()
        if ret:
            # Convert OpenCV image to PIL format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        # Handle serial communication
        self.serial_communicator.communicate()
        self.serial_communicator.read_from_arduino()
        self.serial_communicator.capture()

        # Use last_data if current data is None
        data_to_display = self.serial_communicator.data if self.serial_communicator.data else self.serial_communicator.last_data
        self.data_label.config(text=f"Serial Data: {data_to_display}")

        # Update the frame every 10 ms
        self.after(10, self.update_frame)

    def on_closing(self):
        kanicam.cap.release()
        self.serial_communicator.close()
        self.destroy()

if __name__ == "__main__":
    serial_comm = SerialCommunicator()
    app = Application(serial_comm)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import serial
import threading
import logging

# Configure logging
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
        self.received_data_list = []  # List to store received data

        # Start a thread for reading from Arduino
        self.read_thread = threading.Thread(target=self.read_from_arduino)
        self.read_thread.daemon = True  # Allow thread to exit when main program exits
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
                        
                        # Save the received line to the list
                        self.received_data_list.append(received_line)

                        # Optionally, parse and process the received line
                        data_parts = received_line.split(',')
                        if len(data_parts) == 7:
                            self.arduino_data = received_line
                        else:
                            print("Received incomplete or excess data. Length:", len(data_parts))
            except serial.SerialException as e:
                print(f"SerialException in read_from_arduino: {e}")
                break  # Exit the loop if there's a serial exception
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
        self.attributes('-fullscreen', True)  # Set fullscreen mode
        self.bind("<Escape>", self.toggle_fullscreen)  # Press Escape to exit fullscreen
        self.bind("<BackSpace>", self.on_closing)  # Bind Backspace key to exit

        # Create a frame for the layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Updated size for the camera area
        self.camera_width = int(1920 / 1.6)  # Increase width as needed
        self.camera_height = int(1080 / 1.4)  # Increase height as needed

        # Create a frame for the camera
        self.camera_frame = tk.Frame(self.main_frame, width=self.camera_width, height=self.camera_height)
        self.camera_frame.place(x=0, y=0)  # Position (x, y)

        # Create a frame for the serial data
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.place(x=0, y=self.camera_height + 10)  # Position below the camera frame with some padding

        # Camera display label
        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Serial communication data display labels with fixed width and left-aligned text
        # Serial communication data display labels with fixed width and left-aligned text
        self.sdata_label = Label(self.data_frame, text="Send Data: ", font=("Helvetica", 18), anchor='w', width=120, padx=10)
        self.sdata_label.pack()

        self.rdata_label = Label(self.data_frame, text="Received Data: ", font=("Helvetica", 18), anchor='w', width=120, padx=10)
        self.rdata_label.pack()


        # Update the frame
        self.update_frame()

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
        return "break"

    def format_data(self, data_list):
        """送信データをフォーマットするための関数"""
        formatted_data = []
        for i, value in enumerate(data_list):
            if i < 4:
                # 最初の4つの要素を4桁で表示
                formatted_data.append(f"{int(value):04d}")
            else:
                # その他の要素は通常の形式で表示
                formatted_data.append(str(int(value)))
        return ', '.join(formatted_data)

    def format_received_data(self, data_list):
        """受信データをフォーマットするための関数"""
        formatted_data = []
        for i, value in enumerate(data_list):
            try:
                if i < 6:
                    # 最初の6つの要素を5桁で表示
                    formatted_data.append(f"{int(value):05d}")
                else:
                    # その他の要素は通常の形式で表示
                    formatted_data.append(str(int(value)))
            except ValueError:
                # 数値に変換できない場合は、そのままの文字列を追加
                formatted_data.append(value)
        return ', '.join(formatted_data)

    def update_frame(self):
        ret, frame = self.kanicam.cap.read()
        if ret:
            # Convert OpenCV image to PIL format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # Resize the image (for example, double the size)
            new_width = self.camera_width  # Change as needed
            new_height = self.camera_height  # Change as needed
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        # Handle serial communication
        self.serial_communicator.communicate()

        # Display the last sent data
        send_data = self.format_data(self.serial_communicator.last_data)
        self.sdata_label.config(text=f"Send data       : {send_data}")

        # Display the received data
        received_data = self.serial_communicator.arduino_data.split(',')
        formatted_received_data = self.format_received_data(received_data)

        # Split formatted_received_data into a list with exactly 7 elements
        received_data_list = formatted_received_data.split(',')
        received_data_list = (received_data_list + [''] * 7)[:7]

        # Update rdata_label with the 7-element list
        self.rdata_label.config(text=f"Actuator value : {', '.join(received_data_list)}")

        # Update the frame every 10 ms
        self.after(10, self.update_frame)

    def on_closing(self, event=None):
        self.kanicam.cap.release()
        self.serial_communicator.close()
        self.destroy()

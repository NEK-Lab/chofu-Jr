import cv2
import os
import datetime

from setting import camera_setting

cam_const = camera_setting()

class webcamcapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(cam_const.camid)
        if not self.cap.isOpened():
            raise ValueError("failed cam open")
        self.save_dir = cam_const.save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def show_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("faild get flame")
                break

            cv2.imshow('Webcam', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.save_img(frame)
            elif key == ord('c'):
                self.clear_img()

        self.cap.release()
        cv2.destroyAllWindows()

    def save_img(self, frame):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = os.path.join(self.save_dir, f'photo_{timestamp}.jpg')
        cv2.imwrite(photo_filename, frame)
        print(f"save img: {photo_filename}")

    def clear_img(self):
        for filename in os.listdir(self.save_dir):
            file_path = os.path.join(self.save_dir, filename)
            if os.path.isfile(file_path) and filename.endswith('.jpg'):
                os.remove(file_path)
                print(f"delete: {file_path}")
        print("delete all img")

if __name__ == "__main__":
    webcam = webcamcapture()
    webcam.show_video()

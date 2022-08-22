import tkinter as tk
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
from main import process
from config import Config as cfg
from calculate_thickness import distribute_thickness
from interpretation_of_result import create_histogram


class CameraView(tk.Label):
    def __init__(self, owner, source: cv2.VideoCapture, **kwargs):
        super().__init__(owner, **kwargs)
        self.source = source
        self.last_frame = None
        self._rgb_image = None
        self.after(20, self._update)

    def _update(self):
        if self.source.isOpened():
            success, self.last_frame = self.source.read(self.last_frame)
            if success:
                self._rgb_image = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB, self._rgb_image)
                img = Image.fromarray(self._rgb_image)
                # Convert image to PhotoImage
                imgtk = ImageTk.PhotoImage(image=img)
                self.imgtk = imgtk
                self.configure(image=imgtk)
        self.after(20, self._update)


class MainWindow(tk.Frame):
    def __init__(self, cap, master, **kwargs):
        super().__init__(master, **kwargs)
        self.cap = cap
        self.panel = tk.Frame(self)
        self.btn_camera = tk.Button(self.panel, text='Снимок', command=self.camera_press)  # button
        self.btn_file = tk.Button(self.panel, text='Файл', command=self.file_press)  # button
        self.histogram_file = tk.Button(self.panel, text='Создать гистограмму', command=self.histogram_press)  # button
        self.check_box = tk.Checkbutton(self.panel, text='Субпиксельная', onvalue=0, offvalue=1,
                                        command=self.on_correction)
        self.btn_camera.pack(side='left')
        self.btn_file.pack(side='left')
        self.histogram_file.pack(side='right')
        self.check_box.pack(side='left')
        self.panel.pack(side='top')
        self.label = CameraView(self, cap)  # our custom label
        self.label.pack(side='top')
        self.thickness = []

    def camera_press(self):
        success, frame = self.cap.read()

    def file_press(self):
        filename = tk.filedialog.askopenfilename()
        part_thickness = process(filename, cfg.scale)
        self.thickness.extend(part_thickness)

    def histogram_press(self):
        if len(self.thickness) > 0:
            tmp, average = distribute_thickness(self.thickness)
            create_histogram(tmp, average)
        self.thickness.clear()

    def on_correction(self):
        cfg.correction = not cfg.correction


if __name__ == '__main__':
    print('Connecting to video source...')
    cap = cv2.VideoCapture(0)
    try:
        root = tk.Tk()
        win = MainWindow(cap, root)
        win.pack(fill='both')
        win.mainloop()
    finally:
        cap.release()

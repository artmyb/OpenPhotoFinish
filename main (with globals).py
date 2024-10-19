# pyinstaller main.py --windowed --onefile --name "MY Photo-Finish" --icon "icon.ico"

import cv2
import tkinter as tk
from tkinter import filedialog
import time
import os
from PIL import ImageTk, Image
import numpy as np
import sounddevice as sd
from tkinter import ttk
import tkinter.messagebox
import io
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import soundfile as sf
from PIL import Image, ImageGrab
import pyautogui
import functools

result_times = []

sounddevices = []
index_sound = 0

class VideoRecorder:
    def __init__(self, root):
        self.mousex = 0
        self.mousey = 0
        self.root = root
        self.camera_index = 0
        self.cap = cv2.VideoCapture(self.camera_index)
        # self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fps = 5
        print(self.fps)
        self.out = None
        self.recording = False
        self.start_time = 0
        self.soundlevel = 0
        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.default_athlete = {"lane": "NA", "id": "NA", "name": "NA", "affiliation": "NA", "license": "NA",
                                "time": "NA", "place": "NA"}
        self.athletes = [
            {"lane": "4", "id": "656", "name": "Usain Bolt", "affiliation": "Jamaica", "license": "Professional",
             "time": "9.58", "place": "1"}]
        self.athlete_properties = ("lane", "id", "name", "affiliation", "license", "time", "place")

        self.time_offset = 0

        self.maxvolume = 300

        self.message = 0

        button_frame = tk.Frame(self.root)
        button_frame.pack(anchor=tk.NW)

        self.add_cursor = tk.Button(button_frame, image=addcursorpic)
        self.add_cursor.pack(side=tk.LEFT)
        self.add_cursor.bind("<Enter>", lambda event: self.tooltip(area="cursor"))
        self.add_cursor.bind("<Leave>", self.tooltip)
        self.backward = tk.Button(button_frame, image=backwardpic,
                                  command=lambda: self.handle_scroll(event=0, transfer=-1))
        self.backward.pack(side=tk.LEFT)
        self.backward.bind("<Enter>", lambda event: self.tooltip(area="backward"))
        self.backward.bind("<Leave>", self.tooltip)
        self.forward = tk.Button(button_frame, image=forwardpic,
                                 command=lambda: self.handle_scroll(event=0, transfer=1))
        self.forward.pack(side=tk.LEFT)
        self.forward.bind("<Enter>", lambda event: self.tooltip(area="forward"))
        self.forward.bind("<Leave>", self.tooltip)
        self.plus = tk.Button(button_frame, image=pluspic, command=lambda: self.handle_scroll(1))
        self.plus.pack(side=tk.LEFT)
        self.plus.bind("<Enter>", lambda event: self.tooltip(area="plus"))
        self.plus.bind("<Leave>", self.tooltip)
        self.minus = tk.Button(button_frame, image=minuspic, command=lambda: self.handle_scroll(-1))
        self.minus.pack(side=tk.LEFT)
        self.minus.bind("<Enter>", lambda event: self.tooltip(area="minus"))
        self.minus.bind("<Leave>", self.tooltip)
        self.start_time_button = tk.Button(button_frame, image=startpic, command=self.determine_start_time)
        self.start_time_button.pack(side=tk.LEFT)
        self.start_time_button.bind("<Enter>", lambda event: self.tooltip(area="start time"))
        self.start_time_button.bind("<Leave>", self.tooltip)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', pady=10)

        self.pfcanvas = tk.Canvas(self.root, bg="black")
        self.pfcanvas.pack(fill='both', expand=True)

        self.pfcanvas.bind("<MouseWheel>", self.handle_scroll)
        self.pfcanvas.bind("<Button-1>", self.on_click)
        self.pfcanvas.bind("<Motion>", self.on_mouse_motion)

        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import", command=self.create_timeline)
        file_menu.add_command(label="Export", command=self.take_canvas_screenshot)
        file_menu.add_separator()
        file_menu.add_command(label="Options", command=self.options)
        file_menu.add_command(label="Exit", command=root.destroy)
        self.root.config(menu=menu_bar)

        self.cursorline = self.pfcanvas.create_line(self.pfcanvas.winfo_width() / 2, 0, self.pfcanvas.winfo_width() / 2,
                                                    self.pfcanvas.winfo_height(),
                                                    fill="black")

        self.button_height = 100
        self.options_button = tk.Button(root, image=iconopt, command=self.options, width=self.button_height,
                                        height=self.button_height)
        self.options_button.pack(side=tk.RIGHT, anchor=tk.S)

        self.results_button = tk.Button(root, image=resultpic,
                                        command=self.result, width=self.button_height, height=self.button_height)
        self.results_button.pack(side=tk.RIGHT, anchor=tk.S)

        self.create_timeline_button = tk.Button(root, text="Import Video", font=("Times", 30),
                                                pady=self.button_height // 7.5, command=self.create_timeline)
        self.create_timeline_button.pack(side=tk.RIGHT, anchor=tk.S)

        self.stop_button = tk.Button(root, text="Stop", font=("Times", 30), pady=self.button_height // 7.5,
                                     command=self.stop_recording,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, anchor=tk.S)

        self.listen_button = tk.Button(root, text="Listen to Start Gun", font=("Times", 30),
                                       pady=self.button_height // 7.5, command=self.listen_start_gun)
        self.listen_button.pack(side=tk.RIGHT, anchor=tk.S)

        tk.Label(root, text="i", font=("elephant", 10, "italic"), foreground='#0000FF').pack(side=tk.LEFT, anchor=tk.S)
        self.message = tk.Label(root, text="MY Photo-Finish by METU Athletics", font=("Arial", 10))
        self.message.pack(side=tk.LEFT, anchor=tk.S)
        self.zoom_label = tk.Label(root, text="| Zoom Level: x1", font=("Arial", 10), )
        self.zoom_label.pack(side=tk.LEFT, anchor=tk.S)
        self.threshold = 0.5
        self.threshold_var = tk.DoubleVar(value=self.threshold)

        self.canvas = None

        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Threshold for audio detection
        self.results = []
        self.result_cursors = []
        self.sound_device_index = 1
        self.sample_rate = thesounddevices[self.sound_device_index][2]
        self.sample_rate = float(self.sample_rate)

        self.audio_stream = None
        self.line_thickness = 2

        self.image_middle = 0.5

        self.timeline_image = 0
        self.zoom_level = 1
        self.maxzoom = 12
        self.ticklines = []
        self.image_x_min = 0
        self.image_x_max = self.pfcanvas.winfo_width()
        self.audiodata = 0
        self.audiosamplerate = 0
        self.audiozoomlevel = 0
        self.audiostart = 0
        self.results_on = 0
        self.options_on = 0
        self.currentathlete = 0
        self.competitors = []

    # def addcursor(self):

    def tooltip(self, area=None):
        if self.message:
            if area == "cursor":
                self.message.config(text="Add finish time & cursor")
            elif area == "backward":
                self.message.config(text="Go to the left")
            elif area == "forward":
                self.message.config(text="Go to the right")
            elif area == "plus":
                self.message.config(text="Zoom in")
            elif area == "minus":
                self.message.config(text="Zoom out")
            elif area == "start time":
                self.message.config(text="Select start time on image")
            else:
                self.message.config(text="MY Photo-Finish by METU Athletics")

    def take_canvas_screenshot(self):
        canvas = self.pfcanvas

        ps_data = canvas.postscript(colormode="color", pagewidth=canvas.winfo_reqwidth(),
                                    pageheight=canvas.winfo_reqheight())

        # Create an Image object from the PostScript data
        img = Image.open(io.BytesIO(ps_data.encode("utf-8")))

        # Save the image to a file
        img.save("canvas_screenshot.png", format="PNG")

        print("Canvas screenshot taken and saved.")

    def determine_start_time(self):
        self.start_time_button.config(state=tk.DISABLED)

    def time_scale(self, start, end, ticks):
        duration = end - start
        level = np.round(np.log(duration) / np.log(10))
        increments = 10 ** (level)
        if duration * 10 ** (1 - increments) < 5:
            increments /= 10
            print("a")
        ending = end - end % increments
        starting = start - start % increments + increments
        print(starting, ending, increments, int(level) - 1, duration)
        return np.arange(starting - increments, ending + increments / ticks, increments / ticks), 1 / increments

    def on_mouse_motion(self, event):
        # Update self.mousex and self.mousey
        self.mousex, self.mousey = event.x, event.y
        self.pfcanvas.delete(self.cursorline)
        self.cursorline = self.pfcanvas.create_line(self.mousex, 0, self.mousex, self.pfcanvas.winfo_height(),
                                                    fill="black")

    def on_click(self, event):
        if not self.timeline_image.any():
            return
        time_pixels = ((self.pfcanvas.winfo_width() - event.x)) + (
                    self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1) - self.image_x_max)
        time = (self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1) - time_pixels) / (
                    self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1))
        time = self.start_time - self.record_start + (1 - time) * (self.stop_time - self.start_time)

        if self.start_time_button["state"] == tk.DISABLED:
            self.audiostart = time
            self.start_time_button["state"] = tk.ACTIVE
            self.handle_scroll(0)
            return
        if self.add_cursor["state"] == tk.ACTIVE:
            return
        time -= self.audiostart
        time1 = np.round(time * 100) / 100
        timestr = str(time1)
        if "." not in timestr:
            timestr = timestr + ".0"
        if len(timestr.split(".")[-1]) == 1:
            timestr = timestr + "0"
        self.results.append(time)
        print(self.results)
        self.result_cursors.append([0, 0])
        self.result_cursors[0][0] = self.pfcanvas.create_text(self.mousex, 100, anchor="n", text=timestr + "s",
                                                              fill="red")
        self.result_cursors[0][1] = self.pfcanvas.create_line(self.mousex, 100, self.mousex,
                                                              self.pfcanvas.winfo_height(), fill="black")
        print(time)

    def handle_scroll(self, event, transfer=0):
        if not self.timeline_image.any():
            return
        if event == 0 or event == -1 or event == 1:
            delta = event
            self.zoom_level += delta
            if self.zoom_level == 0:
                self.zoom_level = 1
        else:
            delta = event.delta
        if self.mousey < 100:
            if delta > 0:
                self.audiozoomlevel += 1
            elif delta < 0:
                self.audiozoomlevel -= 1
        else:
            previous_zoom = self.zoom_level
            mouse_image_addition = self.mousex / self.pfcanvas.winfo_width() - 0.5
            if delta > 0 and self.zoom_level < self.maxzoom:
                self.zoom_level += 1
                self.image_middle += mouse_image_addition * 2 ** (1 - previous_zoom)
                if self.image_middle > 1 - 0.5 / 2 ** (self.zoom_level - 1):
                    self.image_middle = 1 - 0.5 / 2 ** (self.zoom_level - 1) - 0.0001
                    print("a")
                elif self.image_middle < 0.5 / 2 ** (self.zoom_level - 1):
                    self.image_middle = 0.5 / 2 ** (self.zoom_level - 1) + 0.0001
                    print("b")


            elif delta < 0 and self.zoom_level > 1:
                self.zoom_level -= 1
                self.image_middle -= mouse_image_addition * 2 ** (1 - previous_zoom)
                if self.zoom_level == 1:
                    self.image_middle = 0.5
                    return
                if self.image_middle > 1 - 0.5 / 2 ** (self.zoom_level - 1):
                    self.image_middle = 1 - 0.5 / 2 ** (self.zoom_level - 1) - 0.0001
                    print("c")
                elif self.image_middle < 0.5 / 2 ** (self.zoom_level - 1):
                    self.image_middle = 0.5 / 2 ** (self.zoom_level - 1) + 0.0001
                    print("d")

        if transfer == 1:
            print("transfer right")
            self.image_middle += 0.2 * 2 ** (1 - self.zoom_level)
        if transfer == -1:
            print("transfer left")
            self.image_middle -= 0.2 * 2 ** (1 - self.zoom_level)
        if self.image_middle < 0.5 * 2 ** (1 - self.zoom_level):
            self.image_middle = 0.5 * 2 ** (1 - self.zoom_level)
        if self.image_middle > 1 - 0.5 * 2 ** (1 - self.zoom_level):
            self.image_middle = 1 - 0.5 * 2 ** (1 - self.zoom_level)

        self.zoom_label.config(text="| Zoom: x" + str(2 ** (self.zoom_level - 1)))

        self.image_x_min = self.pfcanvas.winfo_width() * 2 ** (
                self.zoom_level - 1) * self.image_middle - self.pfcanvas.winfo_width() * 0.5
        self.image_x_max = self.pfcanvas.winfo_width() * 2 ** (
                self.zoom_level - 1) * self.image_middle + self.pfcanvas.winfo_width() * 0.5

        if len(self.zoomed_images) < self.zoom_level:
            canvas_width = self.pfcanvas.winfo_width()
            canvas_height = self.pfcanvas.winfo_height()
            zoomed_image = cv2.resize(self.timeline_image,
                                      (canvas_width * 2 ** (self.zoom_level - 1), canvas_height - 50 - 100))
            self.zoomed_images.append(zoomed_image)

        self.pfcanvas.delete("all")

        start = self.record_start - self.start_time
        end = self.stop_time - self.start_time
        duration = (end - start)
        print("start & end: ", start, end)

        print("xmax:", self.image_x_max, "xmin:", self.image_x_min, "totalx:",
              self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1))

        zoomed_start = duration * ((self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1)) - self.image_x_max) / (
                    self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1)) + start
        zoomed_end = duration * ((self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1)) - self.image_x_min) / (
                    self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1)) + start

        print("zoomed start & end: ", zoomed_start, zoomed_end)
        scale, dummy1 = self.time_scale(zoomed_start - self.audiostart, zoomed_end - self.audiostart, 5)
        scale_positions = self.pfcanvas.winfo_width() * (
                    1 - (scale - zoomed_start + self.audiostart) / duration * 2 ** (self.zoom_level - 1))

        scale_texts, self.carp = self.time_scale(zoomed_start - self.audiostart, zoomed_end - self.audiostart, 1)
        scale_texts = np.round(self.carp * scale_texts) / self.carp
        scale_text_positions = self.pfcanvas.winfo_width() * (
                    1 - (scale_texts - zoomed_start + self.audiostart) / duration * 2 ** (self.zoom_level - 1))

        if self.audiodata.any():
            audiolist = self.audiodata[int(zoomed_start * self.audiosamplerate):int(zoomed_end * self.audiosamplerate)]
            for i in range(len(audiolist) - 1):
                X1 = self.pfcanvas.winfo_width() * (1 - i / ((zoomed_end - zoomed_start) * self.audiosamplerate))
                Y1 = 50 * (1 - audiolist[i] * 2 ** self.audiozoomlevel)
                X2 = self.pfcanvas.winfo_width() * (1 - (i + 1) / ((zoomed_end - zoomed_start) * self.audiosamplerate))
                Y2 = 50 * (1 - audiolist[i + 1] * 2 ** self.audiozoomlevel)
                self.pfcanvas.create_line(int(X1), int(Y1), int(X2), int(Y2), fill="white")

        self.pfcanvas.image = self.zoomed_images[self.zoom_level - 1][0:int(self.pfcanvas.winfo_height()),
                              int(self.image_x_min):int(self.image_x_max)]
        self.img_tk = ImageTk.PhotoImage(image=Image.fromarray(self.pfcanvas.image))

        print("IMAGE CREATE")
        self.pfcanvas.create_image(0, 100, anchor=tk.NW, image=self.img_tk)

        if self.ticklines:
            for i in self.ticklines:
                self.pfcanvas.delete(i)

        for i in scale_positions:
            self.pfcanvas.create_line(i, self.pfcanvas.winfo_height() - 50 + 10, i,
                                      self.pfcanvas.winfo_height() - 50, fill="white")

        for i in range(len(scale_text_positions)):
            self.pfcanvas.create_text(scale_text_positions[i], self.pfcanvas.winfo_height(),
                                      text=str(scale_texts[i])[:5] + "s", anchor="s", fill="white")
            self.pfcanvas.create_line(scale_text_positions[i], self.pfcanvas.winfo_height() - 25,
                                      scale_text_positions[i],
                                      self.pfcanvas.winfo_height() - 50, fill="white")

        for i in range(len(self.results)):
            X = self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1) * (
                        self.results[i] + self.audiostart - (self.record_start - self.start_time)) / (
                            self.stop_time - self.record_start) - (
                            self.pfcanvas.winfo_width() * 2 ** (self.zoom_level - 1) - self.image_x_max)
            print(X)
            X = self.pfcanvas.winfo_width() - X

            time1 = np.round(self.results[i] * 100) / 100
            timestr = str(time1)
            if "." not in timestr:
                timestr = timestr + ".0"
            if len(timestr.split(".")[-1]) == 1:
                timestr = timestr + "0"

            Y = 100 + (self.pfcanvas.winfo_height() - 150) / len(self.results) + (
                        self.pfcanvas.winfo_height() - 150 - 2 * (self.pfcanvas.winfo_height() - 150) / len(
                    self.results)) * i / len(self.results)

            self.result_cursors[i][1] = self.pfcanvas.create_line(X, 100, X, self.pfcanvas.winfo_height(), fill="black")
            self.result_cursors[i][0] = self.pfcanvas.create_text(X, Y, anchor="n", text=timestr + "s", fill="red")

        print("zoom level: ", self.zoom_level)
        print("middle: ", self.image_middle)

    def result(self):
        if self.results_on == 1:
            return
        self.results_on = 1
        result_window = tk.Toplevel(self.root)
        result_window.title("Athletes & Results")
        result_window.wm_iconphoto(False, resultpic)
        result_window.geometry("800x250")
        result_window.resizable(False, True)

        def onclose():
            self.results_on = 0
            result_window.destroy()

        result_window.protocol("WM_DELETE_WINDOW", onclose)
        self.resultlabels = []

        def edit_athlete():
            print(no)
            no = self.currentathlete
            print(self.resultlabels)
            if str(self.resultlabels[no][-2].cget("image")) == str(editpic):
                self.resultlabels[no][-2].configure(image=okpic)
                for j in range(len(self.resultlabels[no]) - 2):
                    self.resultlabels[no][j].config(state="normal")
                return
            if str(self.resultlabels[no][-2].cget("image")) == str(okpic):
                self.resultlabels[no][-2].configure(image=editpic)
                print(self.athletes[no])
                for j in range(len(self.resultlabels[no]) - 2):
                    self.resultlabels[no][j].config(state="readonly")
                    self.athletes[no][self.athlete_properties[j]] = str(self.resultlabels[no][j].get())
                print(self.athletes[no])

        def delete_athlete():
            no = self.currentathlete
            del self.athletes[no]
            for i in range(len(self.resultlabels[no])):
                self.resultlabels[no][i].destroy()
            display_results()

        def add_athlete():
            new_athlete = {}
            for i in self.default_athlete.keys():
                new_athlete[i] = self.athletes[i]
            self.athletes.append(new_athlete)
            for i in range(len(self.resultlabels)):
                for j in range(len(self.resultlabels[0])):
                    self.resultlabels[i][j].destroy()
            self.add_athlete_button.place(x=400, y=20 + len(self.athletes) * 20 + 20, anchor="n")
            print("before add athlete's call:", self.resultlabels)
            result_window.destroy()
            self.result()
            print("after add athlete's call:", self.resultlabels)
            print(self.athletes)

        def display_results():
            for i in range(len(self.athletes)):
                global globals
                ()[f'athlete{i}lane']
                globals()[f'athlete{i}lane'].destroy()

                global globals
                ()[f'athlete{i}id']
                globals()[f'athlete{i}id'].destroy()

                global globals
                ()[f'athlete{i}name']
                globals()[f'athlete{i}name'].destroy()

                global globals
                ()[f'athlete{i}affiliation']
                globals()[f'athlete{i}affiliation'].destroy()

                global globals
                ()[f'athlete{i}license']
                globals()[f'athlete{i}license'].destroy()

                global globals
                ()[f'athlete{i}time']
                globals()[f'athlete{i}time'].destroy()

                global globals
                ()[f'athlete{i}place']
                globals()[f'athlete{i}place'].destroy()

                global globals
                ()[f'athlete{i}edit']
                globals()[f'athlete{i}edit'].destroy()

                global globals
                ()[f'athlete{i}delete']
                globals()[f'athlete{i}delete'].destroy()

            tk.Label(result_window, text="Lane").place(x=0, y=0, anchor="nw")
            tk.Label(result_window, text="ID").place(x=3 + 25, y=0, anchor="nw")
            tk.Label(result_window, text="Full Name").place(x=3 + 70, y=0, anchor="nw")
            tk.Label(result_window, text="Affiliation").place(x=3 + 310, y=0, anchor="nw")
            tk.Label(result_window, text="License").place(x=3 + 550, y=0, anchor="nw")
            tk.Label(result_window, text="Time").place(x=3 + 650, y=0, anchor="nw")
            tk.Label(result_window, text="Place").place(x=3 + 710, y=0, anchor="nw")
            for i in range(len(self.athletes)):
                """
                time1 = np.round(i * 100) / 100
                timestr = str(time1)

                if "." not in timestr:
                    timestr = timestr + ".0"
                if len(timestr.split(".")[-1]) == 1:
                    timestr = timestr + "0"
                """
                global globals
                ()[f'athlete{i}lane']
                globals()[f'athlete{i}lane'] = tk.Entry(result_window, width=5)
                globals()[f'athlete{i}lane'].insert(0, self.athletes[i]["lane"])
                globals()[f'athlete{i}lane'].place(x=3 + 0, y=20 + i * 20, anchor="nw")
                globals()[f'athlete{i}lane'].config(state="readonly")

                global globals
                ()[f'athlete{i}id']
                globals()[f'athlete{i}id'] = tk.Entry(result_window, width=8)
                globals()[f'athlete{i}id'].insert(0, self.athletes[i]["id"])
                globals()[f'athlete{i}id'].place(x=6 + 25, y=20 + i * 20, anchor="nw")
                globals()[f'athlete{i}id'].config(state="readonly")

                global globals
                ()[f'athlete{i}name']
                globals()[f'athlete{i}name'] = tk.Entry(result_window, width=40)
                globals()[f'athlete{i}name'].insert(0, self.athletes[i]["name"])
                globals()[f'athlete{i}name'].place(x=6 + 70, y=20 + i * 20, anchor="nw")
                globals()[f'athlete{i}name'].config(state="readonly")

                global globals
                ()[f'athlete{i}affiliation']
                globals()[f'athlete{i}affiliation'] = tk.Entry(result_window, width=40)
                globals()[f'athlete{i}affiliation'].insert(0, self.athletes[i]["affiliation"])
                globals()[f'athlete{i}affiliation'].place(x=6 + 310, y=20 + i * 20)
                globals()[f'athlete{i}affiliation'].config(state="readonly")

                global globals
                ()[f'athlete{i}license']
                globals()[f'athlete{i}license'] = tk.Entry(result_window, width=30)
                globals()[f'athlete{i}license'].insert(0, self.athletes[i]["license"])
                globals()[f'athlete{i}license'].place(x=6 + 550, y=20 + i * 20)
                globals()[f'athlete{i}license'].config(state="readonly")

                global globals
                ()[f'athlete{i}time']
                globals()[f'athlete{i}time'] = tk.Entry(result_window, width=10)
                globals()[f'athlete{i}time'].insert(0, self.athletes[i]["time"])
                globals()[f'athlete{i}time'].place(x=6 + 650, y=20 + i * 20)
                globals()[f'athlete{i}time'].config(state="readonly")

                global globals
                ()[f'athlete{i}place']
                globals()[f'athlete{i}place'] = tk.Entry(result_window, width=4)
                globals()[f'athlete{i}place'].insert(0, self.athletes[i]["place"])
                globals()[f'athlete{i}place'].place(x=6 + 710, y=20 + i * 20)
                globals()[f'athlete{i}place'].config(state="readonly")
                self.currentathlete = i

                global globals
                ()[f'athlete{i}edit']
                globals()[f'athlete{i}edit'] = tk.Button(result_window, image=editpic, command=edit_athlete)
                globals()[f'athlete{i}edit'].place(x=6 + 740, y=20 + i * 20, width=20, height=20)

                global globals
                ()[f'athlete{i}delete']
                globals()[f'athlete{i}delete'] = tk.Button(result_window, image=crosspic, command=delete_athlete)
                globals()[f'athlete{i}delete'].place(x=6 + 760, y=20 + i * 20, width=20, height=20)

            self.add_athlete_button = tk.Button(result_window, text="Add Athlete", command=add_athlete)
            self.add_athlete_button.place(x=400, y=20 + len(self.athletes) * 20 + 20, anchor="n")

        display_results()

        def undo():
            del self.results[-1]
            self.resultlabels[-1].destroy()
            del self.resultlabels[-1]
            self.pfcanvas.delete(self.result_cursors[-1][0])
            self.pfcanvas.delete(self.result_cursors[-1][1])

        # undo_button = tk.Button(result_window,text= "Clear", command = undo)
        # undo_button.pack()

        result_window.mainloop()

    def on_closing1(self):
        try:
            if self.audio_stream1:
                self.audio_stream1.stop()
            if self.canvas and self.oval:
                self.canvas.delete(self.oval)
        except:
            pass
        self.settings.destroy()
        self.options_on = 0

    def options(self):
        if self.options_on == 1:
            return
        self.options_on = 1
        self.settings = tk.Toplevel(self.root)
        self.settings.title("Options")
        self.settings.geometry("270x400")
        self.settings.wm_iconphoto(False, iconopt)
        self.settings.resizable(False, False)

        self.settings.protocol("WM_DELETE_WINDOW", self.on_closing1)
        self.canvas = tk.Canvas(self.settings, width=270, height=400, bg="#f0f0f0")
        self.canvas.pack()

        soundvalues = [str(i[0]) + " - " + i[1] + " " + str(i[2]) for i in thesounddevices]

        sound_device_label = tk.Label(self.settings, text="Sound Input Device:")
        sound_device_label.place(x=135, y=17, anchor="n")

        sound_device = ttk.Combobox(self.settings, values=soundvalues, width=38, state="readonly")
        sound_device.set(soundvalues[self.sound_device_index])
        sound_device.place(x=135, y=38, anchor="n")

        camera_device_label = tk.Label(self.settings, text="Capture Device Index (0 for default):")
        camera_device_label.place(x=10, y=90, anchor="w")

        camera_device = tk.Entry(self.settings, width=5)
        camera_device.place(x=260, y=90, anchor="e")
        camera_device.insert(0, str(self.camera_index))

        align_camera_button = tk.Button(self.settings, text="Align Camera", font=("Arial", 14),
                                        command=self.align_camera)
        align_camera_button.place(x=135, y=15 + 100, anchor="n")

        micline = self.canvas.create_line(35, 215, 235, 215)

        def test_mic():
            if test_mic_button['text'] == "Test Audio Input":

                self.x = 35
                self.xmax = 35
                self.oval = self.canvas.create_oval(self.x - 2, 215 - 2, self.x + 2, 215 + 2, fill="red")
                self.maxoval = self.canvas.create_oval(self.x - 2, 215 - 2, self.x + 2, 215 + 2, fill="red")

                def audio_callback(indata, frames, time, status):
                    volume_norm = np.linalg.norm(indata) * 10 / self.maxvolume
                    print(volume_norm)
                    if self.canvas and hasattr(self, 'oval'):
                        self.canvas.delete(self.oval)
                        try:
                            if self.x > self.xmax:
                                self.xmax = self.x
                            self.x = 35 + 200 * volume_norm
                            self.oval = self.canvas.create_oval(self.x - 2, 215 - 2, self.x + 2, 215 + 2, fill="red")
                            self.canvas.delete(self.maxoval)
                            self.maxoval = self.canvas.create_oval(self.xmax - 2, 215 - 2, self.xmax + 2, 215 + 2,
                                                                   fill="blue")
                            print((self.xmax - 35) / 200)
                        except:
                            pass

                self.audio_stream1 = sd.InputStream(callback=audio_callback, channels=1,
                                                    samplerate=self.sample_rate, device=self.sound_device_index)
                self.audio_stream1.start()
                test_mic_button.config(text="Stop Test")
            elif test_mic_button['text'] == "Stop Test":
                self.audio_stream1.stop()
                self.canvas.delete(self.maxoval)
                self.canvas.delete(self.oval)
                test_mic_button.config(text="Test Audio Input")
                if self.canvas and self.oval:
                    self.canvas.delete(self.oval)

        test_mic_button = tk.Button(self.settings, text="Test Audio Input", command=test_mic)
        test_mic_button.place(x=135, y=180, anchor="n")

        slider = ttk.Scale(self.settings, from_=0.0, to=1, variable=self.threshold_var, orient=tk.HORIZONTAL,
                           length=200, command=self.update_slider)
        slider.place(x=135, y=230, anchor="n")

        self.value_label = tk.Label(self.settings, text=f"Microphone Threshold: {self.threshold_var.get():.2f}")
        self.value_label.place(x=135, y=260, anchor="n")

        frame_width_label = tk.Label(self.settings, text="Frame Width (pixels): ")
        frame_width_label.place(x=92, y=289, anchor="n")

        def change_fr_width():
            self.line_thickness = int(frame_width_entry.get())

        frame_width_entry = tk.Entry(self.settings, width=10)
        frame_width_entry.place(x=192, y=290, anchor="n")
        frame_width_entry.insert(0, str(self.line_thickness))

        time_offset_label = tk.Label(self.settings, text="Time Offset (seconds):")
        time_offset_label.place(x=92, y=310, anchor="n")

        time_offset_entry = tk.Entry(self.settings, width=10)
        time_offset_entry.place(x=192, y=311, anchor="n")
        time_offset_entry.insert(0, str(self.time_offset))

        def change_sound_device():
            self.sound_device_index = int(str(sound_device.get().split()[0]))
            self.sample_rate = thesounddevices[self.sound_device_index][2]
            self.sample_rate = float(self.sample_rate)

        def is_camera_available(index):
            cap = cv2.VideoCapture(index)
            available = cap.isOpened()
            cap.release()
            return available

        def save_options():
            change_fr_width()
            change_sound_device()
            if is_camera_available(int(camera_device.get())) == True:
                self.camera_index = int(camera_device.get())
                self.cap = cv2.VideoCapture(self.camera_index)

            else:
                tk.messagebox.showerror(title="Invalid Device Index",
                                        message="There is no capture device with index " + camera_device.get() + "!")
                camera_device.delete(0, tk.END)
                camera_device.insert(0, str(self.camera_index))
            self.time_offset = float(time_offset_entry.get())

        save_button = tk.Button(self.settings, text="Ok", command=save_options)

        save_button.place(x=135, y=350, anchor="n")

    def update_slider(self, value):
        self.threshold_var.set(value)
        self.threshold = float(value)

        self.value_label.config(text=f"Threshold: {float(value):.2f}")

        print(self.threshold)

    def align_camera(self):
        # Open a new window for camera display
        align_window = tk.Toplevel(self.root)
        align_window.title("Align Camera")
        align_window.wm_iconphoto(False, iconbg)

        def closecam():
            self.cap.release()
            align_window.destroy()

        align_window.protocol("WM_DELETE_WINDOW", closecam)

        align_label_widget = tk.Label(align_window)
        align_label_widget.pack()

        def on_closing_align():
            self.cap.release()
            align_window.destroy()

        def open_aligned_camera():
            _, frame = self.cap.read()

            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            line_thickness = 1
            spacing = self.line_thickness + 2
            frame_height, frame_width, _ = frame.shape
            middle_x = frame_width // 2
            line1_x = middle_x - spacing - line_thickness // 2
            line2_x = middle_x + spacing + line_thickness // 2

            frame[:, line1_x:line1_x + line_thickness, :] = [0, 0, 255]
            frame[:, line2_x:line2_x + line_thickness, :] = [0, 0, 255]

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            align_label_widget.photo_image = photo_image
            align_label_widget.configure(image=photo_image)
            align_label_widget.after(10, open_aligned_camera)  # Update every 10 milliseconds

        open_aligned_camera()  # Start the update loop
        align_window.mainloop()

        if self.recording:
            self.stop_recording()
        if self.audio_stream:
            self.audio_stream.stop()
        self.root.destroy()

    def start_recording(self):
        self.start_time = time.time()
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.create_timeline_button.config(state=tk.DISABLED)

        self.recording = True
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), self.fps, (640, 480))

        self.record_start = time.time()

    def stop_recording(self):
        return

    def save_video(self):
        return

    def save_image(self):
        ps_data = self.pfcanvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps_data.encode('utf-8')))
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img.save(file_path, format='png')

    def create_timeline(self):

        self.zoom_level = 1
        self.image_middle = 0.5
        # self.out.release()

        self.message.config(text="Creating Photo-Finish image...")
        video_file = filedialog.askopenfilename()
        cap_timeline = cv2.VideoCapture(video_file)
        fps = cap_timeline.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap_timeline.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        print(duration)

        clip = VideoFileClip(video_file)

        # Extract audio data as a NumPy array
        audio = clip.audio

        audio.write_audiofile("temporary.wav")

        self.audiodata, self.audiosamplerate = sf.read("temporary.wav")
        self.stop_time = len(self.audiodata) / self.audiosamplerate
        self.audiodata = self.audiodata[:, 1][::40]
        self.audiosamplerate /= 40
        self.start_time = 0
        self.record_start = 0
        self.stop_time = len(self.audiodata) / self.audiosamplerate
        if self.create_timeline_button['text'] == "Import Video":
            frames = []
            timestamps = []
            while True:
                ret, frame = cap_timeline.read()

                if not ret:
                    break

                frame_height, frame_width, _ = frame.shape
                start_y = 0
                end_y = frame_height
                middle_x = frame_width // 2
                start_x = middle_x - (self.line_thickness + 1) // 2
                end_x = middle_x + (self.line_thickness + 1) // 2
                middle_line_part = frame[start_y:end_y, start_x:end_x]

                frames.append(middle_line_part)
                timestamps.append(time.time() - self.start_time)
            timeline_image = cv2.hconcat(frames)
            cap_timeline.release()
            timeline_image = cv2.cvtColor(timeline_image, cv2.COLOR_RGB2BGR)
            self.timeline_image = cv2.flip(timeline_image, 1)

        # self.create_timeline_button.config(text="Update Picture")
        print(self.timeline_image)

        canvas_width = self.pfcanvas.winfo_width()
        canvas_height = self.pfcanvas.winfo_height()

        self.zoomed_images = []
        self.zoomed_images.append(cv2.resize(self.timeline_image, (canvas_width, canvas_height - 50 - 100
        image = self.zoomed_images[0]  # Resize the image if needed
        # Convert the NumPy array to a Pillow Image and specify the mode
        # img_tk = ImageTk.PhotoImage(image=Image.fromarray(image.astype('uint8'), mode='RGB'))
        # self.pfcanvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        # self.pfcanvas.image = img_tk
        self.message.config(text="Photo-Finish image created.")
        cap_timeline.release()
        self.handle_scroll(0)
        self.cap = cv2.VideoCapture(0)

    def audio_callback(self, indata, frames, time, status, ):
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > self.threshold * self.maxvolume and not self.recording:
            self.start_recording()
            self.update_video()
            print("Start sound detected. Recording & timing.")
            self.message.config(text="Start sound detected. Recording & timing.")

    def listen_start_gun(self):

        self.timer.config(text="00:00:000")
        # Initialize audio stream for listening to the start gun
        self.audio_stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.sample_rate,
                                           device=self.sound_device_index)
        self.audio_stream.start()
        print("Listening to the start gun...")
        self.message.config(text="Waiting for the start signal...")


root = tk.Tk()
root.title("MY Photo-Finish")
opticon = Image.open('images/options.ico')
iconopt = ImageTk.PhotoImage(opticon)
icon = Image.open('images/icon.ico')
iconbg = ImageTk.PhotoImage(icon)
resultico = Image.open('images/results.ico')
resultpic = ImageTk.PhotoImage(resultico)
backwardico = Image.open('images/backward.ico')
backwardpic = ImageTk.PhotoImage(backwardico)
forwardico = Image.open('images/forward.ico')
forwardpic = ImageTk.PhotoImage(forwardico)
addcursorico = Image.open('images/add_cursor.ico')
addcursorpic = ImageTk.PhotoImage(addcursorico)
plusico = Image.open('images/plus.ico')
pluspic = ImageTk.PhotoImage(plusico)
minusico = Image.open('images/minus.ico')
minuspic = ImageTk.PhotoImage(minusico)
startico = Image.open('images/start.ico')
startpic = ImageTk.PhotoImage(startico)

editico = Image.open('images/edit.ico').resize((20, 20))
editpic = ImageTk.PhotoImage(editico)

crossico = Image.open('images/cross.ico').resize((20, 20))
crosspic = ImageTk.PhotoImage(crossico)

okico = Image.open('images/ok.ico').resize((20, 20))
okpic = ImageTk.PhotoImage(okico)

root.wm_iconphoto(False, iconbg)
root.state("zoomed")
root.resizable(True, True)
video_recorder = VideoRecorder(root)
root.mainloop()

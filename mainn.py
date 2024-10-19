# pyinstaller main.py --onefile --name "MY Photo-Finish" --icon "images/main.jpg"

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
import soundfile as sf
from PIL import Image, ImageGrab
from tkinter.filedialog import asksaveasfile
import pandas as pd
import pyautogui
import openpyxl
from functools import partial
import librosa
import noisereduce as nr


result_times = []

sounddevices = []
index_sound = 0



class VideoRecorder:
    def __init__(self, root):
        self.mousex = 0
        self.mousey = 0
        self.root = tk.Toplevel(root)
        self.root.title("MY Photo-Finish")
        self.root.wm_iconphoto(False, iconbg)
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.out = None
        self.recording = False
        self.start_time = 0
        self.soundlevel = 0
        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.default_athlete = {"lane":"NA","id":"NA","name":"NA","affiliation":"NA","license":"NA","time":"NA","place": "NA","priv_id":1}
        self.athletes = []
        self.athlete_properties = ("lane","id","name","affiliation","license","time","place")
        self.private_id = 0

        self.time_offset = 0

        self.maxvolume = 300

        self.message = 0

        button_frame = tk.Frame(self.root)
        button_frame.pack(anchor= tk.NW)

        self.add_cursor = tk.Button(button_frame,image = addcursorpic, command = self.addcursor)
        self.add_cursor.pack(side=tk.LEFT)
        self.add_cursor.bind("<Enter>", lambda event: self.tooltip(area = "cursor"))
        self.add_cursor.bind("<Leave>", self.tooltip)
        self.add_cursor.config(state ="normal")

        self.finish_add_cursor = tk.Button(button_frame,image = addcursorokpic, command = self.addcursorok)
        self.finish_add_cursor.pack(side=tk.LEFT)
        self.finish_add_cursor.bind("<Enter>", lambda event: self.tooltip(area="endcursor"))
        self.finish_add_cursor.bind("<Leave>", self.tooltip)
        self.finish_add_cursor.config(state="disabled")

        self.backward = tk.Button(button_frame, image=backwardpic, command = lambda :self.handle_scroll(event = 0, transfer = -1))
        self.backward.pack(side=tk.LEFT)
        self.backward.bind("<Enter>", lambda event: self.tooltip(area="backward"))
        self.backward.bind("<Leave>", self.tooltip)
        self.forward = tk.Button(button_frame, image=forwardpic, command = lambda :self.handle_scroll(event = 0, transfer = 1))
        self.forward.pack(side=tk.LEFT)
        self.forward.bind("<Enter>", lambda event: self.tooltip(area="forward"))
        self.forward.bind("<Leave>", self.tooltip)
        self.plus = tk.Button(button_frame, image=pluspic, command = lambda :self.handle_scroll(1))
        self.plus.pack(side=tk.LEFT)
        self.plus.bind("<Enter>", lambda event: self.tooltip(area="plus"))
        self.plus.bind("<Leave>", self.tooltip)
        self.minus = tk.Button(button_frame, image=minuspic, command = lambda :self.handle_scroll(-1))
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

        self.canvas_or_height = self.pfcanvas.winfo_height()
        self.canvas_or_width = self.pfcanvas.winfo_width()
        print("height:",self.canvas_or_height,"width:",self.canvas_or_width)

        self.pfcanvas.bind("<MouseWheel>", self.handle_scroll)
        self.pfcanvas.bind("<Button-1>", self.on_click)
        self.pfcanvas.bind("<Motion>", self.on_mouse_motion)

        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        import_menu = tk.Menu(file_menu, tearoff=False)
        file_menu.add_cascade(label="Import", menu=import_menu)
        import_menu.add_command(label="Video", command=self.create_timeline)
        import_menu.add_command(label="Heat", command=self.import_heat)

        export_menu = tk.Menu(file_menu, tearoff=False)
        file_menu.add_cascade(label="Export", menu=export_menu)
        export_menu.add_command(label="Photo-Finish Image", command = self.take_canvas_screenshot)
        export_menu.add_command(label="Results Table", command = self.export_results_table)
        #file_menu.add_command(label="Export", command=self.take_canvas_screenshot)
        file_menu.add_separator()
        file_menu.add_command(label="Athletes & Results", command=self.result)
        file_menu.add_separator()
        file_menu.add_command(label="Options", command=self.options)
        file_menu.add_command(label="Exit", command=self.root.destroy)
        self.root.config(menu=menu_bar)


        self.cursorline = self.pfcanvas.create_line(self.pfcanvas.winfo_width()/2, 0, self.pfcanvas.winfo_width()/2, self.pfcanvas.winfo_height(),
                                                    fill="black")

        self.button_height = 100

        self.infolabel = tk.Label(self.root,text = "i",font=("elephant", 10, "italic"),foreground= '#0000FF')
        self.infolabel.pack(side=tk.LEFT, anchor=tk.S)
        self.message = tk.Label(self.root, text="MY Photo-Finish by METU Athletics", font=("Arial", 10))
        self.message.pack(side=tk.LEFT, anchor=tk.S)
        self.zoom_label = tk.Label(self.root, text="| Zoom Level: x1", font=("Arial", 10), )
        self.zoom_label.pack(side=tk.LEFT, anchor=tk.S)
        self.threshold = 0.5
        self.threshold_var = tk.DoubleVar(value=self.threshold)

        self.canvas = None

        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Threshold for audio detection
        self.results = []
        self.results_formatted = []
        self.result_cursors = []
        self.sound_device_index = 1

        self.audio_stream = None
        self.line_thickness = 15

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
        self.direction = "LR"
        self.dummy = 0
        self.canvas_or_width = self.root.winfo_width()

        self.image_s = 0
    def addcursor(self):
        if self.add_cursor["state"] == "normal":
            self.add_cursor.config(state = "disabled")
            self.finish_add_cursor.config(state="normal")

    def addcursorok(self):
        if self.add_cursor["state"] == "disabled":
            self.add_cursor.config(state = "normal")
            self.finish_add_cursor.config(state="disabled")
        for i in range(len(self.resultlabels)):
            self.resultlabels[i][5].config(values = self.results_formatted)

    def tooltip(self,area = None):
        if self.message:
            if area == "cursor":
                self.message.config(text = "Add finish time & cursor")
            elif area == "endcursor":
                self.message.config(text = "Save finish times")
            elif area == "backward":
                self.message.config(text= "Go to the left")
            elif area == "forward":
                self.message.config(text= "Go to the right")
            elif area == "plus":
                self.message.config(text= "Zoom in")
            elif area == "minus":
                self.message.config(text="Zoom out")
            elif area == "start time":
                self.message.config(text="Calibrate time")
            else:
                self.message.config(text = "MY Photo-Finish by METU Athletics")
    def take_canvas_screenshot(self,mode = 0):
        import mss
        from PIL import Image
        import pygetwindow as gw

        # Initialize the MSS screenshot object
        with mss.mss() as sct:
            # Get information about all monitors
            monitors = sct.monitors

            # Capture screenshots of all monitors
            screenshots = []
            for monitor in monitors:
                try:
                    screenshot = sct.grab(monitor)
                    screenshot_pil = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                    screenshots.append(screenshot_pil)
                except Exception as e:
                    print(f"Error capturing screenshot: {e}")

        # Combine the screenshots into a single image
        combined_width = sum(monitor["width"] for monitor in monitors)
        max_height = max(monitor["height"] for monitor in monitors)
        combined_image = Image.new("RGB", (combined_width, max_height))

        # Paste each screenshot into the combined image
        offset = 0
        for screenshot in screenshots:
            region_size = screenshot.size
            combined_image.paste(screenshot, (offset, 0, offset + region_size[0], region_size[1]))
            offset += screenshot.width

        # Save the combined screenshot
        window_title = "MY Photo-Finish"
        if mode == 1:
            window_title = "Athletes & Results"
        # Find the window by its title
        window = gw.getWindowsWithTitle(window_title)

        # Check if the window was found
        if window:
            window_left = window[0].left
            window_top = window[0].top
            window_width = window[0].width
            window_height = window[0].height
        if mode == 1:
            window_width =  self.result_window.winfo_width()
            window_height = self.result_window.winfo_height()


        if mode == 0:
            if self.image_s == 0:
                aa,bb,cc,dd = 8,130,8,113
            elif self.image_s == 1:
                aa, bb, cc, dd = 10, 130, 926, 483
        elif mode == 1:
            aa,bb,cc,dd = 0,0,0,0

        final_ss = screenshots[0].crop((window_left+aa,window_top+bb,window_left+window_width-cc,window_top+window_height-dd))
        final_ss.save("combined_screenshot.png")
        ppimg = Image.open("combined_screenshot.png")
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))

        # Check if a file path was selected
        if file_path:
            # Save the image to the specified file path
            ppimg.save(file_path)
            print("Image saved successfully.")
        else:
            print("No file path selected.")
        print("Canvas screenshot taken and saved.")

    def export_results_table(self):
        def as_txt():
            results_text_file = asksaveasfile(defaultextension = "*.txt",filetypes=[("Text Documents", "*.txt"),("All Files", "*.*")])
            results_text_file.write("Lane\tID\tFull-Name\tAffiliation\tLicense\tTime\tPlace\n")
            for i in self.resultlabels:
                for j in range(7):
                    results_text_file.write(i[j].get()+"\t")
                results_text_file.write("\n")
            return
        def as_xlsx():
            allresults = []
            for i in self.resultlabels:
                allresults.append([])
                for j in range(7):
                    allresults[-1].append(i[j].get())
            df = pd.DataFrame(allresults,columns = ["Lane","ID","Full-Name","Affiliation","License","Time","Place"])
            results_ex_file = asksaveasfile(defaultextension = "*.xlsx",filetypes=[("Text Documents", "*.xlsx"),("All Files", "*.*")])
            df.to_excel(results_ex_file.name, sheet_name = "Results", index=False)
            return

        def as_photo():
            if self.results_on == 1:
                self.result_window.deiconify()
                self.results_on = 2
            time.sleep(2)
            self.take_canvas_screenshot(mode = 1)
            return

        def onclose():
            self.export_window.destroy()

        self.export_window = tk.Toplevel(self.root)
        self.export_window .title("Export Results...")
        self.export_window.wm_iconphoto(False, resultpic)
        self.export_window.geometry("270x70")
        self.export_window.resizable(False, False)
        self.export_window.protocol("WM_DELETE_WINDOW", onclose)

        exportresults = tk.Label(self.export_window,text="Export results as: ")
        exportresults.place(x=5,y = 5)
        exporttype = ttk.Combobox(self.export_window,state = "readonly",values=["Excel file (*.xlsx)","Text file (*.txt)","Image file (*.png)"],width = 16)
        exporttype.set("Excel file (*.xlsx)")
        exporttype.place(x = 120, y = 5)

        def export_ok():
            if exporttype.get() == "Excel file (*.xlsx)":
                as_xlsx()
            elif exporttype.get() == "Text file (*.txt)":
                as_txt()
            elif exporttype.get() == "Image file (*.png)":
                if self.results_on == 1:
                    self.result_window.deiconify()
                    self.results_on = 2
                self.take_canvas_screenshot(mode = 1)
            else:
                print("no save type detected",exporttype.get())
            self.export_window.destroy()
            return
        exportok = tk.Button(self.export_window,text="Export",command = export_ok)
        exportok.place ( x = 100, y = 40)

        return



    def import_heat(self):
        file = filedialog.askopenfilename()
        if file.split(".")[-1] == "xlsx":
            dataframe = openpyxl.load_workbook(file)
            dataframe1 = dataframe.active

            import_heat_w = tk.Toplevel(self.root)
            import_heat_w.wm_iconphoto(True, iconbg)
            import_heat_w.wm_title("Import Heat...")

            columns = []
            for col in range(1, dataframe1.max_column+1):
                tk.Label(import_heat_w, text="Column "+str(col)+":").pack()
                globals()[f'col{col}'] =  ttk.Combobox(import_heat_w,values = ["lane","id","name","affiliation","license","time","place"],state="readonly", width = 9)
                globals()[f'col{col}'].set("NA")
                globals()[f'col{col}'].pack()
                columns.append(globals()[f'col{col}'])



            def done_with_heat():
                df = pd.read_excel(file)

                # Convert DataFrame to a matrix (2D array)
                matrix = df.values

                for i in range(len(matrix)):
                    self.athletes.append(dict(self.default_athlete))
                    self.private_id += 1
                    self.athletes[-1]["priv_id"] = int(self.private_id)
                    for j in range(len(matrix[0])):
                        try:
                            self.athletes[i][globals()[f'col{j+1}'].get()] = str(matrix[i][j])
                        except:
                            pass
                        print(matrix[i][j])

                # Print the matrix (optional)
                print(matrix)
                import_heat_w.destroy()
                print(self.athletes)
            tk.Button(import_heat_w,text="Ok",command= done_with_heat).pack()

            heat_height = 42*len(columns)+50
            import_heat_w.geometry("250x"+str(heat_height))

            import_heat_w.mainloop()



        elif file.split(".")[-1] == "txt":
            pass
        return

    def determine_start_time(self):
        self.start_time_button.config(state=tk.DISABLED)
    def time_scale(self,start, end, ticks):
        duration = end - start
        level = np.round(np.log(duration) / np.log(10))
        increments = 10 ** (level)
        if duration * 10 ** (1 - increments) < 5:
            increments /= 10
            print("a")
        ending = end - end % increments
        starting = start - start % increments + increments
        print(starting, ending, increments, int(level) - 1, duration)
        return np.arange(starting-increments, ending + increments / ticks, increments / ticks) , 1/increments

    def on_mouse_motion(self, event):
        # Update self.mousex and self.mousey
        self.mousex, self.mousey = event.x, event.y
        self.pfcanvas.delete(self.cursorline)
        self.cursorline = self.pfcanvas.create_line(self.mousex,0,self.mousex,self.pfcanvas.winfo_height(), fill = "black")

    def on_click(self,event):
        if not self.timeline_image.any():
            return
        time_pixels = ( (self.pfcanvas.winfo_width()-event.x) )    +      (self.pfcanvas.winfo_width()*2**(self.zoom_level-1) -self.image_x_max)
        time = (self.pfcanvas.winfo_width()*2**(self.zoom_level-1)-time_pixels)/(self.pfcanvas.winfo_width()*2**(self.zoom_level-1))
        time = self.start_time-self.record_start + (1-time)*(self.stop_time-self.start_time)

        if self.start_time_button["state"] == tk.DISABLED:
            self.audiostart = time-self.time_offset
            self.start_time_button["state"] = tk.ACTIVE
            self.handle_scroll(0)
            return
        if self.add_cursor["state"] == "normal":
            return
        time -= self.audiostart
        time1 = np.round(time*100)/100
        timestr = str(time1)
        if "." not in timestr:
            timestr = timestr+".0"
        if len(timestr.split(".")[-1]) == 1:
            timestr = timestr+"0"

        self.results.append(time)
        self.results_formatted.append(timestr+"s")
        print(self.results)
        self.result_cursors.append([0,0])
        self.result_cursors[0][0] = self.pfcanvas.create_text(self.mousex,100, anchor= "n",text = timestr+"s",fill= "red")
        self.result_cursors[0][1] = self.pfcanvas.create_line(self.mousex,100,self.mousex,self.pfcanvas.winfo_height(), fill = "black")
        print(time)

    def handle_scroll(self, event, transfer = 0):
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
                if self.image_middle > 1 - 0.5/2**(self.zoom_level-1):
                    self.image_middle = 1 - 0.5/2**(self.zoom_level-1) - 0.0001
                    print("a")
                elif self.image_middle < 0.5/2**(self.zoom_level-1):
                    self.image_middle = 0.5/2**(self.zoom_level-1) + 0.0001
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
            self.image_middle += 0.2*2 ** (1 - self.zoom_level)
        if transfer == -1:
            print("transfer left")
            self.image_middle -= 0.2*2 ** (1 -self.zoom_level)
        if self.image_middle < 0.5*2 ** (1 -self.zoom_level):
            self.image_middle = 0.5*2 ** (1 -self.zoom_level)
        if self.image_middle > 1 - 0.5 * 2 ** (1 - self.zoom_level):
            self.image_middle = 1 - 0.5 * 2 ** (1 - self.zoom_level)


        self.zoom_label.config(text = "| Zoom: x"+str(2**(self.zoom_level-1)))

        self.image_x_min = self.pfcanvas.winfo_width() * 2 ** (
                self.zoom_level - 1) * self.image_middle - self.pfcanvas.winfo_width() * 0.5
        self.image_x_max = self.pfcanvas.winfo_width() * 2 ** (
                self.zoom_level - 1) * self.image_middle + self.pfcanvas.winfo_width() * 0.5


        if len(self.zoomed_images) < self.zoom_level:
            canvas_width = self.pfcanvas.winfo_width()
            canvas_height = self.pfcanvas.winfo_height()
            zoomed_image = cv2.resize(self.timeline_image, (canvas_width * 2 ** (self.zoom_level-1), canvas_height-50-100))
            self.zoomed_images.append(zoomed_image)

        self.pfcanvas.delete("all")

        start = self.record_start-self.start_time
        end = self.stop_time-self.start_time
        duration = (end-start)
        print("start & end: ",start,end)

        print("xmax:",self.image_x_max,"xmin:",self.image_x_min,"totalx:",self.pfcanvas.winfo_width()*2**(self.zoom_level-1))

        zoomed_start = duration*((self.pfcanvas.winfo_width()*2**(self.zoom_level-1))-self.image_x_max)/(self.pfcanvas.winfo_width()*2**(self.zoom_level-1)) + start
        zoomed_end = duration*((self.pfcanvas.winfo_width()*2**(self.zoom_level-1))-self.image_x_min)/(self.pfcanvas.winfo_width()*2**(self.zoom_level-1)) + start

        print("zoomed start & end: ",zoomed_start, zoomed_end)
        scale, dummy1 = self.time_scale(zoomed_start-self.audiostart, zoomed_end-self.audiostart, 5)
        scale_positions = self.pfcanvas.winfo_width() * (1 - (scale - zoomed_start +self.audiostart) / duration*2**(self.zoom_level-1))

        scale_texts, self.carp = self.time_scale(zoomed_start-self.audiostart, zoomed_end-self.audiostart, 1)
        scale_texts = np.round(self.carp * scale_texts) / self.carp
        scale_text_positions = self.pfcanvas.winfo_width() * (1 - (scale_texts - zoomed_start+self.audiostart) / duration*2**(self.zoom_level-1))

        if self.audiodata.any():
            audiolist = self.audiodata[int(zoomed_start*self.audiosamplerate):int(zoomed_end*self.audiosamplerate)]
            points = []
            for i in range(len(audiolist)-1):
                X = self.pfcanvas.winfo_width()*(1- i/((zoomed_end-zoomed_start)*self.audiosamplerate))
                Y = 50* (1- audiolist[i][0]*2**self.audiozoomlevel)
                #print(X,Y)
                points.append(int(X))
                points.append(int(Y))
            self.pfcanvas.create_line(points, fill="white")
            print(zoomed_start,zoomed_end)

        self.pfcanvas.image = self.zoomed_images[self.zoom_level-1][0:int(self.pfcanvas.winfo_height()),
                              int(self.image_x_min):int(self.image_x_max)]
        self.img_tk = ImageTk.PhotoImage(image=Image.fromarray(self.pfcanvas.image))


        print("IMAGE CREATE")
        self.pfcanvas.create_image(0, 100, anchor=tk.NW, image=self.img_tk)


        if self.ticklines:
            for i in self.ticklines:
                self.pfcanvas.delete(i)

        for i in scale_positions:
            self.pfcanvas.create_line(i, self.pfcanvas.winfo_height()-50+10, i,
                                                                self.pfcanvas.winfo_height()-50, fill = "white")

        for i in range(len(scale_text_positions)):
            self.pfcanvas.create_text(scale_text_positions[i],self.pfcanvas.winfo_height(),text = str(scale_texts[i])[:5]+"s", anchor = "s",fill = "white")
            self.pfcanvas.create_line(scale_text_positions[i], self.pfcanvas.winfo_height()-25, scale_text_positions[i],
                                      self.pfcanvas.winfo_height() - 50, fill = "white")


        for i in range(len(self.results)):
            X = self.pfcanvas.winfo_width()*2**(self.zoom_level-1)*(self.results[i]+self.audiostart-(self.record_start-self.start_time))/(self.stop_time-self.record_start) - (self.pfcanvas.winfo_width()*2**(self.zoom_level-1)-self.image_x_max)
            print(X)
            X = self.pfcanvas.winfo_width() -X

            time1 = np.round(self.results[i] * 100) / 100
            timestr = str(time1)
            if "." not in timestr:
                timestr = timestr + ".0"
            if len(timestr.split(".")[-1]) == 1:
                timestr = timestr + "0"

            Y = 100+ (self.pfcanvas.winfo_height()-150) / len(self.results) + (self.pfcanvas.winfo_height()-150-2*(self.pfcanvas.winfo_height()-150) / len(self.results))*     i/len(self.results)

            self.result_cursors[i][1] = self.pfcanvas.create_line(X, 100, X, self.pfcanvas.winfo_height(), fill="black")
            self.result_cursors[i][0] = self.pfcanvas.create_text(X, Y, anchor="n", text=timestr + "s", fill="red")

        print("zoom level: ",self.zoom_level)
        print("middle: ",self.image_middle)

    def result(self):
        if self.results_on == 2:
            return
        def onclose():
            self.result_window.iconify()
            self.results_on = 1

        if self.results_on == 1:
            self.result_window.deiconify()
            self.results_on = 2
            return


        self.results_on = 2
        self.result_window = tk.Toplevel(self.root)
        self.result_window .title("Athletes & Results")
        self.result_window.wm_iconphoto(False, resultpic)
        self.result_window.geometry("800x250")
        self.result_window.resizable(False, True)
        self.result_window.protocol("WM_DELETE_WINDOW", onclose)
        self.resultlabels = []


        def edit_athlete(no):
            print(no)
            print(self.resultlabels)
            for i in range(len(self.resultlabels)):
                if self.resultlabels[i][-1] == no:

                    if str(self.resultlabels[i][-3].cget("image")) == str(editpic):
                        self.resultlabels[i][-3].configure(image =  okpic)
                        for j in range(len(self.resultlabels[i])-3):
                            self.resultlabels[i][j].config(state = "normal")
                        return

                    if str(self.resultlabels[i][-3].cget("image")) == str(okpic):
                        self.resultlabels[i][-3].configure(image = editpic)
                        print(self.athletes[i])
                        for j in range(len(self.resultlabels[i]) - 3):
                            self.resultlabels[i][j].config(state="readonly")
                            self.athletes[i][self.athlete_properties[j]] = str(self.resultlabels[i][j].get())
                        print(self.athletes)

        def delete_athlete(no):
            for i in range(len(self.athletes)):
                if self.athletes[i]["priv_id"] == no:
                    del self.athletes[i]
                    deleted_athlete = i
                    break
            for i in range(len(self.resultlabels)):
                if self.resultlabels[i][-1] == no:
                    for j in range(len(self.resultlabels[i])-1):
                        self.resultlabels[i][j].destroy()
                    del self.resultlabels[i]
                    break
            if deleted_athlete != len(self.athletes) +1:
                for i in range(deleted_athlete,len(self.resultlabels)):
                    for j in range(len(self.resultlabels[0])-1):
                        previous_y=self.resultlabels[i][j].winfo_y()
                        x = self.resultlabels[i][j].winfo_x()
                        self.resultlabels[i][j].place(x = x, y = previous_y-20)
            add_y = self.add_athlete_button.winfo_y()
            add_x = self.add_athlete_button.winfo_x()
            self.add_athlete_button.place(x = add_x, y = add_y -20)


        def add_athlete(parameter = 0):
            number_of_athletes = len(self.athletes)
            new_athlete = dict(self.default_athlete)
            self.private_id += 1
            new_athlete["priv_id"] = int(self.private_id)
            self.athletes.append(new_athlete)

            print("before add athlete's call:", self.resultlabels)
            if parameter == 0:
                display_results(number_of_athletes)
            print("after add athlete's call:", self.resultlabels)

        self.add_athlete_button = tk.Button(self.result_window, text="Add Athlete", command=add_athlete)
        def display_results(number_of_athletes = 0):

            tk.Label(self.result_window, text="Lane").place(x=0, y=0, anchor="nw")
            tk.Label(self.result_window, text="ID").place(x=3 + 25, y=0, anchor="nw")
            tk.Label(self.result_window, text="Full-Name").place(x=3 + 70, y=0, anchor="nw")
            tk.Label(self.result_window, text="Affiliation").place(x=3 + 310, y=0, anchor="nw")
            tk.Label(self.result_window, text="License").place(x=3 + 550, y=0, anchor="nw")
            tk.Label(self.result_window, text="Time").place(x=3 + 650, y=0, anchor="nw")
            tk.Label(self.result_window, text="Place").place(x=3 + 710, y=0, anchor="nw")

            for i in range(number_of_athletes,len(self.athletes)):
                X_lane = tk.Entry(self.result_window, width = 5)
                X_lane.insert(0,self.athletes[i]["lane"])
                X_lane.place(x=3+0,y=5+20+i*20,anchor="nw")
                X_lane.config(state="readonly")

                X_id = tk.Entry(self.result_window,width = 8)
                X_id.insert(0, self.athletes[i]["id"])
                X_id.place(x=6+25,y=5+20+i*20,anchor="nw")
                X_id.config(state="readonly")


                X_name = tk.Entry(self.result_window,width = 40)
                X_name.insert(0, self.athletes[i]["name"])
                X_name.place(x=6+70,y=5+20+i*20,anchor="nw")
                X_name.config(state="readonly")

                X_affiliation = tk.Entry(self.result_window, width = 40)
                X_affiliation.insert(0,self.athletes[i]["affiliation"])
                X_affiliation.place(x=6+310,y=5+20+i*20)
                X_affiliation.config(state="readonly")

                X_license = tk.Entry(self.result_window,width=30)
                #X_license.insert(0,self.athletes[i]["license"])
                X_license.insert(0, self.athletes[i]["license"])
                X_license.place(x =6+ 550, y = 5+20+i*20)
                X_license.config(state="readonly")

                result_list = list([self.athletes[i]["time"]]+self.results_formatted)
                X_time = ttk.Combobox(self.result_window,values = result_list, width = 10)
                X_time.set(result_list[0])
                X_time.place(x=6+650,y =5+20+ i*20)
                X_time.config(state="readonly")


                X_place = tk.Entry(self.result_window,width = 4)
                X_place.insert(0,self.athletes[i]["place"])
                X_place.place(x=6+710,y =5+ 20+i*20)
                X_place.config(state="readonly")

                X_private_id = int(self.athletes[i]["priv_id"])

                X_editbutton = tk.Button(self.result_window,image = editpic,command= partial(edit_athlete, X_private_id))
                X_editbutton.place(x = 6+740, y = 5+20+i*20, width = 20, height = 20)

                X_deletebutton = tk.Button(self.result_window, image=crosspic, command=partial(delete_athlete, X_private_id))
                X_deletebutton.place(x=6 + 760, y=5+20 + i * 20, width=20, height=20)

                X = [X_lane,X_id,X_name,X_affiliation,X_license,X_time,X_place,X_editbutton,X_deletebutton,int(self.athletes[i]["priv_id"])]
                print("athlete registered.")

                self.resultlabels.append(X)
                print(self.resultlabels[i][-1])
                print(self.athletes[i])
            self.add_athlete_button.place(x=370, y=20 + len(self.athletes) * 20 + 20)
        display_results()

        self.result_window.mainloop()

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
        self.settings.geometry("270x300")
        self.settings.wm_iconphoto(False, iconopt)
        self.settings.resizable(False, False)
        self.settings.protocol("WM_DELETE_WINDOW", self.on_closing1)
        self.canvas = tk.Canvas(self.settings, width=270, height=400, bg="#f0f0f0")
        self.canvas.pack()

        frame_width_label = tk.Label(self.settings, text = "Frame width (pixels): ")
        frame_width_label.place(x=20, y =20)

        def change_fr_width():
            self.line_thickness = int(frame_width_entry.get())

        frame_width_entry = tk.Entry(self.settings, width = 10)
        frame_width_entry.place(x = 170, y = 21)
        frame_width_entry.insert(0,str(self.line_thickness))


        image_size_label = tk.Label(self.settings, text = "Image size:")
        image_size_label.place(x = 20, y = 45)

        image_s = tk.IntVar()
        sizefull = tk.Radiobutton(self.settings, text = "Full", variable = image_s,value = 0)
        sizemin = tk.Radiobutton(self.settings, text="Minimized", variable=image_s, value = 1)
        sizefull.place(x=102, y = 44)
        sizemin.place(x=180, y=44)
        image_s.set(self.image_s)



        running_dir_label = tk.Label(self.settings, text = "Race direction:")
        running_dir_label.place(x = 20, y = 70)

        direction = tk.IntVar()
        running_dir_1 = tk.Radiobutton(self.settings, text = "L. to Right", variable = direction, value = 0)
        running_dir_2 = tk.Radiobutton(self.settings, text="R. to Left", variable=direction, value = 1)
        running_dir_1.place(x =102, y = 69)
        running_dir_2.place(x=180, y=69)
        direction.set(0)



        distance_label = tk.Label(self.settings, text = "Start signal distance (m):")
        distance_label.place(x = 20, y = 100)
        distance_entry = tk.Entry(self.settings, width = 10)
        distance_entry.place(x =170, y = 101)

        speed_label = tk.Label(self.settings, text="Speed of sound (m/s):")
        speed_label.place(x=20, y=125)
        speed_entry = tk.Entry(self.settings, width=10)
        speed_entry.place(x=170, y=126)
        speed_entry.insert(1,"340")

        wspeed_label = tk.Label(self.settings, text="Wind speed (m/s):")
        wspeed_label.place(x=20, y=150)
        wspeed_entry = tk.Entry(self.settings, width=10)
        wspeed_entry.place(x=170, y=151)
        wspeed_entry.insert(1, "0")

        time_offset_label = tk.Label(self.settings, text = "Time Offset (seconds):")
        time_offset_label.place(x=20, y = 195)

        time_offset_entry = tk.Entry(self.settings, width = 10)
        time_offset_entry.place(x = 170, y = 196)
        time_offset_entry.insert(0,str(self.time_offset))

        def save_options():
            change_fr_width()
            try:
                start_distance = float(distance_entry.get())
            except:
                start_distance = 0

            try:
                sspeed = float(speed_entry.get())
            except:
                sspeed = 340

            try:
                wspeed = float(wspeed_entry.get())
            except:
                wspeed = 0

            sound_time = start_distance/(sspeed+wspeed)


            self.time_offset = float(time_offset_entry.get()) + sound_time

            if direction.get() == 1:
                self.direction = "RL"
            else:
                self.direction = "LR"

            #self.pfcanvas.config(height=int(self.canvas_or_height*0.01*float(image_height_entry.get())))

            self.image_s = image_s.get()
            if image_s.get() == 1:
                self.pfcanvas.pack_forget()
                self.pfcanvas.config(height=450,width = 1000)
                self.pfcanvas.place(x=0, y = 70)
                print("var1")
            elif image_s.get() == 0:
                self.pfcanvas.pack_forget()
                self.infolabel.pack_forget()
                self.message.pack_forget()
                self.zoom_label.pack_forget()

                self.pfcanvas.pack(fill="both", expand=True)
                self.infolabel.pack(side = tk.LEFT, anchor = tk.S)
                self.message.pack(side = tk.LEFT, anchor = tk.S)
                self.zoom_label.pack(side = tk.LEFT, anchor = tk.S)

                print("var0")

            try:
                self.create_timeline(event = 1)
            except:
                pass
        save_button = tk.Button(self.settings, text="OK",command= save_options)

        save_button.place(x=130, y = 240, anchor = "n")


    def create_timeline(self, event = 0):
        self.zoom_level = 1
        self.image_middle = 0.5
        self.message.config(text="Creating Photo-Finish image...")
        if event == 0:
            self.video_file  = filedialog.askopenfilename()
        cap_timeline = cv2.VideoCapture(self.video_file)
        fps = cap_timeline.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap_timeline.get(cv2.CAP_PROP_FRAME_COUNT))
        #duration = frame_count / fps
        clip = VideoFileClip(self.video_file)
        audio = clip.audio
        audio.write_audiofile("temporary.wav")


        self.audiodata, self.audiosamplerate = sf.read("temporary.wav")
        self.stop_time = len(self.audiodata) / self.audiosamplerate
        self.start_time = 0
        self.record_start = 0
        self.stop_time = len(self.audiodata)/self.audiosamplerate

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
            start_x = middle_x - (self.line_thickness+1) // 2
            end_x = middle_x + (self.line_thickness+1) // 2
            middle_line_part = frame[start_y:end_y, start_x:end_x]

            frames.append(middle_line_part)
            timestamps.append(time.time() - self.start_time)
        """
        tone_similarity = 40
        default_bg = [255,255,255]
        sample_amount = 15
        sample_frame = -1

        frames[sample_frame] = cv2.GaussianBlur(frames[sample_frame], (5,5),0)

        for i in range(2,len(frames)-1):
            for j in range(len(frames[0])):
                for k in range(len(frames[0][0])):
                    frames[i] = cv2.GaussianBlur(frames[i], (5,5),0)
                    frames[i][j,k] = [ abs(frames[sample_frame][j,k][0] - frames[i][j,k][0]), abs(frames[sample_frame][j,k][1] - frames[i][j,k][1]), abs(frames[sample_frame][j,k][2] - frames[i][j,k][2])   ]
            print("preparing background",int(100*i/len(frames)),"%")
        """

        if self.direction == "RL":

            frames[0] = frames[0][start_y:end_y, 0:(self.line_thickness + 1) // 2]
            frames[-1] = frames[-1][start_y:end_y, (self.line_thickness + 1) // 2:-1]

        if self.direction == "LR":
            frames = [cv2.flip(i, 1) for i in frames]

            frames[0] = frames[0][start_y:end_y, (self.line_thickness + 1) // 2:-1]
            frames[-1] = frames[-1][start_y:end_y, 0:(self.line_thickness + 1) // 2]



        self.timeline_image = cv2.hconcat(frames)
        self.timeline_image = cv2.flip(self.timeline_image,1)

        cap_timeline.release()
        self.timeline_image = cv2.cvtColor(self.timeline_image, cv2.COLOR_RGB2BGR)
        canvas_width = self.pfcanvas.winfo_width()
        canvas_height =self.pfcanvas.winfo_height()

        self.zoomed_images = []
        self.zoomed_images.append(cv2.resize(self.timeline_image, (canvas_width, canvas_height-50-100)))
        image = self.zoomed_images[0]
        self.message.config(text="Photo-Finish image created.")
        cap_timeline.release()
        self.handle_scroll(0)
        self.cap = cv2.VideoCapture(0)

    def audio_callback(self, indata, frames, time, status,):
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > self.threshold*self.maxvolume and not self.recording:
            self.start_recording()
            self.update_video()
            print("Start sound detected. Recording & timing.")
            self.message.config(text="Start sound detected. Recording & timing.")

    def listen_start_gun(self):

        self.timer.config(text="00:00:000")
        # Initialize audio stream for listening to the start gun
        self.audio_stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.sample_rate, device=self.sound_device_index)
        self.audio_stream.start()
        print("Listening to the start gun...")
        self.message.config(text = "Waiting for the start signal...")


root = tk.Tk()
root.title("MY Photo-Finish (host)")


opticon = Image.open('images/options.ico')
iconopt = ImageTk.PhotoImage(opticon)
resultico = Image.open('images/results.ico')
resultpic = ImageTk.PhotoImage(resultico)
backwardico = Image.open('images/backward.ico')
backwardpic = ImageTk.PhotoImage(backwardico)
forwardico = Image.open('images/forward.ico')
forwardpic = ImageTk.PhotoImage(forwardico)
addcursorico = Image.open('images/add_cursor.ico')
addcursorpic = ImageTk.PhotoImage(addcursorico)
addcursorokico = Image.open('images/add_cursor_ok.ico')
addcursorokpic = ImageTk.PhotoImage(addcursorokico)
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
icon = Image.open('images/icon.ico')
iconbg = ImageTk.PhotoImage(icon)


root.wm_iconphoto(False, iconbg)
#root.state("zoomed")
root.resizable(False,False)
root.geometry("300x100")
def create_instance():
    video_recorder = VideoRecorder(root)
    video_recorder.root.mainloop()
tk.Button(text = "Create Instance", command = create_instance).place(x=150,y = 30, anchor = "n")

root.mainloop()
#pyinstaller main.py --onefile --windowed --name "OpenPhotoFinish" --manifest OpenPhotoFinish.manifest --icon "images/main.png"

"""
Title: OpenPhotoFinish
Author: Murat Yaşar BASKIN
Description: This is an open source photo finish software that primarily aims to detect race times
for athletic track events by analysing video taken at the finish line by any type of video recording device
including a mobile phone. The video must include both audio and image, including the start of the race, to detect
the start time.
To detect the start time of the race properly, the user either has to use a powerful enough blank firing pistol
whose sound can be heard from the finish line (video recording device) or the start signal must be transmitted to
the recording device at the finish line by a long cable or a radio connection (walkie-talkie).
If the latter, there is no need to adjust time delay.
If the former (sound is transmitted through open air), user must adjust for the delay via the entries in the audio tab.

ALL ABOUT THE APP: openphotofinish.blogspot.com  &  github.com/artmyb/openphotofinish
"""
print("Loading az bekle...")
import tkinter
import os
import traceback

import tkinter as tk
import threading
from PIL import ImageTk, Image
import numpy as np

import base64
from io import BytesIO

# Import the encoded image data
from splash_image import image_data
from generate_image_button import image_data as generate_image_bt
from update_image_button import image_data as update_image_bt
from preview_button import image_data as preview_bt
from apply_button import image_data as apply_bt

from import_video_button import image_data as import_video_bt
from import_video_button_w import image_data as import_video_bt_w
from export_button import image_data as export_bt
from export_button_w import image_data as export_bt_w
from add_button import image_data as add_bt
from remove_button import image_data as remove_bt
from add_button_w import image_data as add_bt_w
from remove_button_w import image_data as remove_bt_w
from import_button import image_data as import_bt
from import_button_w import image_data as import_bt_w
from main_icon import image_data as main_icon
from add_instance_button import image_data as add_instance_bt
from add_instance_button_w import image_data as add_instance_bt_w
from video import image_data as video_bt
from play import image_data as play_bt
from pause import image_data as pause_bt
from stop import image_data as stop_bt
from play_w import image_data as play_bt_w
from pause_w import image_data as pause_bt_w
from stop_w import image_data as stop_bt_w
from video_l import image_data as video_l_bt
from video_l_w import image_data as video_l_bt_w
from banner import image_data as banner_image
from gunx3 import image_data as gunx3_bt
from videox3 import image_data as videox3_bt
from tablex3 import image_data as tablex3_bt
from captures import image_data as captures_bt
from laps import image_data as laps_bt
from board import image_data as board_bt
from abort import image_data as abort_bt

#the below part is for splash screen


splash = tk.Tk()
splash.resizable(False, False)

splash.configure(bg='black')

window_width = 700
window_height = 250
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
splash.attributes("-topmost", True)
splash_canvas = tk.Canvas(splash, bg='black', width=window_width, height=window_height, highlightthickness=0)
splash_canvas.pack(fill="both", expand=True)

image_data_bytes = base64.b64decode(image_data)
image = Image.open(BytesIO(image_data_bytes))
splash_icon = ImageTk.PhotoImage(image)

splash_canvas.create_image(0, 0, anchor=tk.NW, image=splash_icon)

splash.overrideredirect(True)

splash.after(5000, splash.destroy)

splash.mainloop()

action_log = open("action_log.txt","w")
error_log = open("error_log.txt","w")

import time

import cv2
import tkinter as tk
from tkinter import filedialog

import os
from PIL import ImageDraw, ImageFont
import numpy as np
import sounddevice as sd
from tkinter import ttk
import tkinter.messagebox
import io
from moviepy.editor import VideoFileClip
import proglog
import soundfile as sf
#import tktable


from tkinter.filedialog import asksaveasfile
import pandas as pd
import pyautogui
import openpyxl
from functools import partial
import io
import base64
from datetime import datetime
import webbrowser
import urllib.parse
import pyperclip
from tkinter import font
from matplotlib import pyplot as plt
#from pydub import AudioSegment
#import simpleaudio as sa

"""
this is for VideoFileClip function to work without cmd. 
after generating executable with --windowed option, which is for running the app without cmd,
the VideoFileClip function doesn't work because it tries to print a progress bar in the cmd.
using this class below, we use another progress bar instead of printing to the cmd, that
actually does nothing.
"""

class Tabs:
    def __init__(self, parent):
        self.parent = parent
        self.button_frame = tk.Frame(parent)
        self.button_frame.pack()

    def new(self, title):
        return

class DummyLogger(proglog.ProgressBarLogger):
    def callback(self, **changes):
        pass

    def bars_callback(self, bar, attr, value, old_value=None):
        pass


def error_message(e, trace,error_at):
    global root
    global main_icon
    image_data_bytes = base64.b64decode(main_icon)
    image = Image.open(BytesIO(image_data_bytes))
    icon = ImageTk.PhotoImage(image)

    error_window = tk.Toplevel(root)
    error_window.title("Error!")
    error_window.wm_iconphoto(False,icon)
    tk.Label(error_window,
             text=f"Exception at "+error_at+f":\n{str(e).splitlines()[0]}\n\nWould you like to send the complete error log to developer\nto make the app better?").pack()

    def send_to_dev():
        recipient = "mybaskin@yahoo.com"
        subject = "Error Log Report"
        body = f"Hi,\n\nI encountered an error. Here is the log:\n\n{trace}"

        # Construct the mailto URL
        mailto_link = f"mailto:{recipient}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

        # Open the user's default mail client with the pre-filled email
        webbrowser.open(mailto_link)
        error_window.destroy()
        return

    tk.Button(error_window, text = "Yes", command=send_to_dev).pack(pady=5)

    error_window.attributes("-topmost", True)

    error_window.mainloop()


def format_time(i, decimals = 2, HMS = "variable"):
    try:
        seconds = int(i)
        decimal = (str(i + 10**(-decimals)- seconds) + decimals * "0")[1:2 + decimals]
        if float(decimal) == 0:
            seconds += 1
        #the time is rounded UP to the nearest 1/100 second according to World Athletics Competition Rules 165.24
        # Convert to struct_time
        time_struct = time.gmtime(seconds)  # or time.localtime(seconds) if you want local time

        # Format the struct_time and add milliseconds manually
        if HMS == "variable":
            if i<60:
                formatted_time = time.strftime("%S", time_struct) + decimal
            elif i<60*60:
                formatted_time = time.strftime("%M:%S", time_struct) + decimal
            else:
                formatted_time = time.strftime("%H:%M:%S", time_struct) + decimal
        elif HMS == "MM:SS":
            formatted_time = time.strftime("%M:%S", time_struct) + decimal
        elif HMS == "HH:MM:SS":
            formatted_time = time.strftime("%M:%S", time_struct) + decimal
        return formatted_time
    except Exception as e:
        error_message(e = e, trace = traceback.format_exc() , error_at = "format_time()")

#a table that can be edited with interaction
class EditableTable(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg="#222222")
        self.pack(fill=tk.BOTH, expand=True)

        self.title_canvas = tk.Canvas(self, height=50, bg="#222222", bd=0, highlightthickness=0)
        self.title_canvas.pack(fill=tk.X, expand=False)

        self.title = self.title_canvas.create_text(
            self.title_canvas.winfo_width() // 2, 25,
            text="Title: ",
            anchor=tk.W,
            fill="white"
        )
        self.title_entry = tk.Entry(self.title_canvas, bd = 0 , w = 60, highlightthickness=0)
        self.title_entry.place(x = self.title_canvas.winfo_width() // 2 + 30, y= 25,anchor = tk.W)

        self.root = root
        self.headers = ["Lane", "ID", "Name", "Date of Birth", "Affiliation", "License", "Time", "Place"]
        self.data = []

        self.results = []
        self.decimals = 2
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Calibri", 10), background="#222222", fieldbackground="#222222",
                        foreground="#CCCCCC")
        style.map('Custom.Treeview', background=[('selected', '#444444')], foreground=[('selected', 'white')])
        style.configure("Custom.Treeview.Heading", font=("Calibri", 10, "bold"), background="#111111",
                        foreground="white")

        # Create a frame to hold the treeview and scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)


        self.tree = ttk.Treeview(self.tree_frame, columns=self.headers, show='headings', style="Custom.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for header in self.headers:
            self.tree.heading(header, text=header)
            if header in ["Lane", "ID", "Time", "Place"]:
                self.tree.column(header, anchor='center', width=0)
            else:
                self.tree.column(header, anchor='center')

        self.update_table()

        # the table is edited by double clicking on a cell.
        self.tree.bind('<Double-1>', self.on_double_click)

        self.entry = None
        self.combobox_frame = None
        self.combobox = None

        self.button_frame = tk.Frame(self, bg="#222222")
        self.button_frame.pack(fill=tk.X, padx=10, pady=0)

        self.center_frame = tk.Frame(self.button_frame, bg="#222222")
        self.center_frame.pack(pady=10)

        self.image_canvas = tk.Canvas(self, bg = "black", highlightthickness = 0)
        self.image_canvas.pack(fill=tk.BOTH, expand = True)

        self.image_button_frame = tk.Frame(self, bg="#222222", height = 10)
        self.image_button_frame.pack(padx = 10)

        self.image_left_button = tk.Button(self.image_button_frame, image=left_icon,
                                           command=partial(self.image_borders, "vleft"), bd=0, width=70, height=35)
        self.image_left_button.bind("<Enter>", self.enter_left)
        self.image_left_button.bind("<Leave>", self.leave_left)
        self.image_left_button.pack(side=tk.LEFT, padx=10)
        self.image_out_button = tk.Button(self.image_button_frame, image=zoom_out_icon,
                                          command=partial(self.image_borders, "vout"), bd=0, width=35, height=35)
        self.image_out_button.bind("<Enter>", self.enter_out)
        self.image_out_button.bind("<Leave>", self.leave_out)
        self.image_out_button.pack(side=tk.LEFT)
        self.image_in_button = tk.Button(self.image_button_frame, image=zoom_in_icon,
                                         command=partial(self.image_borders, "vin"), bd=0, width=35, height=35)
        self.image_in_button.bind("<Enter>", self.enter_in)
        self.image_in_button.bind("<Leave>", self.leave_in)
        self.image_in_button.pack(side=tk.LEFT)
        self.image_right_button = tk.Button(self.image_button_frame, image=right_icon,
                                            command=partial(self.image_borders, "vright"), bd=0, width=70, height=35)
        self.image_right_button.bind("<Enter>", self.enter_right)
        self.image_right_button.bind("<Leave>", self.leave_right)
        self.image_right_button.pack(side=tk.LEFT, padx=10)

        # Image decoding
        image_data_bytes = base64.b64decode(import_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(import_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_icon_w = ImageTk.PhotoImage(image)

        self.import_button = tk.Button(self.center_frame, image=self.import_icon, bd=0, command=self.root.import_heat,
                                       bg="#222222")
        self.import_button.pack(side=tk.LEFT, padx=10)
        self.import_button.bind("<Enter>", self.enter_import)
        self.import_button.bind("<Leave>", self.leave_import)

        self.paste_button = tk.Button(self.center_frame, text = "Paste from Clipboard", bd = 0, highlightthickness=0, font = font.Font(family="Cooper Black", size=11, slant="italic"), command = self.paste_from_clipboard)
        self.paste_button.pack(side = tk.LEFT, padx = 5)
        # to export the results as excel or text file

        image_data_bytes = base64.b64decode(video_l_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.video_l_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(video_l_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.video_l_icon_w = ImageTk.PhotoImage(image)

        # to view photo-finish image on top-level while setting up results.
        self.view_pf_button = tk.Button(self.center_frame, image=self.video_l_icon, bd=0, command=self.visualise_image)
        self.view_pf_button.pack(side=tk.LEFT, padx=10)
        self.view_pf_button.bind("<Enter>", self.enter_view_pf)
        self.view_pf_button.bind("<Leave>", self.leave_view_pf)

        image_data_bytes = base64.b64decode(add_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(add_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_icon_w = ImageTk.PhotoImage(image)

        # to add a new row (or new athlete if you will)
        self.add_button = tk.Button(self.center_frame, image=self.add_icon, bd=0, command=self.add_row, bg="#222222")
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.add_button.bind("<Enter>", self.enter_add)
        self.add_button.bind("<Leave>", self.leave_add)

        image_data_bytes = base64.b64decode(remove_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.remove_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(remove_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.remove_icon_w = ImageTk.PhotoImage(image)

        # to remove a row
        self.remove_button = tk.Button(self.center_frame, image=self.remove_icon, bd=0,
                                       command=partial(self.delete_row, 0), bg="#222222")
        self.remove_button.pack(side=tk.LEFT, padx=10)
        self.remove_button.bind("<Enter>", self.enter_remove)
        self.remove_button.bind("<Leave>", self.leave_remove)
        self.tree.bind("<Delete>", self.delete_row)

        # obvious
        self.sort_combobox = ttk.Combobox(self.center_frame, values=[x for i in self.headers for x in (
        "Sort by " + i + "\u2191", "Sort by " + i + "\u2193")], background="#222222")
        self.sort_combobox.set("Sort by...")
        self.sort_combobox.pack(side=tk.LEFT, padx=10)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_table)
        self.sort_combobox.state(["readonly"])

        self.decimals_combo = ttk.Combobox(self.center_frame, values = ["1 decimal place", "2 decimal places", "3 decimal places", "4 decimal places", "5 decimal places"], background= "#222222")
        self.decimals_combo.set("2 decimal places")
        self.decimals_combo.pack(side= tk.LEFT, padx = 10)
        self.decimals_combo.bind("<<ComboboxSelected>>", self.update_decimals)
        self.decimals_combo.state(["readonly"])

        self.copy_button = tk.Button(self.center_frame, text = "Copy to Clipboard", bd = 0, highlightthickness=0, font = font.Font(family="Cooper Black", size=11, slant="italic"), command = self.copy_to_clipboard)
        self.copy_button.pack(side = tk.LEFT, padx = 5)
        # to export the results as excel or text file
        self.export_button = tk.Button(self.center_frame, image=self.root.export_image_icon, bd=0,
                                       command=self.root.export_results_table, bg="#222222")
        self.export_button.pack(side=tk.LEFT, padx=10)
        self.export_button.bind("<Enter>", self.enter_export)
        self.export_button.bind("<Leave>", self.leave_export)

        # Create a vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.original_v_scrollbar_command = self.v_scrollbar.cget('command')
        self.no_op_command = lambda *args: None

        self.image_center = 0.5
        self.image_zoom_x = 1

    """
    those enter_sth, leave_sth functions are for changing the button image
    when the mouse is hovering over the button. the images are just a brighter
    versions of the originals.
    
    """

    def update_decimals(self, event):
        try:
            self.decimals = int(self.decimals_combo.get()[0])
            self.update_results(new_results = self.root.results_sorted)
        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="update_decimals()")
    def enter_view_pf(self,event):
        self.view_pf_button.config(image = self.video_l_icon_w)

    def leave_view_pf(self,event):
        self.view_pf_button.config(image = self.video_l_icon)


    def enter_import(self, event):
        self.import_button.config(image=self.import_icon_w)

    def leave_import(self, event):
        self.import_button.config(image=self.import_icon)

    def enter_export(self, event):
        self.export_button.config(image=self.root.export_image_icon_w)

    def leave_export(self, event):
        self.export_button.config(image=self.root.export_image_icon)

    def enter_add(self, event):
        self.add_button.config(image=self.add_icon_w)

    def leave_add(self, event):
        self.add_button.config(image=self.add_icon)

    def enter_remove(self, event):
        self.remove_button.config(image=self.remove_icon_w)

    def leave_remove(self, event):
        self.remove_button.config(image=self.remove_icon)

    def change_title(self, title):
        #self.title_canvas.itemconfig(self.title, text=title)
        self.title_entry.delete(0,tk.END)
        self.title_entry.insert(0,title)

    def on_double_click(self, event):
        try:
            region = self.tree.identify_region(event.x, event.y)
            if region == 'cell':
                column = self.tree.identify_column(event.x)
                row = self.tree.identify_row(event.y)

                if self.entry:
                    self.entry.destroy()
                if self.combobox:
                    self.combobox.destroy()
                if self.combobox_frame:
                    self.combobox_frame.destroy()

                x, y, width, height = self.tree.bbox(row, column)
                value = self.tree.item(row, 'values')[int(column[1:]) - 1]

                col_index = int(column[1:]) - 1

                self.v_scrollbar.config(command=self.no_op_command)
                if self.headers[col_index] == "Time":
                    self.combobox_frame = tk.Frame(self.tree_frame, borderwidth=1, relief='solid', bg="#222222")
                    self.combobox_frame.place(x=x, y=y, width=width, height=height)

                    self.combobox = ttk.Combobox(self.combobox_frame, values=self.results, background="#222222")
                    self.combobox.pack(fill=tk.BOTH, expand=True)
                    self.combobox.set(value)
                    self.combobox.focus()

                    self.combobox.bind('<<ComboboxSelected>>',
                                       lambda event, col=column, r=row: self.on_combobox_selected(col, r))
                    self.combobox.bind('<Return>',
                                       lambda event, col=column, r=row: self.on_combobox_selected(col, r))
                else:
                    self.entry = tk.Entry(self.tree, background="#222222", foreground="white")
                    self.entry.place(x=x, y=y, width=width, height=height)
                    self.entry.insert(0, value)
                    self.entry.focus()
                    self.entry.bind('<Return>', lambda event, col=column, r=row: self.on_entry_return(col, r))
                    self.entry.bind('<FocusOut>', lambda event, col=column, r=row: self.on_entry_return(col, r))
        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="on_double_click()")

    def on_entry_return(self, column, row):
        try:
            self.v_scrollbar.config(command=self.original_v_scrollbar_command)
            new_value = self.entry.get()
            values = list(self.tree.item(row, 'values'))
            col_index = int(column[1:]) - 1
            values[col_index] = new_value
            self.tree.item(row, values=values)

            for row_data in self.data:
                if str(row_data["ID"]) == values[1]:  # Assuming ID is unique
                    row_data[self.headers[col_index]] = new_value
                    break
                print(col_index)

            print(self.data)
            self.entry.destroy()
            self.entry = None
        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="on_entry_return()")

    def on_combobox_selected(self, column, row):
        self.v_scrollbar.config(command=self.original_v_scrollbar_command)
        new_value = self.combobox.get()
        values = list(self.tree.item(row, 'values'))
        col_index = int(column[1:]) - 1
        values[col_index] = new_value
        self.tree.item(row, values=values)

        for row_data in self.data:
            if str(row_data["ID"]) == values[1]:  # Assuming ID is unique
                row_data[self.headers[col_index]] = new_value
                break

        self.combobox.destroy()
        self.combobox_frame.destroy()
        self.combobox = None
        self.combobox_frame = None
        self.update_places()

    def add_row(self):
        new_id = len(self.data) + 1
        new_row = {"Lane": "Type Lane", "ID": new_id, "Name": "Type Name", "Date of Birth": "Type DOB", "Affiliation": "Type Affiliation", "License": "Type License", "Time": "",
                   "Place": ""}
        self.data.append(new_row)
        self.tree.insert('', tk.END, values=[new_row.get(header, '') for header in self.headers])

    def delete_row(self,event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], 'values')
            self.tree.delete(selected_item[0])
            self.data = [row for row in self.data if str(row["ID"]) != values[1]]

    def sort_table(self, event):
        selected_header = self.sort_combobox.get()
        ascending = selected_header.endswith("\u2191")
        selected_header = selected_header.replace("Sort by ", "").rstrip("\u2191\u2193")

        if selected_header == "Time":
            self.update_places()
        else:
            self.data.sort(key=lambda x: x.get(selected_header, ''), reverse=not ascending)
            self.update_table()


    #places are updated according to times.
    def update_places(self):
        time_to_place = sorted(self.data, key=lambda x: x.get("Time", ''))
        time_to_place_dict = {row["ID"]: str(index + 1) for index, row in enumerate(time_to_place)}

        for row in self.data:
            row["Place"] = time_to_place_dict.get(row["ID"], "")
        self.update_table()

    def update_results(self, new_results):
        self.results = []
        for i in new_results:
            updated = format_time(i, decimals = self.decimals)
            self.results.append(updated)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.data:
            self.tree.insert('', tk.END, values=[row.get(header, '') for header in self.headers])


    # to get data from excel, excel data is first converted into a matrix (list of lists)
    # and here it sets the table according to that matrix.
    def set_data_from_matrix(self, matrix):
        self.data = []

        # If already in dictionary form, no need to match headers
        if isinstance(matrix[0], dict):
            self.data = matrix
        elif all(len(row) == len(self.headers) for row in matrix):
            for row in matrix:
                row_data = {self.headers[i]: row[i] for i in range(len(self.headers))}
                self.data.append(row_data)
        else:
            print("Matrix row length does not match headers length")
            return

        self.update_table()

    def paste_from_clipboard(self, event = 0):
        self.root.import_heat(mode=1)

    def copy_to_clipboard(self, event=0):
        text = ""
        for i in range(len(self.data)):
            for j in self.root.default_parameters:
                try:
                    text += str(self.data[i][j]) + "\t"  # Ensure it's a string
                except:
                    text += "nan" + "\t"
            text = text.rstrip("\t")  # Remove the last tab from each line
            text += "\n"  # Add a newline after each row
        pyperclip.copy(text)

    def visualise_image(self):

        self.image_canvas.delete("all")

        center_time = (1-self.image_center)*(self.root.image_end_time_full-self.root.image_start_time_full) + self.root.image_start_time_full

        self.image_start_time = center_time - (self.root.image_end_time_full-self.root.image_start_time_full)*0.5*0.75 ** (self.image_zoom_x-1)
        self.image_end_time = center_time + (self.root.image_end_time_full - self.root.image_start_time_full) * 0.5*0.75 ** (self.image_zoom_x-1)

        start = self.image_center - 0.5*0.75 ** (self.image_zoom_x-1)
        end = self.image_center + 0.5*0.75 ** (self.image_zoom_x-1)


        level = np.log(self.image_end_time-self.image_start_time)/np.log(10)
        level = int(level+0.5)
        tick_increments = 10**(level-2)
        label_increments = 10**(level-1)

        tick_start = self.image_start_time - self.image_start_time%tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time%tick_increments
        ticks = np.arange(tick_start,tick_end+10*tick_increments,tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = self.image_canvas.winfo_width()*(1-(ticks-self.image_start_time)/(self.image_end_time-self.image_start_time))

        locations_2 = self.image_canvas.winfo_width() * (1-(labels - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))

        #print(labels)
        #print(locations_2)

        loc_points = []
        scaleY = self.image_canvas.winfo_height() - self.root.scale_height
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY+5)
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY)

        #print("time borders:",self.image_start_time,self.image_end_time)

        #print("center:",self.image_center)
        #print("zoom:", self.image_zoom_x)

        for i in range(len(labels)):
            if label_increments >=1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i]*(1/label_increments))*label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0]+"."+thestr.split(".")[-1][:int(np.log(1/label_increments)/np.log(10))]

            self.image_canvas.create_text(locations_2[i],self.image_canvas.winfo_height()-10,text = thestr,fill="#DDDDDD")
            self.image_canvas.create_line(locations_2[i],self.image_canvas.winfo_height()-20,locations_2[i],scaleY,fill = "#DDDDDD")


        #print("borders:", start, end)
        #print(len(self.zoomed_images))

        height1, width1  = self.root.zoomed_images[0].shape

        cropped_image = cv2.resize(self.root.zoomed_images[self.root.image_zoom_x - 1][0:height1,
                        int(width1 * (1/0.75) ** (self.root.image_zoom_x - 1) * start):int(
                            width1 * (1/0.75) ** (self.root.image_zoom_x - 1) * end)],
                                   (int(width1*self.image_canvas.winfo_width()/self.root.image_canvas.winfo_width()),self.image_canvas.winfo_height()-self.root.scale_height))

        image_pil = Image.fromarray(cropped_image)

        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.image_canvas.create_line(loc_points, fill="#DDDDDD")

        for i in self.root.results:
            X = self.image_canvas.winfo_width() * (1 - (i - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))
            self.image_canvas.create_line(X, 0, X,self.image_canvas.winfo_height() - self.root.scale_height,
                                                       fill=self.root.hashline_color)
        return

    def image_borders(self,var = None):
        if var == "vin" and self.image_zoom_x < self.root.max_image_zoom:
            self.image_zoom_x += 1

        elif var == "vout" and self.image_zoom_x > 1:
            self.image_zoom_x -= 1

        elif var == "vleft":
            self.image_center -= (1-0.75)*0.75**(self.image_zoom_x-1)

        elif var == "vright":
            self.image_center += (1-0.75)*0.75**(self.image_zoom_x-1)

        if self.image_center < 0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 0.5 *0.75** (self.image_zoom_x-1)

        elif self.image_center > 1-0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 1- 0.5*0.75 ** (self.image_zoom_x-1)


        self.visualise_image()

    def enter_left(self, event):
        self.image_left_button.config(image=left_icon_w)

    def leave_left(self, event):
        self.image_left_button.config(image=left_icon)

    def enter_right(self, event):
        self.image_right_button.config(image=right_icon_w)

    def leave_right(self, event):
        self.image_right_button.config(image=right_icon)

    def enter_in(self, event):
        self.image_in_button.config(image=zoom_in_icon_w)

    def leave_in(self, event):
        self.image_in_button.config(image=zoom_in_icon)

    def enter_out(self, event):
        self.image_out_button.config(image=zoom_out_icon_w)

    def leave_out(self, event):
        self.image_out_button.config(image=zoom_out_icon)


"""
    def update_results(self, new_results):
        self.results = []
        for i in new_results:
            if i>60:
                item = str(int(i // 60)) + ":" + str(int((i % 60) * 100) / 100)
                if item[-2] == ".":
                    item = item+"0"
            else:
                item = str(int((i) * 100) / 100)
                if item[-2] == ".":
                    item = item + "0"
            self.results.append(item)
"""


"""
the main class.
this class creates a window with all the components of the program
a window (instance) is already created after you start running the app
for a new instance, you click on the top center icon on the window.
each window will work separately.
all the instances work as "toplevel" windows whose root window is a secretly
running window that always run as long as at least one instance is present,
and stops running after the last single window is closed.
"""
class Instance:
    def __init__(self,root):
        try:


            self.mousex = 0
            self.mousey = 0

            image_data_bytes = base64.b64decode(main_icon)
            image = Image.open(BytesIO(image_data_bytes))
            self.main_icon = ImageTk.PhotoImage(image)
            self.parent = root
            self.parent.wm_iconphoto(False, self.main_icon)
            self.root = tk.Toplevel(root)
            self.root.title("OpenPhotoFinish")

            self.root.wm_iconphoto(False, self.main_icon)
            self.style = ttk.Style()

            """
            the reason for error handling is that when you try to create the second instance,
            it gives error becos style has already been created.
            """
            try:
                self.style.theme_create('custom_theme', parent='alt', settings={
                    'TNotebook': {
                        'configure': {
                            'tabmargins': [0,0,0,0],
                            'background': '#222222'
                        }
                    },
                    'TNotebook.Tab': {
                        'configure': {
                            'padding': [0, 0],
                            'background': '#222222',
                            'foreground': '#222222',
                            'borderwidth': 0
                        },
                        'map': {
                            'background': [('selected', '#444444')],
                            'foreground': [('selected', '#222222')],
                            'expand': [('selected', [1, 1, 1, 0])]
                        }
                    }
                })
            except:
                pass

            self.style.theme_use('custom_theme')
            self.root.configure(bg='black')
            self.root.config(bg='black')
            self.root.option_add('*Background', '#222222')
            self.root.option_add('*Foreground', '#FFFFFF')
            self.root.option_add('*Button.Background', '#222222')
            #self.root.overrideredirect(True)
            self.root.state("zoomed")
            self.root.resizable(True, True)
            self.out = None
            self.start_time = 0
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            #self.video_label = tk.Label(root)
            #self.video_label.pack()

            self.font = "courier"
            self.hashline_color = "#FF0000"

            self.audio_data, self.audiosamplerate = None, None
            self.duration = None

            self.top_frame = tk.Frame(self.root, height = 1)
            self.top_frame.pack(fill = "both", expand = True)

            image_data_bytes = base64.b64decode(add_instance_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.add_instance_icon = ImageTk.PhotoImage(image)
            image_data_bytes = base64.b64decode(add_instance_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.add_instance_icon_w = ImageTk.PhotoImage(image)


            self.new_instance_button = tk.Button(self.top_frame, image = self.add_instance_icon, command = self.new_instance, bd = 0)
            self.new_instance_button.pack(fill='x')
            self.new_instance_button.bind("<Enter>",self.enter_new_instance)
            self.new_instance_button.bind("<Leave>", self.leave_new_instance)


            #tabs for the three main frames of the software
            self.notebook = ttk.Notebook(self.top_frame, style='lefttab.TNotebook')
            self.notebook.pack(expand=True, fill='both')

            image_data_bytes = base64.b64decode(gunx3_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.gun_bt = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(videox3_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.video_bt = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(tablex3_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.table_bt = ImageTk.PhotoImage(image)

            self.audio_frame = tk.Frame(self.notebook)
            self.image_frame = tk.Frame(self.notebook)
            self.results_frame = tk.Frame(self.notebook)
            self.style.configure('lefttab.TNotebook', font="TkDefaultFont", tabposition='wn')
            self.notebook.add(self.audio_frame, image = self.gun_bt)
            self.notebook.add(self.image_frame, image = self.video_bt)
            self.notebook.add(self.results_frame, image = self.table_bt)


            #the bottom frame to display informations, progress bars etc.
            self.global_frame = tk.Frame(self.root, height=50, highlightthickness=0)
            self.global_frame.pack(side=tk.BOTTOM,fill='x')

            self.status = tk.Canvas(self.global_frame, height=40, bg="black", highlightthickness=0)
            self.status.pack(fill='x', expand = True)

            self.status_text =  None
            self.audio_canvas = tk.Canvas(self.audio_frame, bg="#000000", highlightthickness=0)
            self.audio_canvas.pack(fill='both', expand=True)


            self.image_options = tk.Canvas(self.image_frame, width=350, height=745, bg="#222222",
                                           highlightthickness=0)
            self.image_options.pack(side=tk.LEFT)

            self.image_canvas2 = tk.Canvas(self.image_frame, bg="black", highlightthickness=0)
            self.image_canvas2.pack(fill='both', expand=True)
            self.image_canvas2.bind("<Motion>", self.display_zoom)
            self.image_canvas2.bind("<Leave>", self.leave_image_canvas2)
            self.image_canvas2.bind("<MouseWheel>", self.change_display_zoom)

            self.image_canvas = tk.Canvas(self.image_frame, bg="black", highlightthickness=0)
            self.image_canvas.pack(fill='both', expand= True)
            self.image_canvas.bind("<Leave>", self.leave_image_canvas)


            self.audio_button_frame = tk.Frame(self.audio_frame, highlightthickness=0)
            self.audio_button_frame.pack(anchor=tk.S)

            self.image_button_frame = tk.Frame(self.image_frame, highlightthickness=0)
            self.image_button_frame.pack(anchor=tk.S)

            self.image_canvas.config(cursor="none")

            image_data_bytes = base64.b64decode(import_video_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.import_video_icon = ImageTk.PhotoImage(image)
            image_data_bytes = base64.b64decode(import_video_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.import_video_icon_w = ImageTk.PhotoImage(image)


            self.import_video_button = tk.Button(self.audio_button_frame, image = self.import_video_icon, bd = 0, command = self.analyze_audio)
            self.import_video_button.pack(side=tk.LEFT)
            self.import_video_button.bind("<Enter>",self.enter_video_import)
            self.import_video_button.bind("<Leave>", self.leave_video_import)


            self.audio_left_button = tk.Button(self.audio_button_frame, image=left_icon,
                                               command=partial(self.audio_borders, "vleft"), bd=0, width=70, height=35)
            self.audio_left_button.bind("<Enter>",self.enter_left)
            self.audio_left_button.bind("<Leave>", self.leave_left)
            self.audio_left_button.pack(side=tk.LEFT, padx=10)

            self.audio_out_button = tk.Button(self.audio_button_frame, image=zoom_out_icon,
                                              command=partial(self.audio_borders, "vout"), bd=0, width=35, height=35)
            self.audio_out_button.bind("<Enter>",self.enter_out)
            self.audio_out_button.bind("<Leave>", self.leave_out)
            self.audio_out_button.pack(side=tk.LEFT)

            self.audio_in_button = tk.Button(self.audio_button_frame, image=zoom_in_icon,
                                             command=partial(self.audio_borders, "vin"), bd=0, width=35, height=35)
            self.audio_in_button.bind("<Enter>",self.enter_in)
            self.audio_in_button.bind("<Leave>", self.leave_in)
            self.audio_in_button.pack(side=tk.LEFT)

            self.audio_right_button = tk.Button(self.audio_button_frame, image=right_icon,
                                                command=partial(self.audio_borders, "vright"), bd=0, width=70, height=35)
            self.audio_right_button.bind("<Enter>",self.enter_right)
            self.audio_right_button.bind("<Leave>", self.leave_right)
            self.audio_right_button.pack(side=tk.LEFT, padx=10)

            image_data_bytes = base64.b64decode(play_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.play_bt = ImageTk.PhotoImage(image)
            image_data_bytes = base64.b64decode(play_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.play_bt_w = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(stop_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.stop_bt = ImageTk.PhotoImage(image)
            image_data_bytes = base64.b64decode(stop_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.stop_bt_w = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(pause_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.pause_bt = ImageTk.PhotoImage(image)
            image_data_bytes = base64.b64decode(pause_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.pause_bt_w = ImageTk.PhotoImage(image)

            self.play_button = tk.Button(self.audio_button_frame, image = self.play_bt, command = self.play, bd = 0)
            self.play_button.pack(side=tk.LEFT)
            self.play_button.bind("<Enter>", self.enter_play)
            self.play_button.bind("<Leave>", self.leave_play)
            self.stop_button = tk.Button(self.audio_button_frame, image = self.stop_bt, command=self.stop, bd = 0)
            self.stop_button.pack(side=tk.LEFT)
            self.play_button.config(state = "disabled")
            self.stop_button.bind("<Enter>", self.enter_stop)
            self.stop_button.bind("<Leave>", self.leave_stop)

            self.audio_high_var = tk.IntVar()
            self.audio_high_var.set(0)
            self.audio_high_tick = tk.Checkbutton(self.audio_button_frame, text = "HQ plot", var = self.audio_high_var, command = self.handle_scroll_audio)
            self.audio_high_tick.pack(side = tk.LEFT, padx = 3)
            cap_font = font.Font(family="Cooper Black", size=15, slant="italic")
            self.capture_button = tk.Button(self.audio_button_frame, text = "CAP", font = cap_font,bd = 0, command = self.capture)
            self.capture_button.pack(side = tk.LEFT)

            self.save_sample_button = tk.Button(self.audio_button_frame, text = "Save Signal Profile",command = self.save_gun_sample)
            self.save_sample_button.pack(side = tk.LEFT)

            self.find_gun_button = tk.Button(self.audio_button_frame, text="Find Signal", command=self.find_gun)
            self.find_gun_button.pack(side=tk.LEFT)

            #self.previous_shot_bt = tk.Button(self.audio_button_frame, text = "<<<", command = self.previous_gunshot)
            #self.previous_shot_bt.pack(side=tk.LEFT)

            #self.next_shot_bt = tk.Button(self.audio_button_frame, text=">>>", command=self.next_gunshot)
            #self.next_shot_bt.pack(side=tk.LEFT)

            self.captures = []

            self.audio_entry_frame = tk.Frame(self.audio_frame, highlightthickness= 0)
            self.audio_entry_frame.pack(anchor = tk.S)


            self.gun_mic_var = 100
            self.gun_start_var = 5
            self.sound_var = 340
            self.wind_var = 0
            self.time_var = 0

            def enable_apply(event):
                self.apply_button.config(state="normal")

            tk.Label(self.audio_entry_frame, text="Start signal - microphone distance (m):").pack(side = tk.LEFT)
            self.gun_mic_entry = tk.Entry(self.audio_entry_frame, width=10)
            self.gun_mic_entry.pack(side = tk.LEFT)
            self.gun_mic_entry.bind("<KeyRelease>", enable_apply)
            """
            self.sound_options.create_image(330, 85, anchor=tk.E, image=mic_icon)
            self.sound_options.create_image(20, 85, anchor=tk.W, image=gun_icon)
            self.sound_options.create_line(220, 85, 300, 85, fill="#666666")
            self.sound_options.create_line(50, 85, 130, 85, fill="#666666")
            self.sound_options.create_text(175, 85, text="?", fill="#DDDDDD")
            """
            self.gun_mic_entry.insert(0, str(self.gun_mic_var))

            tk.Label(self.audio_entry_frame, text="   Race start - start signal distance (m):").pack(side = tk.LEFT)
            self.gun_start_entry = tk.Entry(self.audio_entry_frame, width=10)
            self.gun_start_entry.pack(side = tk.LEFT)
            self.gun_start_entry.bind("<KeyRelease>", enable_apply)
            """
            self.sound_options.create_image(330, 175, anchor=tk.E, image=gun_icon)
            self.sound_options.create_image(20, 175, anchor=tk.W, image=start_icon)
            self.sound_options.create_line(220, 175, 300, 175, fill="#666666")
            self.sound_options.create_line(50, 175, 130, 175, fill="#666666")
            self.sound_options.create_text(175, 175, text="?", fill="#DDDDDD")
            """
            self.gun_start_entry.insert(0, str(self.gun_start_var))

            tk.Label(self.audio_entry_frame, text="   Speed of sound (m/s):").pack(side = tk.LEFT)
            self.sound_entry = tk.Entry(self.audio_entry_frame, width=10)
            self.sound_entry.pack(side = tk.LEFT)
            #self.sound_options.create_image(330, 250, anchor=tk.E, image=sound_icon)
            self.sound_entry.insert(0, str(self.sound_var))
            self.sound_entry.bind("<KeyRelease>", enable_apply)

            tk.Label(self.audio_entry_frame, text="   Wind speed (m/s):").pack(side = tk.LEFT)
            self.wind_entry = tk.Entry(self.audio_entry_frame, width=10)
            self.wind_entry.pack(side = tk.LEFT)
            #self.sound_options.create_image(330, 320, anchor=tk.E, image=wind_icon)
            self.wind_entry.insert(0, str(self.wind_var))
            self.wind_entry.bind("<KeyRelease>", enable_apply)

            tk.Label(self.audio_entry_frame, text="   Additional time offset (s):").pack(side = tk.LEFT)
            self.time_entry = tk.Entry(self.audio_entry_frame, width=10)
            self.time_entry.pack(side = tk.LEFT)
            self.time_entry.insert(0, str(self.time_var))
            self.time_entry.bind("<KeyRelease>", enable_apply)


            def apply():
                try:
                    self.gun_mic_var = float(self.gun_mic_entry.get())
                    self.gun_start_var = float(self.gun_start_entry.get())
                    self.sound_var = float(self.sound_entry.get())
                    self.wind_var = float(self.wind_entry.get())
                    self.time_var = float(self.time_entry.get())
                    self.apply_button.config(state="disabled")
                except Exception as e:
                    error_message(e=e, trace=traceback.format_exc(), error_at="apply()")
                return

            image_data_bytes = base64.b64decode(apply_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.apply_icon = ImageTk.PhotoImage(image)

            self.apply_button = tk.Button(self.audio_entry_frame, image = self.apply_icon, bd = 0, command = apply)
            self.apply_button.pack(side = tk.LEFT, padx=10)
            self.apply_button.config(state = "disabled")



            tk.Label(self.image_button_frame, text= "BEGIN:").pack(side=tk.LEFT)
            self.image_start_entry_minute = tk.Entry(self.image_button_frame, width = 5)
            self.image_start_entry_minute.pack(side=tk.LEFT)

            tk.Label(self.image_button_frame, text="m ").pack(side=tk.LEFT)
            self.image_start_entry_second = tk.Entry(self.image_button_frame, width=5)
            self.image_start_entry_second.pack(side=tk.LEFT)

            tk.Label(self.image_button_frame, text="s   END:").pack(side=tk.LEFT)
            self.image_end_entry_minute = tk.Entry(self.image_button_frame, width=5)
            self.image_end_entry_minute.pack(side=tk.LEFT)

            tk.Label(self.image_button_frame, text="m ").pack(side=tk.LEFT)
            self.image_end_entry_second = tk.Entry(self.image_button_frame, width=5)
            self.image_end_entry_second.pack(side=tk.LEFT)
            tk.Label(self.image_button_frame, text="s   ").pack(side=tk.LEFT)

            self.fps_inc_combo = ttk.Combobox(self.image_button_frame, values = ["Do not increase FPS",
                                                                                 "Increase FPS by x2",
                                                                                 "Increase FPS by x3",
                                                                                 "Increase FPS by x4",
                                                                                 "Increase FPS by x5",
                                                                                 "Increase FPS by x6"])
            self.style.configure("TCombobox",  fieldbackground="#444444", background="#222222", foreground = "#DDDDDD")
            self.fps_inc_combo.configure(style="TCombobox")
            self.fps_inc_combo.config(state = ["readonly"])
            self.fps_inc_combo.set("Do not increase FPS")
            self.fps_inc_combo.pack(side = tk.LEFT)

            self.capture_button2 = tk.Button(self.image_button_frame, text="CAP", font=cap_font, bd=0, command=self.capture)
            self.capture_button2.pack(side=tk.LEFT)

            image_data_bytes = base64.b64decode(generate_image_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.generate_image_icon = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(abort_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.abort_icon = ImageTk.PhotoImage(image)

            self.image_button = tk.Button(self.image_button_frame, image = self.generate_image_icon, bd = 0, command=self.generate_new_image)
            self.image_button.pack(side=tk.LEFT, padx=10)
            self.image_button.config(state= "disabled")


            self.image_undo_button = tk.Button(self.image_button_frame, image=undo_icon, command=self.undo, bd=0, width=35,
                                               height=35)
            self.image_undo_button.bind("<Enter>",self.enter_undo)
            self.image_undo_button.bind("<Leave>", self.leave_undo)
            self.image_undo_button.pack(side=tk.LEFT)

            self.image_redo_button = tk.Button(self.image_button_frame, image=redo_icon, command=self.redo, bd=0, width=35,
                                               height=35)
            self.image_redo_button.bind("<Enter>",self.enter_redo)
            self.image_redo_button.bind("<Leave>", self.leave_redo)
            self.image_redo_button.pack(side=tk.LEFT)

            self.root.bind('<Control-z>', self.undo)
            self.root.bind('<Control-Z>', self.redo)

            self.image_left_button = tk.Button(self.image_button_frame, image=left_icon,
                                               command=partial(self.image_borders, "vleft"), bd=0, width=70, height=35)
            self.image_left_button.bind("<Enter>",self.enter_left)
            self.image_left_button.bind("<Leave>", self.leave_left)
            self.image_left_button.pack(side=tk.LEFT, padx=10)
            self.image_out_button = tk.Button(self.image_button_frame, image=zoom_out_icon,
                                              command=partial(self.image_borders, "vout"), bd=0, width=35, height=35)
            self.image_out_button.bind("<Enter>",self.enter_out)
            self.image_out_button.bind("<Leave>", self.leave_out)
            self.image_out_button.pack(side=tk.LEFT)
            self.image_in_button = tk.Button(self.image_button_frame, image=zoom_in_icon,
                                             command=partial(self.image_borders, "vin"), bd=0, width=35, height=35)
            self.image_in_button.bind("<Enter>",self.enter_in)
            self.image_in_button.bind("<Leave>", self.leave_in)
            self.image_in_button.pack(side=tk.LEFT)
            self.image_right_button = tk.Button(self.image_button_frame, image=right_icon,
                                                command=partial(self.image_borders, "vright"), bd=0, width=70, height=35)
            self.image_right_button.bind("<Enter>",self.enter_right)
            self.image_right_button.bind("<Leave>", self.leave_right)
            self.image_right_button.pack(side=tk.LEFT, padx=10)

            image_data_bytes = base64.b64decode(export_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.export_image_icon = ImageTk.PhotoImage(image)


            image_data_bytes = base64.b64decode(export_bt_w)
            image = Image.open(BytesIO(image_data_bytes))
            self.export_image_icon_w = ImageTk.PhotoImage(image)

            self.export_image_button = tk.Button(self.image_button_frame, image=self.export_image_icon,
                                                command=self.take_canvas_screenshot, bd=0)
            self.export_image_button.bind("<Enter>",self.enter_export_image)
            self.export_image_button.bind("<Leave>", self.leave_export_image)
            self.export_image_button.pack(side=tk.LEFT, padx=15)


            tk.Label(self.image_options, text="Image Alignment").place(x = 175, y=10, anchor="center")

            tk.Label(self.image_options, text="Frame width (pixels):").place(x = 5 +20, y = 10+20, anchor = "w")
            self.frame_width_entry = tk.Entry(self.image_options, width=10)
            self.frame_width_entry.place(x = 345 -20, y = 10+20, anchor = "e")
            self.frame_width_entry.insert(0,"8")

            tk.Label(self.image_options, text="Image center horizontal offset (pixels):").place(x = 5 +20, y = 35+20, anchor = "w")
            self.x_offset_entry = tk.Entry(self.image_options, width=10)
            self.x_offset_entry.place(x = 345-20, y = 35+20, anchor = "e")
            self.x_offset_entry.insert(0,"0")

            tk.Label(self.image_options, text="Frame height (pixels):").place(x = 5 +20, y = 60+20, anchor = "w")
            self.frame_height_entry = tk.Entry(self.image_options, width=10)
            self.frame_height_entry.place(x = 345-20, y = 60+20, anchor = "e")

            tk.Label(self.image_options, text="Image center vertical offset (pixels):").place(x = 5 +20, y = 85+20, anchor = "w")
            self.y_offset_entry = tk.Entry(self.image_options, width=10)
            self.y_offset_entry.place(x = 345-20, y = 85+20, anchor = "e")
            self.y_offset_entry.insert(0, "0")

            self.direction = tk.IntVar()

            tk.Label(self.image_options, text="Race direction:").place(x=5 + 20, y=110 + 20, anchor="w")
            self.running_dir_1 = tk.Radiobutton(self.image_options, text="Left to Right", variable=self.direction, value=0)
            self.running_dir_2 = tk.Radiobutton(self.image_options, text="Right to Left", variable=self.direction, value=1)
            self.running_dir_1.place(x=210, y=110 + 20, anchor = "e")
            self.running_dir_2.place(x=320, y=110 + 20,anchor = "e")
            self.direction.set(0)

            self.image_dimensions = tk.Label(self.image_options, text = "Image dimensions: 0x0")
            self.image_dimensions.place(x = int(350/2), y = 110 + 40, anchor = "center")

            self.preview_canvas_width = 300
            self.preview_canvas_height = 500

            self.preview_canvas = tk.Canvas(self.image_options, width = 300, height = 500, bg = "black", highlightthickness=0)
            self.preview_canvas.place(x = 175, y = 150+20, anchor = "n")
            self.preview_canvas.bind("<MouseWheel>", self.change_frame_width)
            self.preview_canvas.bind("<Button-1>", self.change_frame_on_fc)
            self.preview_canvas.bind("<ButtonRelease-1>", self.change_frame_off_fc)
            self.change_frame_on = False
            self.preview_canvas.bind("<Motion>", self.change_frame_pos)
            self.preview_canvas.bind("<Return>", self.update_image)

            self.root.bind("<Control_L>", self.on_ctrl_press)
            self.root.bind("<KeyRelease-Control_L>", self.on_ctrl_release)
            self.root.bind("<Control_R>", self.on_ctrl_press)
            self.root.bind("<KeyRelease-Control_R>", self.on_ctrl_release)

            #image_data_bytes = base64.b64decode(preview_bt)
            #image = Image.open(BytesIO(image_data_bytes))
            #self.preview_icon = ImageTk.PhotoImage(image)

            #self.preview_button = tk.Button(self.image_options,image = self.preview_icon, bd = 0, command = self.preview_frame)
            #self.preview_button.place(x = 70, y = 660+20, anchor = "nw")
            #self.preview_button.config(state = "disabled")


            image_data_bytes = base64.b64decode(update_image_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.update_image_icon = ImageTk.PhotoImage(image)

            self.image_update_button = tk.Button(self.image_options, image = self.update_image_icon, bd = 0,  command=self.update_image)
            self.image_update_button.place(x=325, y=660 +20, anchor="ne")
            self.image_update_button.config(state="disabled")

            tk.Label(self.image_options, text = "Rotation angle:").place(x = 25, y=660 + 25, anchor = "nw")
            self.angle_entry = tk.Entry(self.image_options, width = 4)
            self.angle_entry.place(x = 130, y = 660 + 25, anchor = "n")
            self.angle_entry.insert(0,"0")
            self.angle_entry.bind("<MouseWheel>", self.change_angle)


            points = [250,10,345,10,345,725,5,725,5,10,100,10]
            self.image_options.create_line(points, fill = "#444444")

            self.audio_canvas.bind("<Button-1>", self.on_click_audio)
            self.audio_canvas.bind("<MouseWheel>", self.handle_scroll_audio)
            self.audio_canvas.bind("<Motion>", self.on_mouse_motion_audio)

            self.image_middle = 0.5

            self.scale_height = 30

            self.cursorline = self.audio_canvas.create_line(self.audio_canvas.winfo_width() / 2, 0, self.audio_canvas.winfo_width() / 2,
                                                            self.audio_canvas.winfo_height(),
                                                            fill="white")

            self.start_cursor = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                              fill="red")

            self.red_gun = self.audio_canvas.create_image(99999,
                                                          self.audio_canvas.winfo_height() - self.scale_height - 30,
                                                          anchor=tk.S,image = red_gun_icon)
            self.red_gun2 = self.audio_canvas.create_image(99999,
                                                           self.scale_height + 30, anchor=tk.N,
                                                           image=red_gun_icon)

            #self.video_label = tk.Label(self.image_frame)
            #self.video_label.pack()

            self.audio_canvas.create_line(0, int(self.audio_canvas.winfo_height() / 2),
                                          int(self.audio_canvas.winfo_width()),
                                          int(self.audio_canvas.winfo_height() / 2), fill="white")

            self.audio_zoom_x = 1
            self.audio_zoom_y = 1
            self.abort = False
            self.image_in_progress = False


            self.audiostartrel = 0
            self.audioendrel = 1

            self.image_zoom_x = 1
            self.image_center = 0.5
            self.imagestartrel = 0
            self.imageendrel = 1

            self.playback_cursor = None

            self.line_thickness = 50
            self.image_offset_x = 0
            self.image_offset_upper = 0
            self.image_offset_lower = 0

            self.playing = False

            self.timeline_image = None
            self.image = None
            self.image_resized = None
            self.zoomed_images = []

            self.image_start_time_full = 0
            self.image_end_time_full = 0

            self.image_start_time = 0
            self.image_end_time = 0

            self.max_image_zoom = 10

            self.start_entry = None
            self.end_entry = None
            self.audio = None
            self.similarities = None


            self.image_canvas.bind("<Button-1>", self.on_click_image)
            self.image_canvas.bind("<MouseWheel>", self.handle_scroll_image)
            self.image_canvas.bind("<Motion>", self.on_mouse_motion_image)
            self.image_canvas.bind("<Button-3>", self.display_frames)

            self.hash_line = self.image_canvas.create_line(self.image_canvas.winfo_width() // 2, 0,
                                                           self.image_canvas.winfo_width() // 2,
                                                           self.image_canvas.winfo_height(),
                                                           fill=self.hashline_color)

            self.hash_line_hor = self.image_canvas.create_line(self.image_canvas.winfo_width() // 2 + 5,
                                                               self.image_canvas.winfo_height() // 2,
                                                               self.image_canvas.winfo_width() // 2 + 5,
                                                               self.image_canvas.winfo_height() // 2,
                                                               fill=self.hashline_color)

            self.results = []
            self.deleted_results = []
            self.results_sorted = None

            self.status_text = None


            self.progress_bar_bg = None
            self.progress_bar = None

            self.status_text_left = None

            self.root.configure(bg="#555555")

            #self.results_table()
            #self.create_edit_controls()
            self.table = EditableTable(self.results_frame,self)

            self.current_time_audio = 0

            self.default_athlete =  {"Lane":"nan","ID":"nan","Name":"nan","Date of Birth": "nan", "Affiliation":"nan","License":"nan","Time":"nan","Place": "nan", "priv_id":0}
            self.default_parameters = ["Lane","ID","Name","Date of Birth","Affiliation","License","Time","Place"]
            self.background_change = False

            self.frames_ready = False
            self.timeline_ready = False
            self.framess = None

            self.view_pf_var = False
            self.update_image_var = False
            self.excel_import = False

            self.frame_interpolation = False
            self.interpolation_factor = 1

            polygon_points = [self.status.winfo_width() - 600, 5, self.status.winfo_width() - 600 + 0 * 600, 5,
                              self.status.winfo_width() - 600 + 0 * 600, self.status.winfo_height() - 5,
                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]
            self.progress_bar = self.status.create_polygon(polygon_points, fill="#555555")
            self.status.tag_lower(self.progress_bar)
            self.ctrl_pressed = False
            self.paused_time = 0

            self.rect_width, self.rect_height = 30, 50
            self.decimals = 2
            self.capture_opened = False
            self.current_gunshot = 0
        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="initialization")

    def enter_play(self,event):
        if self.playing == True:
            self.play_button.config(image= self.pause_bt_w)
        else:
            self.play_button.config(image=self.play_bt_w)

    def leave_play(self,event):
        if self.playing == True:
            self.play_button.config(image= self.pause_bt)
        else:
            self.play_button.config(image=self.play_bt)
    def enter_stop(self, event):
        self.stop_button.config(image=self.stop_bt_w)

    def leave_stop(self, event):
        self.stop_button.config(image=self.stop_bt)

    def enter_new_instance(self,event):
        self.new_instance_button.config(image = self.add_instance_icon_w)

    def leave_new_instance(self,event):
        self.new_instance_button.config(image = self.add_instance_icon)

    def enter_export_image(self,event):
        self.export_image_button.config(image = self.export_image_icon_w)

    def leave_export_image(self,event):
        self.export_image_button.config(image = self.export_image_icon)

    def enter_video_import(self,event):
        self.import_video_button.config(image = self.import_video_icon_w)

    def leave_video_import(self,event):
        self.import_video_button.config(image = self.import_video_icon)

    def enter_undo(self,event):
        self.image_undo_button.config(image = undo_icon_w)

    def leave_undo(self, event):
        self.image_undo_button.config(image=undo_icon)

    def enter_redo(self, event):
        self.image_redo_button.config(image=redo_icon_w)

    def leave_redo(self, event):
        self.image_redo_button.config(image=redo_icon)

    def enter_left(self, event):
        self.image_left_button.config(image=left_icon_w)
        self.audio_left_button.config(image=left_icon_w)

    def leave_left(self, event):
        self.image_left_button.config(image=left_icon)
        self.audio_left_button.config(image=left_icon)

    def enter_right(self, event):
        self.image_right_button.config(image=right_icon_w)
        self.audio_right_button.config(image=right_icon_w)

    def leave_right(self, event):
        self.image_right_button.config(image=right_icon)
        self.audio_right_button.config(image=right_icon)

    def enter_in(self, event):
        self.image_in_button.config(image=zoom_in_icon_w)
        self.audio_in_button.config(image=zoom_in_icon_w)

    def leave_in(self, event):
        self.image_in_button.config(image=zoom_in_icon)
        self.audio_in_button.config(image=zoom_in_icon)

    def enter_out(self, event):
        self.image_out_button.config(image=zoom_out_icon_w)
        self.audio_out_button.config(image=zoom_out_icon_w)

    def leave_out(self, event):
        self.image_out_button.config(image=zoom_out_icon)
        self.audio_out_button.config(image=zoom_out_icon)


    """
    i said that all instances are connected to a secret root and that main root
    is closed after the last single frame is closed.
    this condition is checked via the global var total_instances
    """
    def new_instance(self):
        global total_instances
        total_instances += 1
        video_recorder = Instance(root)
        video_recorder.root.mainloop()

    def on_closing(self):
        global total_instances
        total_instances -= 1
        if total_instances == 0:
            global root
            root.destroy()
        else:
            self.root.destroy()


    """
    after a video is selected, 
    its audio is imported first.
    """
    def analyze_audio(self):
        #self.root.iconbitmap("images/cross.ico")
        try:
            video_file = filedialog.askopenfilename(title="Import Video")

            self.video_file = video_file

            #print(self.video_file)

            if self.status_text_left:
                self.status.itemconfig(self.status_text_left, text="Extracting audio...")

            else:
                self.status_text_left = self.status.create_text(7, self.status.winfo_height() // 2,
                                                                text="Extracting audio...", font=(self.font, 15),
                                                                anchor="w", fill="#00FF00")

            #self.cap_timeline = cv2.VideoCapture(self.video_file)
            #fps = self.cap_timeline.get(cv2.CAP_PROP_FPS)
            #frame_count = int(self.cap_timeline.get(cv2.CAP_PROP_FRAME_COUNT))
            #duration = frame_count / fps
            clip = VideoFileClip(self.video_file)
            self.audio = clip.audio

            self.audio.write_audiofile("temporary.wav", logger=DummyLogger())

            self.audio_data, self.audiosamplerate = sf.read("temporary.wav")

            self.duration = len(self.audio_data[:, 1]) / self.audiosamplerate

            def after_interval_window():
                if self.status_text:
                    self.status.itemconfig(self.status_text, text="Audio extracted.")
                else:
                    self.status_text = self.status.create_text(self.status.winfo_width() - 7,
                                                               self.status.winfo_height() // 2,
                                                               text="Audio extracted.", anchor="e", fill="#00FF00",
                                                               font=self.font)
                self.visualise_audio(self.audio_data, self.audiosamplerate, 0, 1)

                # self.create_image()

                self.status.itemconfig(self.status_text_left,
                                       text="Title: " + str(self.video_file).split("/")[-1].split(".")[0])
                self.root.title(str(self.video_file).split("/")[-1].split(".")[0] + " - OpenPhotoFinish")
                if self.excel_import == False:
                    self.table.change_title(
                        str(self.video_file).split("/")[-1].split(".")[0] + ", Wind: " + str(
                            self.wind_var) + " m/s")

                self.play_button.config(state="normal")
                self.image_button.config(state="normal")
                self.current_time_audio = 0
                self.paused_time = 0
                self.start_time = 0
                self.similarities = None

            audio_interval_window = tk.Toplevel(self.root)
            audio_interval_window.title("Audio Interval")
            audio_interval_window.wm_iconphoto(False, self.main_icon)
            tk.Label(audio_interval_window, text = "Import audio clip untill:").pack(pady = 5)

            interval_entry_frame = tk.Frame(audio_interval_window)
            interval_entry_frame.pack()
            self.interval_entry_m = tk.Entry(interval_entry_frame, width = 5)
            self.interval_entry_m.pack(side = tk.LEFT)
            tk.Label(interval_entry_frame, text = "m   ").pack(side = tk.LEFT)
            self.interval_entry_s = tk.Entry(interval_entry_frame, width=5)
            self.interval_entry_s.pack(side = tk.LEFT)
            tk.Label(interval_entry_frame, text="s").pack(side=tk.LEFT)

            interval_button_frame = tk.Frame(audio_interval_window)
            interval_button_frame.pack(pady = 5)

            def clip_interval():
                end_time = float(self.interval_entry_m.get()) + float(self.interval_entry_s.get())
                self.audio_data= self.audio_data[:int(end_time*self.audiosamplerate)]
                after_interval_window()
                audio_interval_window.destroy()

            def clip_whole():
                after_interval_window()
                audio_interval_window.destroy()

            tk.Button(interval_button_frame, text = "Import entire audio", command = clip_whole).pack(side = tk.LEFT, padx = 3)
            tk.Button(interval_button_frame, text="Import untill specified time", command=clip_interval).pack(
                side=tk.LEFT,padx = 3)

            audio_interval_window.mainloop()


        except Exception as e:
            print(e)
            error_message(e=e, trace=traceback.format_exc(), error_at="analyse_audio()")


    def capture(self):
        try:
            if self.capture_opened == False:
                self.capture_opened = True
            else:
                self.capture_window.iconify()
                self.capture_window.deiconify()
                return


            self.capture_window = tk.Toplevel(self.root)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.capture_frame = tk.Frame(self.capture_window, height = 40)
            self.capture_frame.pack(side = tk.TOP, fill = "x")
            def onclose():
                self.capture_opened = False
                self.capture_window.destroy()

            self.capture_window.wm_protocol("WM_DELETE_WINDOW", onclose)

            window_width = 350
            window_height = 400
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            self.capture_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            self.capture_window.wm_iconphoto(False, self.main_icon)
            self.capture_window.resizable(False, True)
            self.capture_window.title("Capture Interval")


            self.notebook_cap = ttk.Notebook(self.capture_window, style='lefttab.TNotebook')
            self.notebook_cap.pack(expand=True, fill='both')
            self.capture_window1 = tk.Frame(self.notebook_cap)
            self.capture_window2 = tk.Frame(self.notebook_cap)
            self.capture_window3 = tk.Frame(self.notebook_cap)

            image_data_bytes = base64.b64decode(captures_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.captures_bt = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(laps_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.laps_bt = ImageTk.PhotoImage(image)

            image_data_bytes = base64.b64decode(board_bt)
            image = Image.open(BytesIO(image_data_bytes))
            self.board_bt = ImageTk.PhotoImage(image)

            self.notebook_cap.add(self.capture_window1, image = self.captures_bt)
            self.notebook_cap.add(self.capture_window2, image = self.laps_bt)
            self.notebook_cap.add(self.capture_window3, image = self.board_bt)



            self.capture_time_text = tk.Label(self.capture_frame, text = "0.0")
            self.capture_time_text.place(x = 200, y = 25, anchor = "center")
            self.interval_widgets = []
            self.interval_start = None
            self.reflex = 0.25
            self.board_opened = False
            self.lap_times = []
            self.lap_widgets = []
        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="capture()")


        def display_captures():
            if self.interval_widgets:
                for i in self.interval_widgets:
                    for j in i:
                        j.destroy()

            for i in range(len(self.captures)):
                def delete_capture(j):
                    del self.captures[j]
                    display_captures()

                def apply_interval(j):
                    self.image_start_entry_minute.delete(0, tk.END)
                    self.image_start_entry_minute.insert(0, int(self.captures[j][2]//60))
                    self.image_start_entry_second.delete(0, tk.END)
                    self.image_start_entry_second.insert(0, format_time(self.captures[j][2] % 60))
                    self.image_end_entry_minute.delete(0, tk.END)
                    self.image_end_entry_minute.insert(0, int(self.captures[j][3] // 60))
                    self.image_end_entry_second.delete(0, tk.END)
                    self.image_end_entry_second.insert(0, format_time(self.captures[j][3] % 60))

                start_text = tk.Label(self.capture_window1, text=self.captures[i][0])
                start_text.place(x=5, y=30 * i +20, anchor="w")

                end_text = tk.Label(self.capture_window1, text=self.captures[i][1])
                end_text.place(x=105, y=30 * i+20, anchor="w")

                apply_interval_button = tk.Button(self.capture_window1, text="Apply", command=partial(apply_interval, i))
                apply_interval_button.place(x=200, y=30 * i+20, anchor="w")

                delete_capture_button = tk.Button(self.capture_window1, text="Delete",
                                                  command=partial(delete_capture, i))
                delete_capture_button.place( x = 250, y = 30*i+20, anchor = "w")



                self.interval_widgets.append([start_text, end_text, delete_capture_button, apply_interval_button])



        def display_laps():
            if self.lap_widgets:
                for i in self.lap_widgets:
                    for j in i:
                        j.destroy()

            for i in range(len(self.lap_times)):
                def delete_lap(j):
                    del self.lap_times[j]
                    display_laps()

                lap_text = tk.Label(self.capture_window2, text= "("+str(i+1)+") "+self.lap_times[i][1])
                lap_text.place(x=5, y=30 * i +20, anchor="w")


                delete_lap_button = tk.Button(self.capture_window2, text="Delete",
                                                  command=partial(delete_lap, i))
                delete_lap_button.place( x = 250, y = 30*i+20, anchor = "w")



                self.lap_widgets.append([lap_text, delete_lap_button])

        if self.captures:
            display_captures()

        self.stop_timer = True
        self.timer_running = False


        def start_timer():
            if self.timer_running == False:
                self.timer_running = True
                self.stop_timer = False
                self.capture_start = time.time() - self.reflex - (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))
                self.start_timer_button.config(text = "Lap")
                def timer_thread():
                    while True:
                        self.capture_time_text.config(text = format_time(time.time()-self.capture_start, decimals = 1))
                        time.sleep(0.05)
                        if self.stop_timer == True:
                            break
                    return
                threading.Thread(target = timer_thread).start()
            else:
                self.lap_times.append((time.time()-self.capture_start, format_time(time.time()-self.capture_start)))
                display_laps()
                print(self.lap_times)
                return

        def stop_timer():
            self.timer_running = False
            self.stop_timer = True
            self.start_timer_button.config(text="Start")
            self.capture_time_text.config(text="0.0")
            time.sleep(0.3)
            self.capture_time_text.config(text="0.0")

        def capture_interval():
            if self.interval_start == None:
                self.interval_start = time.time()-self.capture_start
                self.timer_button.config(bg = "#00FF00",fg = "#FF0000")
            else:
                self.captures.append((format_time(self.interval_start), format_time(time.time()-self.capture_start), self.interval_start,   time.time()-self.capture_start))
                self.interval_start = None
                self.timer_button.config(bg="#222222", fg="#FFFFFF")
                display_captures()
                print(self.captures)

        def decrease_font():
            self.timer_font_size = int(self.timer_font_size / 1.1)
            self.big_timer_label.config(font=("calibri", self.timer_font_size))

        def increase_font():
            self.timer_font_size = int(self.timer_font_size * 1.1)
            self.big_timer_label.config(font=("calibri", self.timer_font_size))

        self.timer_button_frame = tk.Frame(self.capture_window3, height=10)
        self.timer_button_frame.pack(anchor=tk.N)
        self.timer_font_minus = tk.Button(self.timer_button_frame, text="-", width=5, command=decrease_font)
        self.timer_font_plus = tk.Button(self.timer_button_frame, text="+", width=5, command=increase_font)
        self.timer_font_minus.pack(side=tk.LEFT)
        self.timer_font_plus.pack(side=tk.LEFT)

        def big_timer_display_thread():
            while True:
                try:
                    try:
                        disp_canvas.destroy()
                    except:
                        pass
                    font_size = int(self.big_timer_label.cget("font").split()[1])
                    wind_width = self.big_timer.winfo_width()
                    wind_height = self.big_timer.winfo_height()
                    if wind_width >= wind_height:
                        disp_width = 300
                        disp_height = int(disp_width*wind_height/wind_width)
                    else:
                        disp_height = 300
                        disp_width = int(disp_height * wind_width / wind_height)
                    print(disp_height,disp_width,font_size,self.big_timer_label.cget("text"),int(font_size*disp_width/self.big_timer.winfo_width()))
                    disp_canvas = tk.Canvas(self.capture_window3,width = disp_width, height = disp_height, bg = "black", bd = 0, highlightthickness = 0)
                    disp_canvas.pack()

                    disp_canvas.create_text(int(disp_width/2),int(disp_height/2), text = self.big_timer_label.cget("text"),font=("calibri", int(font_size*disp_width/self.big_timer.winfo_width())), anchor = "center", fill = "white")
                    """
                    disp_canvas.create_text(int(disp_width / 2), int(disp_height / 2),
                                        text="test",
                                        font=("calibri", int(font_size * disp_width / self.big_timer.winfo_width())),
                                        anchor="center")

                    """
                except Exception as e:
                    print(e)
                time.sleep(0.3)

        threading.Thread(target = big_timer_display_thread).start()

        def big_timer(event):

            if self.board_opened == False:
                self.board_opened = True
            else:
                self.big_timer.iconify()
                self.big_timer.deiconify()
                return

            self.big_timer = tk.Toplevel(self.capture_window)
            self.big_timer.state("zoomed")
            self.big_timer.title("OpenPhotoFinish Board")

            def onnclose():
                self.board_opened = False
                self.big_timer.destroy()

            self.big_timer.wm_protocol("WM_DELETE_WINDOW", onnclose)


            self.big_timer.configure(bg='black')
            self.big_timer.config(bg='black')
            #self.big_timer.wm_attributes("-topmost", True)
            self.big_timer.wm_iconphoto(False, self.main_icon)
            self.timer_font_size = 150
            self.big_timer_label = tk.Label(self.big_timer, text = self.capture_time_text.cget("text"), font = ("calibri",self.timer_font_size))
            self.big_timer_label.configure(bg='black')
            self.big_timer_label.config(bg='black')

            self.big_timer_label.pack(expand = True)
            def big_timer_thread():
                while True:
                    self.big_timer_label.config(text=self.capture_time_text.cget("text"))
                    time.sleep(0.05)
                    if self.stop_timer == True:
                        self.big_timer_label.config(text="0.0")
                        break
                    self.big_timer_label.config(text=self.capture_time_text.cget("text"))
                return
            threading.Thread(target = big_timer_thread).start()
            def results_thread():
                while True:
                    if self.results_sorted and self.stop_timer == True:
                        text = ""
                        for i in range(len(self.results_sorted)):
                            if i == 3:
                                break
                            text += "("+str(i+1)+") "+format_time(self.results_sorted[i])+"\n"
                        text = text[:-1]
                        self.big_timer_label.config(text=text)

                    else:
                        threading.Thread(target=big_timer_thread).start()
                        while True:
                            if self.stop_timer == True:
                                break
                            time.sleep(1)
                    time.sleep(1)
                return
            threading.Thread(target = results_thread).start()
            self.big_timer.mainloop()

        self.capture_time_text.bind("<Double-1>", big_timer)

        self.timer_button = tk.Button(self.capture_frame, text = "Capture", command = capture_interval)
        self.timer_button.place(x = 340, y = 25, anchor = "e")

        self.start_timer_button = tk.Button(self.capture_frame, text="Start", command=start_timer)
        self.start_timer_button.place(x=60, y=25, anchor="w")

        self.stop_timer_button = tk.Button(self.capture_frame, text="Stop", command=stop_timer)
        self.stop_timer_button.place(x=120, y=25, anchor="w")

        self.capture_window.mainloop()

    def start_sample(self):
        return

    # play the audio of the video

    def play(self):
        try:
            #this function also pauses the audio if evoked while playing.
            if self.playing == True:
                self.play_button.config(image= self.play_bt_w)
                sd.stop()
                self.playing = False
                self.paused_time = self.current_time_audio
            else:
                self.play_button.config(image= self.pause_bt_w)
                self.audio_canvas.delete(self.playback_cursor)
                self.playback_deleted = True
                print(self.current_time_audio)
                def play_audio():
                    sd.play(self.audio_data[:,1][int(len(self.audio_data[:,1])*self.current_time_audio/self.duration):], samplerate=self.audiosamplerate)
                    sd.wait()

                self.playing = True
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()


            #the cursor progresses as the audio plays
            def playback_cursor():
                self.playback_start = time.time()

                while self.playing == True:

                    #frama rate of the cursor is 30 fps
                    time.sleep(1/30)

                    #time_elapsed = time.time()- self.playback_start
                    #self.audio_canvas.delete(self.playback_cursor)
                    #calculates how much seconds has passed after the playback_cursor function is evoked.
                    self.current_time_audio = (time.time() - self.playback_start) + self.paused_time

                    #sets the position of the cursor on the canvas according to the time passed.
                    self.playback_cursor_position = self.audio_canvas.winfo_width() * (
                                self.current_time_audio / self.duration - self.audiostartrel) / (self.audioendrel - self.audiostartrel)
                    #print(self.playback_cursor_position)

                    #the first cursor is created when the play is evoked, the next cursors are just shifted versions.
                    if self.playback_deleted == True:
                        self.playback_cursor = self.audio_canvas.create_line(self.playback_cursor_position, 0,
                                                                             self.playback_cursor_position,
                                                                             self.audio_canvas.winfo_height(),
                                                                             fill="green")
                        self.playback_deleted = False
                    else:
                        self.audio_canvas.coords(self.playback_cursor, self.playback_cursor_position, 0,
                                                                    self.playback_cursor_position,
                                                                    self.audio_canvas.winfo_height())

                    time_delta = self.current_time_audio - self.start_time

                    self.status.itemconfig(self.status_text_left,text = "Video time: "+format_time(self.current_time_audio)+"    Race time: "+format_time(time_delta))

            cursor_thread = threading.Thread(target=playback_cursor)
            cursor_thread.start()

        except Exception as e:
            error_message(e=e, trace=traceback.format_exc(), error_at="play()")


    def stop(self):
        self.playing = False
        sd.stop()
        time.sleep(1 / 30)
        self.current_time_audio = self.start_time
        self.audio_canvas.delete(self.playback_cursor)
        self.playback_deleted = True
        self.play_button.config(image= self.play_bt)
        self.status.itemconfig(self.status_text_left,
                               text="Gun shot at: " + format_time(self.start_time))
        self.paused_time = self.start_time


    #clicking on the audio will determine a start time for the race.
    def on_click_audio(self,event):
        if event == 0:
            print("event 0")
        elif event == 1:
            print("event")

        if not self.audio:
            return

        elif self.playing == False:
            clicked = self.mousex_rel*len(self.audio_data[:,1])/self.audiosamplerate
            print(clicked)
            self.audio_canvas.delete(self.start_cursor)
            self.audio_canvas.delete(self.red_gun)
            self.audio_canvas.delete(self.red_gun2)
            self.start_cursor = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                    fill="red")

            self.red_gun = self.audio_canvas.create_image(self.mousex, self.audio_canvas.winfo_height()-self.scale_height-30, anchor = tk.S, image = red_gun_icon)
            self.red_gun2 = self.audio_canvas.create_image(self.mousex,
                                                        self.scale_height + 30, anchor = tk.N,
                                                          image=red_gun_icon)

            self.start_cursor_x = self.mousex_rel
            self.start_time = clicked
            self.start_cursor_position = self.audio_canvas.winfo_width()*(self.start_time/self.duration - self.audiostartrel)/(self.audioendrel-self.audiostartrel)
            self.current_time_audio = self.start_time
            self.paused_time = self.start_time

        self.status.itemconfig(self.status_text_left,
                               text="Gun shot at: " + format_time(self.start_time))

        return


    def save_gun_sample(self):
        #print(int(self.start_time*self.audiosamplerate),int(self.start_time*self.audiosamplerate) + int(self.audiosamplerate/2))
        chunk = self.audio_data[:,1][int(self.start_time*self.audiosamplerate):int(self.start_time*self.audiosamplerate) + 128]
        fourier = abs(np.fft.fft(chunk))[:len(chunk)]
        frequencies = np.linspace(0,int(self.audiosamplerate/2), len(chunk))
        file_name = filedialog.asksaveasfilename(filetypes=(("Python Files", "*.py"), ("All Files", "*.*")))
        if not file_name.endswith(".py"):
            file_name += ".py"
        thefile = open(file_name,"w")
        thefile.write("array = [")
        for i in range(len(fourier)-1):
            thefile.write(str(fourier[i])+", ")
        thefile.write(str(fourier[-1])+"]")
        thefile.close()
        from matplotlib import pyplot as plt
        #plt.plot(frequencies, fourier)
        #plt.show()

    def find_gun(self):
        def find_gun_thread():
            # Open a file dialog to select a Python file
            file_path = filedialog.askopenfilename(
                title="Select a Python file",
                filetypes=[("Python Files", "*.py")],
                defaultextension=".py"
            )

            if file_path:
                # Use a simple exec to read the contents of the file
                with open(file_path, 'r') as file:
                    file_content = file.read()

                    # Execute the file's content in a local context
                    local_context = {}
                    exec(file_content, {}, local_context)

                    # Assuming the file contains a list called 'my_list'
                    my_list = local_context.get('array')
                    if my_list is not None:
                        print("Loaded list:", my_list)
                    else:
                        print("No 'my_list' found in the file.")
            print(my_list)
            my_list = np.array(my_list)
            similarities = []
            audioo = np.array(self.audio_data[:, 1])
            chunk_size = 128
            for i in range(len(audioo[:-len(my_list)])):
                chunk = audioo[i:i+ chunk_size]
                fourier = np.abs(np.fft.fft(chunk))[:len(chunk)]
                #frequencies = np.linspace(0, int(self.audiosamplerate / 2), len(chunk))
                #similarity = sum(((my_list*fourier[1]/my_list[1]-fourier)**2))
                similarity = np.sum(((my_list - fourier) ** 2))
                similarities.append(similarity)
                if i%20000 == 0:
                    polygon_points = [self.status.winfo_width() - 600, 5,
                                      self.status.winfo_width() - 600 + int(((i + 1) / len(self.audio_data[:,1][:-len(my_list)])) * 600),
                                      5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.audio_data[:,1][:-len(my_list)])) * 600),
                                      self.status.winfo_height() - 5,
                                      self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                    self.status.coords(self.progress_bar, polygon_points)
                    self.status.itemconfig(self.status_text, text="Analysing audio: " + str(
                        int(100 * (i + 1) / len(self.audio_data[:,1][:-len(my_list)]))) + " %", font=self.font)
            print("A")
            startt = similarities.index(sorted(similarities)[0])
            print("B")
            default_similarity = np.sum(((my_list - np.array([0]*len(my_list))) ** 2))
            self.start_time = startt/self.audiosamplerate
            self.similarities = np.array(similarities)
            self.similarities = default_similarity - self.similarities
            #self.similarities = np.log(np.exp(-np.array(similarities))+1)/np.log(2)
            self.similarities = (self.similarities)/np.amax(self.similarities)
            self.handle_scroll_audio()
            print("C")
            #plt.plot(similarities)
            #plt.show()
            print(startt, self.start_time)
        threading.Thread(target = find_gun_thread).start()

    def next_gunshot(self):
        if self.current_gunshot < len(self.gunshots):
            self.current_gunshot += 1
            startt = self.gunshots[self.current_gunshot]

            self.start_time = startt / self.audiosamplerate
            self.handle_scroll_audio()
        return

    def previous_gunshot(self):
        if self.current_gunshot > 0:
            self.current_gunshot -= 1
            startt = self.gunshots[self.current_gunshot]

            self.start_time = startt / self.audiosamplerate
            self.handle_scroll_audio()
        return

    #moving the mouse will move the cursor.
    def on_mouse_motion_audio(self, event):
        try:
            self.mousex, self.mousey = event.x, event.y
            self.mousex_oncanvas = self.mousex/self.audio_canvas.winfo_width()
            self.mousex_rel = self.image_middle + (self.mousex_oncanvas-0.5)*2**(1-self.audio_zoom_x)
            #print(self.mousex_rel)

            self.audio_canvas.delete(self.cursorline)
            self.cursorline = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                        fill="white")
            clicked = self.mousex_rel * len(self.audio_data[:, 1]) / self.audiosamplerate
            current_time_str = str(int(clicked//60)) + ":" +str((int((clicked%60)*1000+0.5))/1000)

            self.status.itemconfig(self.status_text, text = current_time_str)
        except:
            pass

    # visualises the audio signal
    # evoked after the audio is imported, and each time zoom level or position is changed via scroll
    def visualise_audio(self,audio, sr, start, end):

        data = audio[:,1][int(start*len(audio[:,1])):int(end*len(audio[:,1]))]

        self.audio_canvas.delete("all",)
        self.playback_deleted = True
        #print(int(start*len(audio[:,1])),int(end*len(audio[:,1])),"::",int(start*len(audio[:,1]))/len(audio[:,1]),int(end*len(audio[:,1]))/len(audio[:,1]))


        #the below part is to determine an amout of increment (powers of 10 in seconds) on the scale
        duration = len(audio[:,1])/sr
        level = np.round(np.log(duration)/np.log(10))
        increments = 10**level
        while True:
            if increments*15 < duration*(end-start):
                break
            else:
                increments /= 10

        #print(duration, start, end, increments)
        starting = duration*start - (duration*start)%increments + increments
        starting = int(starting/increments)
        starting *= increments

        ending =  duration*end - (duration*end)%increments
        #print("operation:", starting,ending, increments)
        thearray = np.arange(starting, ending+10*increments, increments)
        locations = self.audio_canvas.winfo_width()*(thearray/duration - start)/(end-start)


        loc_points = []
        loc_points2 = []
        grids = []
        scaleY = self.audio_canvas.winfo_height()-50
        #locations for the ticks of the scale on the canvas.
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i])
            loc_points.append(scaleY+20)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY+20)

            loc_points2.append(locations[i])
            loc_points2.append(50)
            loc_points2.append(locations[i])
            loc_points2.append(30)
            loc_points2.append(locations[i+1])
            loc_points2.append(30)


            grids.append(locations[i])
            grids.append(0)
            grids.append(locations[i])
            grids.append(scaleY + 20)
            grids.append(locations[i + 1])
            grids.append(scaleY + 20)


            if abs(thearray[i]%(increments*10)) < increments:
                thestr = str(int(thearray[i] / increments) * increments)

                if thearray[i] > 60:
                    #print(thearray[i])
                    seconds = thearray[i]%60
                    minutes = thearray[i] // 60
                    seconds = str(int(seconds / increments) * increments)
                    thestr = str(int(minutes))+":"+seconds
                    #print(thestr)
                if "." in thestr:
                    thestr = thestr+"00000000"
                    decimal = thestr.find(".")
                    thestr = thestr[:decimal+int(1-np.log(increments)/np.log(10))]

                if thestr[-1] == ".":
                    thestr = thestr+"00"

                elif increments > 0.005 and increments < 0.05:
                    thestr = thestr+"0"


                self.audio_canvas.create_text(locations[i],scaleY+40, text = thestr, fill = "white")
                self.audio_canvas.create_line(locations[i],scaleY-20,locations[i],scaleY+20, fill="white")

                self.audio_canvas.create_text(locations[i], 10, text=thestr, fill="white")
                self.audio_canvas.create_line(locations[i], 70, locations[i], 30, fill="white")

        grids = self.audio_canvas.create_line(grids, fill="#333333")
        zero_line = self.audio_canvas.create_line(0, int(self.audio_canvas.winfo_height() / 2),
                                      int(self.audio_canvas.winfo_width()),
                                      int(self.audio_canvas.winfo_height() / 2), fill="#333333")
        self.audio_canvas.tag_lower(zero_line)
        self.audio_canvas.tag_lower(grids)
        self.audio_canvas.create_line(loc_points, fill="white")
        self.audio_canvas.create_line(loc_points2, fill="white")

        ratio = (1/10)*len(data)/self.audio_canvas.winfo_width()+1
        data_lowres = data[::int(ratio)]
        data_high = data
        fulldatalen = len(audio[:, 1][::int(ratio)])

        data_lowres = np.array(data_lowres)

        # Calculate X using NumPy's arange and broadcasting for vectorized operations
        X = np.arange(len(data_lowres)) / (fulldatalen * (end - start))  # Create a sequence from 0 to len(data_lowres)
        X *= self.audio_canvas.winfo_width()  # Scale by canvas width

        # Calculate Y using vectorized operations, applying the transformation directly to data_lowres
        Y = 0.5 * self.audio_canvas.winfo_height() * (1 - data_lowres * (2 ** (1 - self.audio_zoom_y)))
        points = np.ravel(np.column_stack((X, Y)))
        points = points.astype(int)
        self.audio_low_data_line = self.audio_canvas.create_line(*points, fill="white")
        self.audio_canvas.update_idletasks()


        def datahigh(dataa):
            fulldatalen = len(audio[:, 1])
            data = np.array(dataa)

            # Calculate X using NumPy's arange and broadcasting for vectorized operations
            X = np.arange(len(data)) / (
                        fulldatalen * (end - start))  # Create a sequence from 0 to len(data_lowres)
            X *= self.audio_canvas.winfo_width()  # Scale by canvas width

            # Calculate Y using vectorized operations, applying the transformation directly to data_lowres
            Y = 0.5 * self.audio_canvas.winfo_height() * (1 - data * (2 ** (1 - self.audio_zoom_y)))
            points = np.ravel(np.column_stack((X, Y)))
            points = points.astype(int)
            try:
                self.audio_canvas.coords(self.audio_high_data_line,points)
                self.audio_canvas.delete(self.audio_low_data_line)
            except:
                pass
            self.audio_high_data_line = self.audio_canvas.create_line(*points, fill="white")

        if self.audio_high_var.get() == 1:
            threading.Thread(target = partial(datahigh, dataa = data)).start()

        try:
            def similarity_plot_thread():
                if not self.similarities:
                    return
                data2 = self.similarities[int(start * len(audio[:, 1])):int(end * len(audio[:, 1]))]
                points2 = []
                #ratio2 = len(data2) / self.audio_canvas.winfo_width() + 1
                #data2 = data2[::int(ratio2)]
                fulldatalen2 = len(self.similarities)

                X2 = self.audio_canvas.winfo_width() * (np.arange(0,len(data2),1) / (fulldatalen2 * (end - start)))
                #Y2 = 0.5 * self.audio_canvas.winfo_height() * (1 - data2 * 2 ** (1 - self.audio_zoom_y))
                #Y2 = self.audio_canvas.winfo_height() - 60 - data2*(self.audio_canvas.winfo_height()*0.5-60)
                #Y2 = self.audio_canvas.winfo_height()*(1-data2*(0.5-60)) - 60
                Y2 = (self.audio_canvas.winfo_height()-60)*(1-data2)+30
                points2 = np.column_stack((X2,Y2)).ravel()
                """
                for i in range(len(data2)):
                    X2 = self.audio_canvas.winfo_width() * (i / (fulldatalen2 * (end - start)))
                    Y2 = 0.5 * self.audio_canvas.winfo_height() * (1 - data2[i] * 2 ** (1 - self.audio_zoom_y))

                    points2.append(X2)
                    points2.append(Y2)
                """
                simil = self.audio_canvas.create_line(points2.tolist(), fill="gray")
                self.audio_canvas.tag_lower(simil)

            threading.Thread(target = similarity_plot_thread).start()
        except:
            pass
        #print("array:",thearray)
        #print("locations",locations)
        #print(duration, start*duration, duration*end)


    def change_frame_on_fc(self, event):
        self.change_frame_on = True
        self.change_frame_pos()
        print("clicked")

    def change_frame_off_fc(self, event):
        self.change_frame_on = False
        print("unclicked")

    def change_frame_pos(self, event = 0):
        if not self.framess:
            return
        if event != 0:
            self.pr_x, self.pr_y = event.x, event.y

        if self.change_frame_on == True :
            X = self.pr_x*self.frame_width/self.preview_canvas.winfo_width()
            Y = self.pr_y*self.frame_height/self.preview_canvas.winfo_height()
            X_off = int(X - self.frame_width//2)
            Y_off = int(Y - self.frame_height//2)
            self.x_offset_entry.delete(0,tk.END)
            self.x_offset_entry.insert(0, X_off)
            self.y_offset_entry.delete(0, tk.END)
            self.y_offset_entry.insert(0, Y_off)

        if int(self.y_offset_entry.get()) + int(self.frame_height_entry.get()) //2 >= self.frame_height // 2:
            self.y_offset_entry.delete(0, tk.END)
            self.y_offset_entry.insert(0, str(self.frame_height//2 - int(self.frame_height_entry.get())//2 -1))


        elif self.frame_height//2 + int(self.y_offset_entry.get()) - int(self.frame_height_entry.get()) //2 <= 0:
            self.y_offset_entry.delete(0, tk.END)
            self.y_offset_entry.insert(0, str(int(self.frame_height_entry.get())//2 - self.frame_height//2 +1))


        if self.direction.get() == 0:
            if int(self.x_offset_entry.get()) + self.frame_width//2 - int(self.frame_width_entry.get()) <= 0:
                self.x_offset_entry.delete(0, tk.END)
                self.x_offset_entry.insert(0, str(-self.frame_width//2 + int(self.frame_width_entry.get()) +1) )
            elif int(self.x_offset_entry.get()) >= self.frame_width//2:
                self.x_offset_entry.delete(0, tk.END)
                self.x_offset_entry.insert(0, str(self.frame_width // 2 -1))
        elif self.direction.get() == 1:
            if int(self.x_offset_entry.get()) + self.frame_width//2 <= 0:
                self.x_offset_entry.delete(0, tk.END)
                self.x_offset_entry.insert(0, str(-self.frame_width//2 +1))
            elif int(self.x_offset_entry.get()) >= self.frame_width//2 - int(self.frame_width_entry.get()) :
                self.x_offset_entry.delete(0, tk.END)
                self.x_offset_entry.insert(0, str(self.frame_width // 2- int(self.frame_width_entry.get()) +1)-1 )
        self.preview_frame()


    def on_ctrl_press(self,event):
        self.ctrl_pressed = True
        print("ctrl pressed")
    def on_ctrl_release(self,event):
        self.ctrl_pressed = False
        print("ctrl released")
    def change_frame_width(self, event):
        delta = event.delta
        if self.ctrl_pressed == True:
            previous = int(self.frame_height_entry.get())
            new = previous + 10*int(delta / abs(delta))
            self.frame_height_entry.delete(0, tk.END)
            self.frame_height_entry.insert(0, new)
        else:
            previous = int(self.frame_width_entry.get())
            new = previous + int(delta / abs(delta))
            self.frame_width_entry.delete(0, tk.END)
            self.frame_width_entry.insert(0, new)
        self.preview_frame()


    #scrolling zooms in the audio signal in x axis.
    #if the mouse is not on the center, the signal is shifted towards the opposite side.
    # to zoom in towards left: keep mouse on the left side etc.
    def audio_borders(self, var):
        if var == "vin":
            self.audio_zoom_x += 1
        if var == "vout" and self.audio_zoom_x > 1:
            self.audio_zoom_x += -1
        if var == "vleft":
            self.image_middle = self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        if var == "vright":
            self.image_middle = self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)

        if self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x) < 0:
            self.image_middle  = 0.5 * 2 ** (1 - self.audio_zoom_x)
        if self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x) > 1:
            self.image_middle = 1 -  0.5 * 2 ** (1 - self.audio_zoom_x)

        self.handle_scroll_audio()

    def change_angle(self, event = 0):
        delta = event.delta
        if delta > 0:
            previous = float(self.angle_entry.get())
            self.angle_entry.delete(0,tk.END)
            next = str(previous+1).split(".")[0]+"."+str(previous+1).split(".")[-1][:2]
            self.angle_entry.insert(0,next)

        else:
            previous = float(self.angle_entry.get())
            self.angle_entry.delete(0,tk.END)
            next = str(previous-1).split(".")[0]+"."+str(previous-1).split(".")[-1][:2]
            self.angle_entry.insert(0,next)
        try:
            self.preview_frame()
        except:
            pass


        return

    def handle_scroll_audio(self,event = 0,transfer = 0):
        if not self.audio:
            return
        if event == 0:
            pass
        else:
            delta = event.delta

            self.mousex_rel = self.image_middle + (self.mousex_oncanvas - 0.5) * 2 ** (1 - self.audio_zoom_x)
            if delta > 0:

                self.image_middle = (self.image_middle + self.mousex_rel)/2
                self.audio_zoom_x += 1
            elif self.audio_zoom_x >1:
                self.image_middle = 2*self.image_middle - self.mousex_rel
                self.audio_zoom_x -= 1

        start = self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        end = self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)

        if start < 0:
            self.image_middle -= self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        elif end > 1:
            self.image_middle -= self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)-1
        self.audiostartrel = self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        self.audioendrel = self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)

        startt = self.audiostartrel
        endd = self.audioendrel

        self.visualise_audio(self.audio_data, self.audiosamplerate, startt, endd)

        self.audio_canvas.delete(self.start_cursor)

        self.start_cursor_position = self.audio_canvas.winfo_width()*(self.start_time/self.duration - self.audiostartrel)/(self.audioendrel-self.audiostartrel)
        self.start_cursor = self.audio_canvas.create_line(self.start_cursor_position, 0, self.start_cursor_position, self.audio_canvas.winfo_height(),
                                                          fill="red")

        self.red_gun = self.audio_canvas.create_image(self.start_cursor_position,
                                                      self.audio_canvas.winfo_height() - self.scale_height - 30, anchor = tk.S,
                                                      image=red_gun_icon)
        self.red_gun2 = self.audio_canvas.create_image(self.start_cursor_position,
                                                      self.scale_height + 30, anchor = tk.N,
                                                      image=red_gun_icon)

        self.mousex_rel = self.image_middle + (self.mousex_oncanvas - 0.5) * (self.audio_zoom_x - 1)* 2 ** (1
            -self.audio_zoom_x)
        #duration = len(self.audio_data)/self.audio_sr
        #start = 0


        #print(delta, self.audio_zoom_x, self.image_middle)

    def create_signal(self):
        self.audio_data, self.audiosr = sf.read("temporary.wav")
        self.handle_scroll(event = 0)
        return

    def change_display_zoom(self,event):
        par = event.delta
        par = -par/abs(par)
        self.rect_width, self.rect_height = (1.2**par)*self.rect_width, (1.2**par)*self.rect_height
        self.display_zoom()

    def display_zoom(self,event = 0):
        if event != 0:
            self.disx, self.disy = event.x, event.y
        rect_width, rect_height = self.rect_width, self.rect_height
        def sig(x):
            if x < 0:
                return 0
            else:
                return x

        try:
            self.image_canvas2.delete(self.zoom_rectangle)
        except:
            pass

        try:
            x_left = sig(self.disx-rect_width//2)
            x_right = sig(self.disx + rect_width // 2)
            y_top = sig(self.disy-rect_height//2)
            y_bottom = sig(self.disy+rect_height//2)

            points = [x_left, y_top, x_right, y_top, x_right, y_bottom, x_left, y_bottom, x_left, y_top]
            self.zoom_rectangle = self.image_canvas2.create_line(points, fill = "#FF0000")

            x_left_ratio = ((self.image_canvas2.winfo_width() - x_left)/self.frames_width)
            x_right_ratio = ((self.image_canvas2.winfo_width() - x_right) / self.frames_width)
            y_top_ratio = (sig(y_top-30)/(self.frames_height))
            y_bottom_ratio = (sig(y_bottom-30)/(self.frames_height))

            #print(x_left_ratio, x_right_ratio,y_top_ratio,y_bottom_ratio, self.frames_or_width,self.frames_or_height)

            left_crop = int(self.frames_or_width*(1-x_left_ratio))
            right_crop = int(self.frames_or_width*(1-x_right_ratio))
            top_crop = int(y_top_ratio*self.frames_or_height)
            bottom_crop = int(y_bottom_ratio*self.frames_or_height)

            #print(left_crop,right_crop,top_crop,bottom_crop)

            self.frames_zoomed = self.frames_original[top_crop:bottom_crop,left_crop:right_crop]
            #cv2.imwrite("zoomed.png",self.frames_zoomed)
            self.frames_zoomed = cv2.resize(self.frames_zoomed, (300,500))
            self.frames_zoomed = ImageTk.PhotoImage(Image.fromarray(self.frames_zoomed))
            self.preview_canvas.create_image(0,0,anchor = tk.NW, image = self.frames_zoomed)
        except:
            pass

    def display_frames(self, event):
        try:
            if not self.timeline_image:
                return
        except:
            pass
        #print("button 3")

        self.image_canvas2.delete("all")
        start_frame = int((self.current_time - self.image_start_time_full)*self.fps*self.interpolation_factor)
        frames = []
        the_range = 6
        start_time = self.image_start_time_full + start_frame/(self.fps*self.interpolation_factor)
        times = []
        center = (self.frame_width // 2, self.frame_height // 2)
        angle = -float(self.angle_entry.get())
        scale = (1- np.sin(abs(angle*np.pi/180))) + np.sin(abs(angle*np.pi/180)) * self.frame_width/self.frame_height

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

        if self.image_end_time_full-self.current_time < 1.5:
            the_range = int(6*(self.image_end_time_full-self.current_time)/1.5)
        for i in range(the_range):
            #try:
            print(start_frame-i*int((0.3)*self.fps*self.interpolation_factor), self.fps*self.interpolation_factor, self.current_time , self.image_start_time_full)
            times.append(start_time + i*0.3)

            rotated = cv2.warpAffine(self.framess[start_frame-i*int(0.3*self.fps*self.interpolation_factor)], rotation_matrix,
                                                  (self.frame_width, self.frame_height))
            frames.append(rotated)
            #except:
            #    pass
        #print(len(self.framess))
        #print(len(frames))
        #print(times)
        frames = [frames[-i-1] for i in range(len(frames))]

        self.frames_original = cv2.hconcat(frames)
        self.frames_or_height,self.frames_or_width = cv2.hconcat(frames).shape
        #cv2.imwrite("frames.png", self.frames_original)
        self.frames_resized = cv2.resize(self.frames_original, (int((len(frames)/6)*self.image_canvas2.winfo_width()),self.image_canvas2.winfo_height()-30))

        self.frames_height, self.frames_width = self.frames_resized.shape
        self.frames_image = ImageTk.PhotoImage(Image.fromarray(self.frames_resized))
        #print(self.frames_width, self.frames_height)
        points = [1,30,1,1,int(self.image_canvas2.winfo_width()/6),1,int(self.image_canvas2.winfo_width()/6),30,int(self.image_canvas2.winfo_width()/6),1,
                  int(2*self.image_canvas2.winfo_width()/6),1,int(2*self.image_canvas2.winfo_width()/6),30,int(2*self.image_canvas2.winfo_width()/6),1,
                  int(3*self.image_canvas2.winfo_width()/6),1,int(3*self.image_canvas2.winfo_width()/6),30,int(3*self.image_canvas2.winfo_width()/6),1,
                  int(4*self.image_canvas2.winfo_width()/6),1,int(4*self.image_canvas2.winfo_width()/6),30,int(4*self.image_canvas2.winfo_width()/6),1,
                  int(5*self.image_canvas2.winfo_width()/6),1,int(5*self.image_canvas2.winfo_width()/6),30,int(5*self.image_canvas2.winfo_width()/6),1,
                  int(self.image_canvas2.winfo_width()),1,int(self.image_canvas2.winfo_width()),30,int(self.image_canvas2.winfo_width()),1,]

        self.image_canvas2.create_line(points, fill="black")

        self.image_canvas2.create_image(self.image_canvas2.winfo_width(), 30, anchor = tk.NE, image = self.frames_image)

        for i in range(len(times)):
            string = str(int(times[i]//60)) + ":" +str((int((times[i]%60)*100+0.5))/100)
            x_pos = int(self.image_canvas2.winfo_width()*(11/12))-i*int(self.image_canvas2.winfo_width()/6)
            #print(i,x_pos,string)
            self.image_canvas2.create_text(x_pos, 1, text = string, anchor = tk.N, fill="#DDDDDD")
        return

    def update_image(self, event = 0):
        self.update_image_var = True
        #print(self.update_image_var)
        self.generate_image()

    def generate_new_image(self):
        self.update_image_var = False
        self.generate_image()


    #this function crops all video frames, and stitches all the cropped frames to generate one single time-synchronized photo finish image.
    def generate_image(self, mode = 1):
        self.timeline_ready = False

        self.image_zoom_x = 1
        self.image_center = 0.5
        if mode == 1:
            if self.results:
                self.ask_del_over = False
                self.ask_del_res()
                while True:
                    time.sleep(0.3)
                    if self.ask_del_over == True:
                        break

        if self.update_image_var == False:
            #print("2",self.update_image_var)
            self.create_image()


        def crop_stitch():
            while True:
                if self.frames_ready == False:
                    time.sleep(0.2)
                else:
                    break

            self.change_frame_pos()

            start_y = self.frame_height//2 - int(self.frame_height_entry.get())//2 + int(self.y_offset_entry.get())
            end_y = self.frame_height//2 + int(self.frame_height_entry.get())//2 + int(self.y_offset_entry.get())
            if self.direction.get() == 0:
                end_x = self.frame_width//2 + int(self.x_offset_entry.get())
                start_x = self.frame_width//2 + int(self.x_offset_entry.get()) - int(self.frame_width_entry.get())
            elif self.direction.get() == 1:
                start_x = self.frame_width // 2 + int(self.x_offset_entry.get())
                end_x = self.frame_width // 2 + int(self.x_offset_entry.get()) + int(self.frame_width_entry.get())
            #print(start_y,end_y,middle_x,start_x,end_x)
            if self.fps_inc_combo.get() == "Do not increase FPS":
                self.frame_interpolation = False
            else:
                self.frame_interpolation = True
                self.interpolation_factor = int(str(self.fps_inc_combo.get()).split("x")[-1])
            if self.update_image_var == False:
                if self.frame_interpolation == True:
                    """
                    this block interpolates frames.
                    it adds frames in between existing frames by calculating the optic flow.
                    so for etc. in frame1, the object is at x=5, in frame2, the object is at x=6; in the interpolated frame, it is gonna apper to be at x = 5.5
                    there is no need for this funcion if frame rate fis large enough.
                    """
                    interpolation_factor = self.interpolation_factor
                    #self.frames_to_interpolate = [cv2.resize]
                    interpolated_frames = []

                    background_frame = self.framess[-1]

                    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST)

                    for i in range(len(self.framess) - 1):
                        frame1 = self.framess[i]
                        frame2 = self.framess[i + 1]

                        flow = dis.calc(frame1, frame2, None)
                        #flow[..., 1] = 0
                        interpolated_frames.append(frame1)

                        for j in range(1, interpolation_factor):
                            if self.abort:
                                polygon_points = [self.status.winfo_width() - 600, 5,
                                                  self.status.winfo_width() - 600,
                                                  5, self.status.winfo_width() - 600,
                                                  self.status.winfo_height() - 5,
                                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                                self.status.coords(self.progress_bar, polygon_points)
                                self.status.itemconfig(self.status_text, text=" ", font=self.font)
                                self.image_in_progress = False
                                self.abort = False
                                return
                            alpha = j / interpolation_factor
                            flow_scaled = flow * alpha

                            h, w = flow.shape[:2]
                            flow_map_x, flow_map_y = np.meshgrid(np.arange(w), np.arange(h))
                            flow_map_x = (flow_map_x - flow_scaled[..., 0]).astype(np.float32)
                            flow_map_y = (flow_map_y - flow_scaled[..., 1]).astype(np.float32)
                            flow_map = np.stack((flow_map_x, flow_map_y), axis=-1)

                            intermediate_frame = cv2.remap(frame1, flow_map, None, cv2.INTER_LINEAR)

                            static_mask = np.abs(background_frame - intermediate_frame) < 5

                            intermediate_frame_corrected = np.where(static_mask, background_frame, intermediate_frame)

                            interpolated_frames.append(intermediate_frame_corrected)

                        polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                        self.status.coords(self.progress_bar, polygon_points)
                        self.status.itemconfig(self.status_text, text="Interpolating frames: " + str(
                            int(100 * (i + 1) / len(self.framess))) + " %", font=self.font)


                    interpolated_frames.append(self.framess[-1])
                    def save_frames():
                        output_filename = 'output_video.avi'
                        frame_height, frame_width = interpolated_frames[0].shape[:2]
                        fps = self.fps*self.interpolation_factor

                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height), isColor=False)

                        for i in range(len(interpolated_frames)):

                            frame = interpolated_frames[i].astype(np.uint8)


                            out.write(frame)


                        out.release()

                        #custom progress bar
                        polygon_points = [self.status.winfo_width() - 600, 5,
                                          self.status.winfo_width() - 600 + int(((i + 1) / len(interpolated_frames)) * 600),
                                          5, self.status.winfo_width() - 600 + int(((i + 1) / len(interpolated_frames)) * 600),
                                          self.status.winfo_height() - 5,
                                          self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                        self.status.coords(self.progress_bar, polygon_points)
                        self.status.itemconfig(self.status_text, text="Saving interpolated video: " + str(
                            int(100 * (i + 1) / len(interpolated_frames))) + " %", font=self.font)
                    #threading.Thread(target = save_frames).start()
                    self.framess = interpolated_frames



            frames = []
            center = (self.frame_width // 2, self.frame_height // 2)
            angle = -float(self.angle_entry.get())
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

            for i in range(len(self.framess)):
                if angle >0.1 or angle < -0.1:
                    rotated = cv2.warpAffine(self.framess[i], rotation_matrix,
                                                  (self.frame_width, self.frame_height))
                else:
                    rotated = self.framess[i]
                image_cropped= rotated[start_y:end_y, start_x:end_x]


                frames.append(image_cropped)
                if self.abort:
                    polygon_points = [self.status.winfo_width() - 600, 5,
                                      self.status.winfo_width() - 600,
                                      5, self.status.winfo_width() - 600,
                                      self.status.winfo_height() - 5,
                                      self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                    self.status.coords(self.progress_bar, polygon_points)
                    self.status.itemconfig(self.status_text, text=" " + str(int(100 * (
                                (i + 1 - int((self.image_start_value + self.start_time) * fps)) / (
                                    (int((float(self.image_end_value) + self.start_time) * fps) - 1) - (
                                int((self.image_start_value + self.start_time) * fps)))))) + " %", font=self.font)
                    self.image_in_progress = False
                    self.abort = False
                    return
                polygon_points = [self.status.winfo_width() - 600, 5,
                                  self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                  5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                  self.status.winfo_height() - 5,
                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                self.status.coords(self.progress_bar, polygon_points)
                self.status.itemconfig(self.status_text, text="Cropping & stitching frames: " + str(
                    int(100 * (i + 1) / len(self.framess))) + " %", font=self.font)

            polygon_points = [self.status.winfo_width() - 600, 5,
                              self.status.winfo_width() - 600,
                              5, self.status.winfo_width() - 600,
                              self.status.winfo_height() - 5,
                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)

            #print("direction:",self.direction.get())

            if self.direction.get() == 1:
                pass
            if self.direction.get() == 0:
                frames = [cv2.flip(i, 1) for i in frames]

            #self.background_change = True
            if self.background_change == True:

                self.resize_co = 2
                # Resize the sample frame once
                sample = len(frames)-90
                frames[sample] = cv2.resize(frames[sample],
                                          (int(self.frame_width / self.resize_co), int(self.frame_height / self.resize_co)))

                for j in range(len(frames)):
                    if j != sample:
                        current_frame = cv2.resize(frames[j], (
                        int(self.frame_width / self.resize_co), int(self.frame_height / self.resize_co)))

                        diff = cv2.absdiff(current_frame, frames[sample])

                        mask = abs(diff) < 35

                        current_frame[mask] = 255

                        frames[j] = current_frame

                        if j % 5 == 0:
                            polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() - 600 + int(((j + 1) / len(frames)) * 600),
                                              5, self.status.winfo_width() - 600 + int(((j + 1) / len(frames)) * 600),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                            self.status.coords(self.progress_bar, polygon_points)
                            self.status.itemconfig(self.status_text, text="Setting background: " + str(
                                int(100 * (j + 1) / len(frames))) + " %", font=self.font)

                        #self.root.update_idletasks()


            polygon_points = [self.status.winfo_width() - 600, 5,
                              self.status.winfo_width() - 600,
                              5, self.status.winfo_width() - 600,
                              self.status.winfo_height() - 5,
                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)

            self.timeline_image = cv2.hconcat(frames)

            self.timeline_image = cv2.flip(self.timeline_image, 1)

            #self.timeline_image = cv2.cvtColor(self.timeline_image, cv2.COLOR_RGB2GRAY)

            self.status.itemconfig(self.status_text,
                                   text="Photo-finish image is ready!", font=self.font)
            self.image_in_progress = False
            self.image_button.config(state="normal")
            self.image_button.config(image=self.generate_image_icon)
            self.image_update_button.config(state="normal")

            polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() ,
                                              5, self.status.winfo_width(),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)



            start_ratio = 1 - self.image_start_value / self.duration

            end_ratio = 1 - self.image_end_value/ self.duration

            height, width = self.timeline_image.shape

            self.image = self.timeline_image[0:height, 0:]

            height, width = self.image.shape

            self.image_resized = cv2.resize(self.image, (
            int(width * (self.image_canvas.winfo_height() - self.scale_height) / height),
            (self.image_canvas.winfo_height() - self.scale_height)))
            self.timeline_ready = True



        crop_stitch_th = threading.Thread(target=crop_stitch)
        crop_stitch_th.start()






        def zoomed_images_thread():
            self.zoomed_images = []
            while True:
                if self.timeline_ready is False:
                    time.sleep(0.2)
                else:
                    break
            for i in range(1,self.max_image_zoom+1):
                zoomed = cv2.resize(self.image_resized, (int(((1/0.75)**(i-1))*self.image_canvas.winfo_width()),(self.image_canvas.winfo_height()-self.scale_height)))
                self.zoomed_images.append(zoomed)
                #cv2.imwrite("zoom"+str(i)+".png", zoomed)
                self.status.itemconfig(self.status_text,
                                       text="Constructing zoom levels "+str(i)+"/"+str(self.max_image_zoom) ,
                                       font=self.font)
                if i == 1:
                    self.visualise_image()
            self.status.itemconfig(self.status_text,
                                   text=str(self.max_image_zoom)+" zoom levels constructed!",
                                   font=self.font)

        images_thread = threading.Thread(target=zoomed_images_thread)
        images_thread.start()



        #cv2.imwrite("test_cropped.png", self.image)

    def on_click_image(self, event):
        try:
            if not self.timeline_image:
                return
        except:
            pass
        if self.audio:
            self.results.append(self.current_time)
            self.visualise_image()
            self.results_sorted = sorted(self.results)
            self.table.update_results(self.results_sorted)
            self.table.update_table()
            print(self.results_sorted)
        return

    def undo(self, event = 0):
        self.deleted_results.append(self.results[-1])
        del self.results[-1]
        self.results_sorted = sorted(self.results)
        self.results_sorted = sorted(self.results)
        self.table.update_results(self.results_sorted)
        self.visualise_image()
        print(self.results_sorted)

    def redo(self, event = 0):
        self.results.append(self.deleted_results[-1])
        del self.deleted_results[-1]
        self.results_sorted = sorted(self.results)
        self.table.update_results(self.results_sorted)
        self.visualise_image()

    def handle_scroll_image(self):
        return

    def leave_image_canvas(self,event):
        try:
            self.image_canvas.delete(self.hash_line)
            self.image_canvas.delete(self.hash_line_hor)
        except:
            pass

    def on_mouse_motion_image(self,event):
        self.mousex, self.mousey = event.x, event.y
        self.mousex_oncanvas = self.mousex/self.image_canvas.winfo_width()

        self.current_time = (1-self.mousex_oncanvas)*(self.image_end_time-self.image_start_time) + self.image_start_time

        current_time_str = str(int(self.current_time//60)) + ":" +str((int((self.current_time%60)*1000+0.5))/1000)

        self.status.itemconfig(self.status_text, text = current_time_str)

        try:
            self.image_canvas.delete(self.hash_line)
            self.image_canvas.delete(self.hash_line_hor)
        except:
            pass
        self.hash_line = self.image_canvas.create_line(self.mousex, 0, self.mousex, self.image_canvas.winfo_height()-self.scale_height,
                                                    fill=self.hashline_color)


        self.hash_line_hor = self.image_canvas.create_line(self.mousex-10, self.mousey, self.mousex+10, self.mousey,
                                                       fill=self.hashline_color)
        return

    def image_borders(self,var = None):
        if var == "vin" and self.image_zoom_x < self.max_image_zoom:
            self.image_zoom_x += 1

        elif var == "vout" and self.image_zoom_x > 1:
            self.image_zoom_x -= 1

        elif var == "vleft":
            self.image_center -= (1-0.75)*0.75**(self.image_zoom_x-1)

        elif var == "vright":
            self.image_center += (1-0.75)*0.75**(self.image_zoom_x-1)

        if self.image_center < 0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 0.5 *0.75** (self.image_zoom_x-1)

        elif self.image_center > 1-0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 1- 0.5*0.75 ** (self.image_zoom_x-1)


        self.visualise_image()

    def visualise_image(self):

        self.image_canvas.delete("all")

        self.image_start_time_full = self.image_start_value
        self.image_end_time_full = self.image_end_value

        center_time = (1-self.image_center)*(self.image_end_time_full-self.image_start_time_full) + self.image_start_time_full

        self.image_start_time = center_time - (self.image_end_time_full-self.image_start_time_full)*0.5*0.75 ** (self.image_zoom_x-1)
        self.image_end_time = center_time + (self.image_end_time_full - self.image_start_time_full) * 0.5*0.75 ** (self.image_zoom_x-1)

        start = self.image_center - 0.5*0.75 ** (self.image_zoom_x-1)
        end = self.image_center + 0.5*0.75 ** (self.image_zoom_x-1)


        level = np.log(self.image_end_time-self.image_start_time)/np.log(10)
        level = int(level+0.5)
        tick_increments = 10**(level-2)
        label_increments = 10**(level-1)

        tick_start = self.image_start_time - self.image_start_time%tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time%tick_increments
        ticks = np.arange(tick_start,tick_end+10*tick_increments,tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = self.image_canvas.winfo_width()*(1-(ticks-self.image_start_time)/(self.image_end_time-self.image_start_time))

        locations_2 = self.image_canvas.winfo_width() * (1-(labels - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))

        #print(labels)
        #print(locations_2)

        loc_points = []
        scaleY = self.image_canvas.winfo_height() - self.scale_height
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY+5)
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY)

        #print("time borders:",self.image_start_time,self.image_end_time)

        #print("center:",self.image_center)
        #print("zoom:", self.image_zoom_x)

        for i in range(len(labels)):
            if label_increments >=1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i]*(1/label_increments))*label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0]+"."+thestr.split(".")[-1][:int(np.log(1/label_increments)/np.log(10))]

            self.image_canvas.create_text(locations_2[i],self.image_canvas.winfo_height()-10,text = thestr,fill="#DDDDDD")
            self.image_canvas.create_line(locations_2[i],self.image_canvas.winfo_height()-20,locations_2[i],scaleY,fill = "#DDDDDD")


        #print("borders:", start, end)
        #print(len(self.zoomed_images))

        height1, width1  = self.zoomed_images[0].shape

        cropped_image = self.zoomed_images[self.image_zoom_x - 1][0:height1,
                        int(width1 * (1/0.75) ** (self.image_zoom_x - 1) * start):int(
                            width1 * (1/0.75) ** (self.image_zoom_x - 1) * end)]

        image_pil = Image.fromarray(cropped_image)

        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.image_canvas.create_line(loc_points, fill="#DDDDDD")

        for i in self.results:
            X = self.image_canvas.winfo_width() * (1 - (i - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))
            self.image_canvas.create_line(X, 0, X,self.image_canvas.winfo_height() - self.scale_height,
                                                       fill=self.hashline_color)
        return

    def ask_del_res(self):
        self.ask_del_results = tk.Toplevel(self.root)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 400
        window_height = 100
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.ask_del_results.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.ask_del_results.wm_iconphoto(False, self.main_icon)
        self.ask_del_results.title("Delete times?")
        tk.Label(self.ask_del_results, text="Do you want to delete previously marked results?").place(x=200, y=30,
                                                                                                      anchor="center")

        def delete_results():
            self.results = []
            self.deleted_results = []
            self.results_sorted = []
            self.ask_del_over = True
            self.generate_image(mode =2)

            self.ask_del_results.destroy()
            return

        def not_delete():
            self.ask_del_results.destroy()
            self.ask_del_over = True
            self.generate_image(mode=2)
            return

        tk.Button(self.ask_del_results, text="Yes", command=delete_results).place(x=190, y=70, anchor="e")
        tk.Button(self.ask_del_results, text="No", command=not_delete).place(x=210, y=70, anchor="w")

        self.ask_del_results.mainloop()


    def create_image(self):
        self.timeline_image = None
        self.framess = None

        if self.image_in_progress:
            self.abort = True
            self.image_button.config(image=self.generate_image_icon)
            return

        self.image_button.config(image = self.abort_icon)
        self.image_update_button.config(state="disabled")
        self.frames_ready = False
        self.image_in_progress = True

        if not self.image_start_entry_minute.get():
            self.image_start_entry_minute.insert(0,"0")
        if not self.image_start_entry_second.get():
            self.image_start_entry_second.insert(0,"0")
        if not self.image_end_entry_minute.get():
            self.image_end_entry_minute.insert(0,str(int((self.duration-self.start_time)//60)))
        if not self.image_end_entry_second.get():
            sec = str((self.duration-self.start_time)%60)
            sec = sec.split(".")[0]+"."+sec.split(".")[-1][:2]
            self.image_end_entry_second.insert(0,sec)


        self.image_start_value = 60*int(self.image_start_entry_minute.get()) + float(self.image_start_entry_second.get())
        self.image_end_value = 60 * float(self.image_end_entry_minute.get()) + float(
            self.image_end_entry_second.get())
        print(self.image_start_value, self.image_end_value)
        if self.image_end_value > self.duration - self.start_time:
            self.image_end_value =  self.duration - self.start_time
        if self.image_end_value <= self.image_start_value:
            print(self.image_end_value , self.image_start_value)
            tk.messagebox.showinfo(title="Invalid interval", message="End time cannot be smaller than or equal to start time.")
            self.image_button.config(state="normal")
            self.image_button.config(image=self.generate_image_icon)
            self.image_in_progress = False
            return
        def image_in_thread():
            #clip = VideoFileClip(self.video_file)
            #framess = [frame for frame in clip.iter_frames()]
            cap = cv2.VideoCapture(self.video_file)

            self.framess = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            self.fps = fps
            cap.set(cv2.CAP_PROP_POS_FRAMES,int((self.image_start_value+self.start_time- (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))) * fps)   )
            print("fps",fps)
            progress_points = [self.status.winfo_width() -600-1,5,self.status.winfo_width()-1,5,self.status.winfo_width()-1,self.status.winfo_height()-5,self.status.winfo_width()-600-1,self.status.winfo_height()-5,self.status.winfo_width()-600-1,5]
            self.progress_bar_bg = self.status.create_line(progress_points, fill = "#00FF00")
            #stamp = 0
            #print(self.duration)
            self.capture_start = int((self.image_start_value+self.start_time - (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))) * fps)
            self.capture_end = int((self.image_end_value+self.start_time - (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))) * fps)
            for i in range(self.capture_start,self.capture_end-1):
                ret, frame = cap.read()
                if not ret:
                    break
                if self.abort:
                    polygon_points = [self.status.winfo_width() - 600, 5,
                                      self.status.winfo_width() - 600,
                                      5, self.status.winfo_width() - 600,
                                      self.status.winfo_height() - 5,
                                      self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                    self.status.coords(self.progress_bar, polygon_points)
                    self.status.itemconfig(self.status_text, text=" " + str(int(100 * (
                                (i + 1 - int((self.image_start_value + self.start_time) * fps)) / (
                                    (int((float(self.image_end_value) + self.start_time) * fps) - 1) - (
                                int((self.image_start_value + self.start_time) * fps)))))) + " %", font=self.font)
                    self.status.itemconfig(self.status_text, text=" ", font=self.font)
                    self.image_in_progress = False
                    self.abort = False
                    return
                if i == self.capture_start:
                    self.image_start_value = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - self.start_time + (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))
                    #print(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
                if i == self.capture_end-2:
                    self.image_end_value = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - self.start_time + (self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var))
                    #print(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)


                #print(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
                #stamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                self.framess.append(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
                polygon_points = [self.status.winfo_width()  - 600, 5, self.status.winfo_width() -600 +int( ((i+1-int((self.image_start_value+self.start_time) * fps))/(int((float(self.image_end_value)+self.start_time) * fps)-int((self.image_start_value+self.start_time) * fps))) * 600),
                                  5, self.status.winfo_width() -600 + int( ((i+1-int((self.image_start_value+self.start_time) * fps))/(int((float(self.image_end_value)+self.start_time) * fps)-int((self.image_start_value+self.start_time) * fps))) * 600), self.status.winfo_height() - 5,
                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                self.status.coords(self.progress_bar,polygon_points)

                self.status.itemconfig(self.status_text, text = "Extracting video frames: "+str(int(100 * ((i+1-int((self.image_start_value+self.start_time) * fps)) / (( int((float(self.image_end_value)+self.start_time) * fps)-1)-(int((self.image_start_value+self.start_time) * fps)))))) + " %", font = self.font)

            if self.fps_inc_combo.get() == "Do not increase FPS":
                self.interpolation_factor = 1
            else:
                self.interpolation_factor = int(str(self.fps_inc_combo.get()).split("x")[-1])

            self.image_end_value += 1/(self.fps*self.interpolation_factor)
            print("end altered:",1/(self.fps*self.interpolation_factor))
            self.status.itemconfig(self.status_text,
                                   text="Video frames ready!",
                                   font=self.font)
            #self.preview_button.config(state="normal")
            cap.release()
            self.frame_height, self.frame_width = self.framess[0].shape
            self.image_dimensions.config(text = f"Image dimensions: {self.frame_width}x{self.frame_height}")
            self.frame_height_entry.delete(0, tk.END)
            self.frame_height_entry.insert(0, self.frame_height - 1)
            #print(self.frame_height)

            self.frames_ready = True
            #cv2.imwrite("test.png",self.timeline_image)

        image_thread = threading.Thread(target = image_in_thread)
        image_thread.start()

    def import_heat(self, mode=0):
        import pandas as pd
        from tkinter import filedialog

        if mode == 0:
            file = filedialog.askopenfilename()
            if not file or file.split(".")[-1] != "xlsx":
                return
            dataframe = pd.read_excel(file, header=0)
            matrix = dataframe.values.tolist()
            headers_from_file = list(dataframe.columns)
        else:
            import pyperclip
            textdata = pyperclip.paste()
            rows = textdata.strip().split("\n")
            matrix = [row.split("\t") for row in rows if row.strip()]
            #headers_from_file = matrix.pop(0)

        import_heat_w = tk.Toplevel(self.root)
        import_heat_w.wm_iconphoto(False, self.main_icon)
        import_heat_w.title("Import Heat")

        columns = []
        column_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                          "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                          "U", "V", "W", "X", "Y", "Z"]

        column_count = max(len(row) for row in matrix)
        for col in range(column_count):
            label = tk.Label(import_heat_w, text=f"Column {column_letters[col]}:")
            label.pack()

            combo = ttk.Combobox(import_heat_w, values=self.default_parameters,
                                 state="readonly", width=15)
            default_value = self.default_parameters[col] if col < len(self.default_parameters) else \
            self.default_parameters[0]
            combo.set(default_value)
            combo.pack()

            columns.append(combo)

        def done_with_heat():
            selected_headers = [combo.get() for combo in columns]
            selected_headers = [h for h in selected_headers if h and h not in ("nan", "-")]

            athletes = []
            for row in matrix:
                row_data = {}
                for i in range(min(len(selected_headers), len(row))):
                    row_data[selected_headers[i]] = str(row[i])
                athletes.append(row_data)

            self.excel_import = True
            import_heat_w.destroy()

            if mode == 0:
                self.table.change_title(str(file).split("/")[-1].split(".")[0] +
                                        ", Wind: " + str(self.wind_var) + " m/s")

            self.table.set_data_from_matrix(athletes)

        tk.Button(import_heat_w, text="Ok", command=done_with_heat).pack(pady=10)
        height = 42 * len(columns) + 60
        import_heat_w.geometry(f"250x{height}")
        import_heat_w.mainloop()

    def view_pf(self):
        self.view_pf_var = True
        self.take_canvas_screenshot()
        return

    def take_canvas_screenshot(self, mode = 0):
        if self.view_pf_var == False:
            if mode == 0:
                filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        image_pil = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(image_pil)

        font = ImageFont.load_default()

        level = np.log(self.image_end_time - self.image_start_time) / np.log(10)
        level = int(level+0.5)
        tick_increments = 10 ** (level - 2)
        label_increments = 10 ** (level - 1)

        tick_start = self.image_start_time - self.image_start_time % tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time % tick_increments
        ticks = np.arange(tick_start, tick_end + 10*tick_increments, tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = canvas_width * (1 - (ticks - self.image_start_time) / (self.image_end_time - self.image_start_time))
        locations_2 = canvas_width * (
                    1 - (labels - self.image_start_time) / (self.image_end_time - self.image_start_time))

        scaleY = canvas_height - self.scale_height

        for i in range(len(ticks) - 1):
            draw.line([locations[i], scaleY + 5, locations[i], scaleY], fill="black")
            draw.line([locations[i], scaleY, locations[i + 1], scaleY], fill="black")

        for i in range(len(labels)):
            if label_increments >= 1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i] * (1 / label_increments)) * label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0] + "." + thestr.split(".")[-1][
                                                      :int(np.log(1 / label_increments) / np.log(10))]


            bbox = draw.textbbox((0, 0), thestr, font=font)
            text_width = bbox[2] - bbox[0]  # bbox[2] is the x2 coordinate, bbox[0] is the x1 coordinate
            text_height = bbox[3] - bbox[1]  # bbox[3] is the y2 coordinate, bbox[1] is the y1 coordinate

            draw.text((locations_2[i] - text_width / 2, canvas_height - 10 - text_height / 2), thestr, fill="black",
                      font=font)

            draw.line([locations_2[i], canvas_height - 20, locations_2[i], scaleY], fill="black")

        start = self.image_center - 0.5 * 0.75 ** (self.image_zoom_x - 1)
        end = self.image_center + 0.5 * 0.75 ** (self.image_zoom_x - 1)

        if self.zoomed_images:
            height1, width1 = self.zoomed_images[0].shape
            cropped_image = self.zoomed_images[self.image_zoom_x - 1][0:height1,
                            int(width1 * (1 / 0.75) ** (self.image_zoom_x - 1) * start):int(
                                width1 * (1 / 0.75) ** (self.image_zoom_x - 1) * end)]
            cropped_image_pil = Image.fromarray(cropped_image)
            image_pil.paste(cropped_image_pil, (0, 0))

        for i in self.results:
            X = canvas_width * (1 - (i - self.image_start_time) / (self.image_end_time - self.image_start_time))
            draw.line([X, 0, X, canvas_height - self.scale_height], fill=self.hashline_color)




        if self.view_pf_var == False:
            if mode == 0:
                image_pil.save(filename)
        else:
            self.view_pf_var = False
            pf_display = tk.Toplevel(self.root)
            pf_display.title("Photo-finish image")
            pf_display.attributes("-topmost", True)
            pf_display.wm_iconphoto(False, self.main_icon)
            pf_display.resizable(False,False)
            x_dim = self.image_canvas.winfo_width()
            y_dim = self.image_canvas.winfo_height()

            pf_display.geometry(f"{x_dim}x{y_dim}")

            pf_canvas = tk.Canvas(pf_display,width = x_dim, height = y_dim)
            pf_canvas.pack()

            tk_image = ImageTk.PhotoImage(image_pil)
            pf_canvas.create_image(0,0, anchor = tk.NW,image = tk_image,)

            pf_display.mainloop()
        return image_pil



    def export_results_table(self):
        def as_txt():
            name = asksaveasfile(defaultextension="*.txt",
                                 filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])

            if name is None:
                return

            with open(name.name, "w", encoding="utf-8") as results_text_file:
                results_text_file.write("Lane\tID\tName\t\t\tDate of Birth\tAffiliation\t\t\tLicense\tTime\tPlace\n")

                for i in self.table.data:
                    for j in self.default_parameters:
                        tab = "\t"
                        if j == "Name" or j == "Affiliation":
                            tab = "\t\t\t\t"
                        if j == "Place":
                            tab = "\n"
                        results_text_file.write(i[j]+tab)
            return
        def as_xlsx():
            allresults = self.table.data
            df = pd.DataFrame(allresults,columns = self.default_parameters)
            results_ex_file = asksaveasfile(defaultextension = "*.xlsx",filetypes=[("Text Documents", "*.xlsx"),("All Files", "*.*")])
            df.to_excel(results_ex_file.name, sheet_name = "Results", index=False)
            return

        def as_photo(mode=0):
            # Open a file dialog to ask for the location and file name to save the image
            if mode == 0:
                file_name = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
                                                         title="Save the table image as")

                if not file_name:
                    # If the user cancels the save, return without creating the image
                    return

            # Set some basic parameters
            padding = 10
            row_height = 40

            # Get the title text
            title_text = self.table.title_entry.get()  # Get the title from the entry

            # Define column widths based on header type
            col_widths = []
            for header in self.default_parameters:
                if header == "Name" or header == "Affiliation":
                    col_widths.append(250)  # More space for names and affiliations
                elif header == "Lane":
                    col_widths.append(50)  # Less space for one-digit lane number
                elif header == "ID":
                    col_widths.append(70)  # Space for 3-digit ID
                elif header == "License":
                    col_widths.append(120)  # Moderate space for license
                elif header == "Time":
                    col_widths.append(100)  # Space for 7-digit time
                elif header == "Place":
                    col_widths.append(50)  # Less space for 1-2 digit place
                else:
                    col_widths.append(150)  # Default space for other columns

            # Calculate image dimensions
            image_width = sum(col_widths) + 2 * padding
            image_height = (len(self.table.data) + 1) * row_height + 2 * padding + 40  # +40 for the title

            # Create a blank image with white background
            img = Image.new("RGB", (image_width, image_height), color="white")
            draw = ImageDraw.Draw(img)

            # Load the default font
            font = ImageFont.load_default()

            # Function to replace Turkish characters with English equivalents
            def replace_turkish_chars(text):
                replacements = {
                    'Ğ': 'G', 'ğ': 'g',
                    'Ü': 'U', 'ü': 'u',
                    'Ö': 'O', 'ö': 'o',
                    'Ç': 'C', 'ç': 'c',
                    'Ş': 'S', 'ş': 's',
                    'İ': 'I', 'ı': 'i',
                }
                for turkish_char, english_char in replacements.items():
                    text = text.replace(turkish_char, english_char)
                return text

            # Draw the title
            title_x = padding
            title_y = padding  # Title position
            draw.text((title_x, title_y), replace_turkish_chars(title_text), fill="black", font=font)

            # Draw the headers
            for col_num, header in enumerate(self.default_parameters):
                x = padding + sum(col_widths[:col_num])
                y = padding + 40  # Move headers down by 40 for the title
                draw.text((x, y), replace_turkish_chars(header), fill="black", font=font)

            # Draw the table rows and lines
            for row_num, row_data in enumerate(self.table.data):
                for col_num, header in enumerate(self.default_parameters):
                    x = padding + sum(col_widths[:col_num])
                    y = padding + (row_num + 2) * row_height  # +2 to account for title and header
                    text = replace_turkish_chars(str(row_data.get(header, "")))
                    draw.text((x, y), text, fill="black", font=font)

                # Draw horizontal line for row separation
                line_y = padding + (row_num + 2) * row_height  # +2 for title and header
                draw.line([(padding - 3, line_y - 3), (image_width - padding - 3, line_y - 3)],
                          fill="black", width=1)

            # Draw vertical lines for column separation
            x_position = padding
            for index, col_width in enumerate(col_widths):
                if index > 0:  # Skip the first column
                    draw.line([(x_position - 3, padding + 40 - 3), (x_position - 3, image_height - padding - 3)],
                              fill="black", width=1)
                x_position += col_width

            # Save the image to the chosen location
            if mode == 0:
                img.save(file_name)
            return img

        def onclose():
            self.export_window.destroy()

        self.export_window = tk.Toplevel(self.root)
        self.export_window .title("Export Results...")
        self.export_window.wm_iconphoto(False, self.export_image_icon)
        self.export_window.geometry("270x70")
        self.export_window.resizable(False, False)
        self.export_window.protocol("WM_DELETE_WINDOW", onclose)

        exportresults = tk.Label(self.export_window,text="Export results as: ")
        exportresults.place(x=5,y = 5)
        exporttype = ttk.Combobox(self.export_window,state = "readonly",values=["Excel file (*.xlsx)",
                                                                                "Text file (*.txt)",
                                                                                "Image file (*.png)",
                                                                                "Image (with photo-finish) (*png)"],width = 20)
        exporttype.set("Excel file (*.xlsx)")
        exporttype.place(x = 120, y = 5)

        def export_ok():
            if exporttype.get() == "Excel file (*.xlsx)":
                as_xlsx()
            elif exporttype.get() == "Text file (*.txt)":
                as_txt()
            elif exporttype.get() == "Image file (*.png)":
                as_photo()
            elif exporttype.get() == "Image (with photo-finish) (*png)":
                img1 = as_photo(mode = 1)
                img2 = self.take_canvas_screenshot(mode = 1)
                width1, height1 = img1.size
                width2, height2 = img2.size

                # Determine the maximum width
                max_width = max(width1, width2)

                # Resize images to have the same width
                if width1 < max_width:
                    img1 = img1.resize((max_width, int((height1 / width1) * max_width)))
                if width2 < max_width:
                    img2 = img2.resize((max_width, int((height2 / width2) * max_width)))

                # Calculate the total height for the new image
                total_height = img1.height + img2.height

                # Create a new blank image with the calculated width and height
                unified_image = Image.new('RGB', (max_width, total_height))

                # Paste the first image on top
                unified_image.paste(img1, (0, 0))
                # Paste the second image below the first one
                unified_image.paste(img2, (0, img1.height))
                file_name = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
                                                         title="Save the table image as")

                if not file_name:
                    # If the user cancels the save, return without creating the image
                    return
                unified_image.save(file_name)

            else:
                print("no save type detected",exporttype.get())
            self.export_window.destroy()
            return
        exportok = tk.Button(self.export_window,text="Export",command = export_ok)
        exportok.place ( x = 100, y = 40)

        return

    def results_table(self):
        return
    def options(self):
        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Options")
        self.options_window.wm_iconphoto(False, options_icon)
        self.options_window.resizable(False, False)
        self.options_window.geometry("355x505")
        self.options_window.option_add('*Background', '#222222')
        self.options_window.option_add('*Foreground', '#FFFFFF')
        self.options_window.option_add('*Button.Background', '#222222')

        self.notebook_options = ttk.Notebook(self.options_window)
        self.notebook_options.pack(expand=True, fill='both')

        self.calibration_options = tk.Frame(self.notebook_options)
        self.display_options = tk.Frame(self.notebook_options)


        self.notebook_options.add(self.calibration_options, text='Calibration')
        self.notebook_options.add(self.display_options , text='Display')


        self.sound_options = tk.Canvas(self.calibration_options, width=350, height=800, bg="#222222",
                                       highlightthickness=0)
        self.sound_options.pack(side=tk.LEFT)

        tk.Label(self.sound_options, text="Sound Calibration").place(x=175, y=10, anchor="center")

        points = [250, 10, 345, 10, 345, 660, 5, 660, 5, 10, 100, 10]
        self.sound_options.create_line(points, fill="#CCCCCC")




        def apply():
            self.gun_mic_var = float(self.gun_mic_entry.get())
            self.gun_start_var = float(self.gun_start_entry.get())
            self.sound_var = float(self.sound_entry.get())
            self.wind_var = float(self.wind_entry.get())
            self.time_var = float(self.time_entry.get())
            return

        self.apply_button = tk.Button(self.sound_options, text = "Apply", command = apply)
        self.apply_button.place(x = 175, y  =450, anchor = "center")



        self.options_window.mainloop()
        #return

    def leave_image_canvas2(self,event):
        try:
            self.preview_frame()
        except:
            pass

    def preview_frame(self):
        try:
            self.image_canvas2.delete(self.zoom_rectangle)
        except:
            pass
        self.line_thickness = int(self.frame_width_entry.get())
        width, height = self.preview_canvas_width, self.preview_canvas_height

        x_ratio = width / self.frame_width
        y_ratio = height / self.frame_height

        #print("preview frame")

        center = (self.frame_width // 2, self.frame_height // 2)
        angle = -float(self.angle_entry.get())
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)


        sample_image = self.framess[-1]

        rotated = cv2.warpAffine(sample_image, rotation_matrix,
                                 (self.frame_width, self.frame_height))

        self.rotated = rotated

        image = ImageTk.PhotoImage(
            Image.fromarray(cv2.resize(rotated, (width + 1, height + 1))))

        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=image)

        self.preview_canvas.image = image



        """
        x_min = int(self.frame_width // 2 - self.line_thickness // 2 + image_center_offset)
        x_max = int(self.frame_width // 2 + self.line_thickness // 2 + image_center_offset)
        y_min = top_y_offset
        y_max = self.frame_height - bottom_y_offset

        #print(x_min, x_max, y_min, y_max)


        resized_x = self.line_thickness * x_ratio
        resized_y = y_ratio * (self.frame_height - top_y_offset - bottom_y_offset)
        #print(y_ratio, height, top_y_offset, bottom_y_offset, resized_y)

        cropped_image_array = sample_image[y_min:y_max, x_min:x_max]  # Fix slicing order
        cropped_image = ImageTk.PhotoImage(Image.fromarray(
            cv2.cvtColor(cv2.resize(cropped_image_array, (int(resized_x)+2, int(resized_y))), cv2.COLOR_BGR2RGB)))
        """
        top_y = self.frame_height // 2 - int(self.frame_height_entry.get()) // 2 + int(self.y_offset_entry.get())
        bottom_y = self.frame_height // 2 + int(self.frame_height_entry.get()) // 2 + int(self.y_offset_entry.get())
        if self.direction.get() == 0:
            right_x = self.frame_width // 2 + int(self.x_offset_entry.get())
            left_x = self.frame_width // 2 + int(self.x_offset_entry.get()) - int(self.frame_width_entry.get())
            center_x = right_x
        elif self.direction.get() == 1:
            left_x = self.frame_width // 2 + int(self.x_offset_entry.get())
            right_x = self.frame_width // 2 + int(self.x_offset_entry.get()) + int(self.frame_width_entry.get())
            center_x = left_x

        points = [x_ratio*left_x, y_ratio*top_y,
                  x_ratio*right_x, y_ratio*top_y,
                  x_ratio*right_x, y_ratio*bottom_y,
                  x_ratio*left_x, y_ratio*bottom_y,
                  x_ratio*left_x, y_ratio*top_y]
        points = [int(i) for i in points]


        #self.preview_canvas.create_image(left_x+1, top_y+1, anchor=tk.NW, image=cropped_image)
        self.preview_canvas.create_line(points, fill="#FF0000", dash = (1,2))
        self.preview_canvas.create_line(int(x_ratio*center_x),0, int(x_ratio*center_x), self.preview_canvas.winfo_height(),fill="#FF0000")
        #print(self.frame_width, points)

        #self.preview_canvas.image2 = cropped_image

    def auto_width(self):
        lower_res = [cv2.resize(i, (int(self.frame_width/4), int(self.frame_height/4))) for i in self.framess]
        """
        for i in range(len(self.framess)-1):
            difference_matrix =
        """
        return





#opticon = Image.open('images/stop.ico')

#array = np.array(Image.open('images/splash.png'))

"""
string = "["

for i in range(len(array)):
    string += "["
    for j in range(len(array[i])):
        string += "[" + ",".join(map(str, array[i][j])) + "]"
        if j < len(array[i]) - 1:
            string += ","
    string += "]"
    if i < len(array) - 1:
        string += ","

string += "]"


file = open("splash.py","w")
file.write(string)
print(string)
"""


root = tk.Tk()
root.title("OpenPhotoFinish (host)")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 0
window_height = 0

# Calculate position x and y coordinates
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f'{window_width}x{window_height}+{x}+{y}')
root.overrideredirect(True)

opticon_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,66],[0,0,0,185],[0,0,0,189],[0,0,0,190],[0,0,0,177],[0,0,0,48],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,174],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,150],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,57],[0,0,0,238],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,44],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,80],[0,0,0,36],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,136],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,123],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,54],[0,0,0,102],[0,0,0,34],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,37],[0,0,0,190],[0,0,0,253],[0,0,0,224],[0,0,0,157],[0,0,0,72],[0,0,0,21],[0,0,0,67],[0,0,0,218],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,213],[0,0,0,65],[0,0,0,24],[0,0,0,83],[0,0,0,175],[0,0,0,237],[0,0,0,255],[0,0,0,190],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,40],[0,0,0,193],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,244],[0,0,0,212],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,239],[0,0,0,216],[0,0,0,247],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,40],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,154],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,136],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,120],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,94],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,41],[0,0,0,226],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,213],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,146],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,132],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,64],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,242],[0,0,0,197],[0,0,0,161],[0,0,0,161],[0,0,0,197],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,241],[0,0,0,59],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,100],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,72],[0,0,0,13],[0,0,0,1],[0,0,0,1],[0,0,0,13],[0,0,0,72],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,100],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,7],[0,0,0,52],[0,0,0,132],[0,0,0,224],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,189],[0,0,0,31],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,189],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,227],[0,0,0,144],[0,0,0,66],[0,0,0,14],[0,0,0,0]],[[0,0,0,77],[0,0,0,170],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,61],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,61],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,244],[0,0,0,191],[0,0,0,103]],[[0,0,0,243],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,178],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,179],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,250]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,138],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,138],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,250],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,178],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,179],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,243]],[[0,0,0,103],[0,0,0,191],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,60],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,61],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,170],[0,0,0,77]],[[0,0,0,0],[0,0,0,14],[0,0,0,67],[0,0,0,145],[0,0,0,227],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,188],[0,0,0,30],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,189],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,224],[0,0,0,133],[0,0,0,52],[0,0,0,7],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,101],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,71],[0,0,0,13],[0,0,0,1],[0,0,0,1],[0,0,0,13],[0,0,0,71],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,99],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,59],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,242],[0,0,0,196],[0,0,0,160],[0,0,0,160],[0,0,0,196],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,243],[0,0,0,64],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,132],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,146],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,213],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,226],[0,0,0,42],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,94],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,120],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,137],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,155],[0,0,0,1],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,40],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,247],[0,0,0,216],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,239],[0,0,0,212],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,193],[0,0,0,40],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,37],[0,0,0,191],[0,0,0,255],[0,0,0,237],[0,0,0,175],[0,0,0,83],[0,0,0,24],[0,0,0,65],[0,0,0,214],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,218],[0,0,0,67],[0,0,0,21],[0,0,0,71],[0,0,0,157],[0,0,0,224],[0,0,0,253],[0,0,0,190],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,34],[0,0,0,102],[0,0,0,54],[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,124],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,36],[0,0,0,81],[0,0,0,31],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,44],[0,0,0,228],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,238],[0,0,0,58],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,150],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,175],[0,0,0,9],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,48],[0,0,0,177],[0,0,0,190],[0,0,0,189],[0,0,0,185],[0,0,0,67],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
array_np = np.array(opticon_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
options_icon = ImageTk.PhotoImage(image)

resultico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,47],[0,0,0,228],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,47],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,73],[0,0,0,249],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,249],[0,0,0,73],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,73],[0,0,0,249],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,249],[0,0,0,73],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,58],[0,0,0,236],[0,0,0,253],[0,0,0,253],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,253],[0,0,0,236],[0,0,0,58],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,64],[0,0,0,82],[0,0,0,145],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,141],[0,0,0,82],[0,0,0,64],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,21],[0,0,0,11],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,91],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,85],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,20],[0,0,0,15],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,66],[0,0,0,205],[0,0,0,160],[0,0,0,24],[0,0,0,0],[0,0,0,2],[0,0,0,29],[0,0,0,82],[0,0,0,172],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,170],[0,0,0,82],[0,0,0,30],[0,0,0,2],[0,0,0,0],[0,0,0,50],[0,0,0,197],[0,0,0,181],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,44],[0,0,0,216],[0,0,0,255],[0,0,0,254],[0,0,0,172],[0,0,0,61],[0,0,0,136],[0,0,0,218],[0,0,0,251],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,251],[0,0,0,218],[0,0,0,136],[0,0,0,74],[0,0,0,201],[0,0,0,255],[0,0,0,255],[0,0,0,188],[0,0,0,21],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,67],[0,0,0,241],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,241],[0,0,0,254],[0,0,0,255],[0,0,0,237],[0,0,0,196],[0,0,0,158],[0,0,0,137],[0,0,0,137],[0,0,0,158],[0,0,0,196],[0,0,0,237],[0,0,0,255],[0,0,0,254],[0,0,0,245],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,210],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,5],[0,0,0,109],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,227],[0,0,0,136],[0,0,0,52],[0,0,0,13],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,11],[0,0,0,52],[0,0,0,136],[0,0,0,227],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,223],[0,0,0,68],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,15],[0,0,0,186],[0,0,0,255],[0,0,0,253],[0,0,0,178],[0,0,0,49],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,10],[0,0,0,71],[0,0,0,62],[0,0,0,25],[0,0,0,1],[0,0,0,1],[0,0,0,49],[0,0,0,178],[0,0,0,253],[0,0,0,255],[0,0,0,173],[0,0,0,10],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,107],[0,0,0,247],[0,0,0,254],[0,0,0,156],[0,0,0,19],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,27],[0,0,0,218],[0,0,0,246],[0,0,0,215],[0,0,0,143],[0,0,0,44],[0,0,0,0],[0,0,0,19],[0,0,0,156],[0,0,0,254],[0,0,0,248],[0,0,0,107],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,47],[0,0,0,224],[0,0,0,255],[0,0,0,174],[0,0,0,18],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,222],[0,0,0,93],[0,0,0,2],[0,0,0,18],[0,0,0,174],[0,0,0,255],[0,0,0,224],[0,0,0,46],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,2],[0,0,0,148],[0,0,0,255],[0,0,0,221],[0,0,0,45],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,240],[0,0,0,99],[0,0,0,0],[0,0,0,45],[0,0,0,221],[0,0,0,255],[0,0,0,148],[0,0,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,38],[0,0,0,225],[0,0,0,255],[0,0,0,125],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,56],[0,0,0,0],[0,0,0,125],[0,0,0,255],[0,0,0,225],[0,0,0,39],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,99],[0,0,0,255],[0,0,0,230],[0,0,0,43],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,165],[0,0,0,3],[0,0,0,42],[0,0,0,230],[0,0,0,255],[0,0,0,99],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,154],[0,0,0,255],[0,0,0,182],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,232],[0,0,0,45],[0,0,0,5],[0,0,0,182],[0,0,0,255],[0,0,0,154],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,188],[0,0,0,255],[0,0,0,139],[0,0,0,0],[0,0,0,2],[0,0,0,6],[0,0,0,5],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,254],[0,0,0,94],[0,0,0,0],[0,0,0,139],[0,0,0,255],[0,0,0,188],[0,0,0,8],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,16],[0,0,0,204],[0,0,0,255],[0,0,0,116],[0,0,0,0],[0,0,0,55],[0,0,0,184],[0,0,0,152],[0,0,0,13],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,27],[0,0,0,216],[0,0,0,252],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,253],[0,0,0,122],[0,0,0,0],[0,0,0,116],[0,0,0,255],[0,0,0,204],[0,0,0,15],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,17],[0,0,0,206],[0,0,0,255],[0,0,0,114],[0,0,0,0],[0,0,0,52],[0,0,0,175],[0,0,0,145],[0,0,0,12],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,67],[0,0,0,78],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,78],[0,0,0,40],[0,0,0,0],[0,0,0,114],[0,0,0,255],[0,0,0,206],[0,0,0,17],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,11],[0,0,0,194],[0,0,0,255],[0,0,0,133],[0,0,0,0],[0,0,0,1],[0,0,0,3],[0,0,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,133],[0,0,0,255],[0,0,0,194],[0,0,0,11],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,2],[0,0,0,164],[0,0,0,255],[0,0,0,172],[0,0,0,4],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,4],[0,0,0,172],[0,0,0,255],[0,0,0,164],[0,0,0,2],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,113],[0,0,0,255],[0,0,0,221],[0,0,0,32],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,32],[0,0,0,221],[0,0,0,255],[0,0,0,113],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,51],[0,0,0,235],[0,0,0,254],[0,0,0,105],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,105],[0,0,0,254],[0,0,0,235],[0,0,0,51],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,168],[0,0,0,255],[0,0,0,205],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,205],[0,0,0,255],[0,0,0,168],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,65],[0,0,0,237],[0,0,0,255],[0,0,0,146],[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,35],[0,0,0,37],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,146],[0,0,0,255],[0,0,0,237],[0,0,0,65],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,135],[0,0,0,254],[0,0,0,247],[0,0,0,121],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,4],[0,0,0,170],[0,0,0,179],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,121],[0,0,0,247],[0,0,0,254],[0,0,0,135],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,19],[0,0,0,173],[0,0,0,255],[0,0,0,246],[0,0,0,142],[0,0,0,24],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,160],[0,0,0,169],[0,0,0,6],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,24],[0,0,0,142],[0,0,0,246],[0,0,0,255],[0,0,0,173],[0,0,0,19],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,29],[0,0,0,175],[0,0,0,254],[0,0,0,253],[0,0,0,199],[0,0,0,93],[0,0,0,23],[0,0,0,1],[0,0,0,0],[0,0,0,21],[0,0,0,22],[0,0,0,1],[0,0,0,1],[0,0,0,23],[0,0,0,93],[0,0,0,199],[0,0,0,253],[0,0,0,254],[0,0,0,175],[0,0,0,29],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,21],[0,0,0,141],[0,0,0,241],[0,0,0,255],[0,0,0,250],[0,0,0,211],[0,0,0,156],[0,0,0,113],[0,0,0,91],[0,0,0,90],[0,0,0,113],[0,0,0,156],[0,0,0,211],[0,0,0,250],[0,0,0,255],[0,0,0,241],[0,0,0,141],[0,0,0,21],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,5],[0,0,0,71],[0,0,0,177],[0,0,0,240],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,254],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,240],[0,0,0,177],[0,0,0,71],[0,0,0,5],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,12],[0,0,0,70],[0,0,0,147],[0,0,0,206],[0,0,0,239],[0,0,0,252],[0,0,0,252],[0,0,0,239],[0,0,0,206],[0,0,0,147],[0,0,0,70],[0,0,0,12],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(resultico_array)):
    for j in range(len(resultico_array[0])):
        resultico_array[i][j] = [255,255,255,resultico_array[i][j][3]]
array_np = np.array(resultico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
results_icon = ImageTk.PhotoImage(image)




playico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[7,7,7,255],[3,3,3,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[2,2,2,255],[8,8,8,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[4,4,4,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[8,8,8,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[12,12,12,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[6,6,6,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[2,2,2,255],[1,1,1,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[9,9,9,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[2,2,2,255],[3,3,3,255],[3,3,3,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[9,9,9,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(playico_array)):
    for j in range(len(playico_array[0])):
        playico_array[i][j] = [255,255,255,playico_array[i][j][3]]

array_np = np.array(playico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
play_icon = ImageTk.PhotoImage(image)

pauseico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[5,5,5,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[10,10,10,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[26,26,26,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[6,6,6,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(pauseico_array)):
    for j in range(len(pauseico_array[0])):
        pauseico_array[i][j] = [255,255,255,pauseico_array[i][j][3]]

array_np = np.array(pauseico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
pause_icon = ImageTk.PhotoImage(image)

stopico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[9,9,9,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[8,8,8,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[17,17,17,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(stopico_array)):
    for j in range(len(stopico_array[0])):
        stopico_array[i][j] = [255,255,255,stopico_array[i][j][3]]

array_np = np.array(stopico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
stop_icon = ImageTk.PhotoImage(image)


undo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[6,6,6,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[4,4,4,128],[0,0,0,255],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[3,3,3,255],[0,0,0,128],[2,2,2,128],[0,0,0,128],[6,6,6,128],[8,8,8,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[1,1,1,255],[9,9,9,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[4,4,4,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,128],[0,0,0,128],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[8,8,8,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(undo_array)):
    for j in range(len(undo_array[0])):
        undo_array[i][j] = [210,210,210,undo_array[i][j][3]]

array_np = np.array(undo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
undo_icon = ImageTk.PhotoImage(image)

undo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[6,6,6,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[4,4,4,128],[0,0,0,255],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[3,3,3,255],[0,0,0,128],[2,2,2,128],[0,0,0,128],[6,6,6,128],[8,8,8,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[1,1,1,255],[9,9,9,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[4,4,4,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,128],[0,0,0,128],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[8,8,8,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(undo_array)):
    for j in range(len(undo_array[0])):
        undo_array[i][j] = [255,255,255,undo_array[i][j][3]]

array_np = np.array(undo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
undo_icon_w = ImageTk.PhotoImage(image)

redo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[8,8,8,128],[6,6,6,128],[0,0,0,128],[6,6,6,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[2,2,2,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[3,3,3,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,128],[6,6,6,128],[0,0,0,128],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[7,7,7,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[5,5,5,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[3,3,3,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,128],[6,6,6,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[28,28,28,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[4,4,4,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(redo_array)):
    for j in range(len(redo_array[0])):
        redo_array[i][j] = [210,210,210,redo_array[i][j][3]]

array_np = np.array(redo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
redo_icon = ImageTk.PhotoImage(image)

redo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[8,8,8,128],[6,6,6,128],[0,0,0,128],[6,6,6,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[2,2,2,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[3,3,3,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,128],[6,6,6,128],[0,0,0,128],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[7,7,7,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[5,5,5,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[3,3,3,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,128],[6,6,6,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[28,28,28,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[4,4,4,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(redo_array)):
    for j in range(len(redo_array[0])):
        redo_array[i][j] = [255,255,255,redo_array[i][j][3]]

array_np = np.array(redo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
redo_icon_w = ImageTk.PhotoImage(image)

zoom_in_array = [[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_in_array)):
    for j in range(len(zoom_in_array[0])):
        zoom_in_array[i][j] = [210,210,210,255-zoom_in_array[i][j][0]]

array_np = np.array(zoom_in_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_in_icon = ImageTk.PhotoImage(image)

zoom_in_array = [[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_in_array)):
    for j in range(len(zoom_in_array[0])):
        zoom_in_array[i][j] = [255,255,255,255-zoom_in_array[i][j][0]]

array_np = np.array(zoom_in_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_in_icon_w = ImageTk.PhotoImage(image)

zoom_out_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_out_array)):
    for j in range(len(zoom_out_array[0])):
        zoom_out_array[i][j] = [210,210,210,255-zoom_out_array[i][j][0]]

array_np = np.array(zoom_out_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_out_icon = ImageTk.PhotoImage(image)

zoom_out_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_out_array)):
    for j in range(len(zoom_out_array[0])):
        zoom_out_array[i][j] = [255,255,255,255-zoom_out_array[i][j][0]]

array_np = np.array(zoom_out_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_out_icon_w = ImageTk.PhotoImage(image)


left_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(left_array)):
    for j in range(len(left_array[0])):
        left_array[i][j] = [210,210,210,left_array[i][j][3]]

array_np = np.array(left_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
left_icon = ImageTk.PhotoImage(image)

left_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(left_array)):
    for j in range(len(left_array[0])):
        left_array[i][j] = [255,255,255,left_array[i][j][3]]

array_np = np.array(left_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
left_icon_w = ImageTk.PhotoImage(image)


right_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(right_array)):
    for j in range(len(right_array[0])):
        right_array[i][j] = [210,210,210,right_array[i][j][3]]


array_np = np.array(right_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
right_icon = ImageTk.PhotoImage(image)


right_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(right_array)):
    for j in range(len(right_array[0])):
        right_array[i][j] = [255,255,255,right_array[i][j][3]]


array_np = np.array(right_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
right_icon_w = ImageTk.PhotoImage(image)

mic_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[91,91,91,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[84,84,84,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[46,46,46,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[51,51,51,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[46,46,46,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[39,39,39,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(mic_array)):
    for j in range(len(mic_array[0])):
        mic_array[i][j] = [255,255,255,mic_array[i][j][3]]


array_np = np.array(mic_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
mic_icon = ImageTk.PhotoImage(image)

gun_array = [[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]]]
for i in range(len(gun_array)):
    for j in range(len(gun_array[0])):
        gun_array[i][j] = [255,255,255,gun_array[i][j][3]]

array_np = np.array(gun_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
gun_icon = ImageTk.PhotoImage(image)

for i in range(len(gun_array)):
    for j in range(len(gun_array[0])):
        gun_array[i][j] = [255,0,0,gun_array[i][j][3]]

array_np = np.array(gun_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
red_gun_icon = ImageTk.PhotoImage(image)


start_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[55,55,55,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[108,108,108,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[8,8,8,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[76,76,76,255],[104,104,104,255],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[91,91,91,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[14,14,14,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[78,78,78,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[49,49,49,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(start_array)):
    for j in range(len(start_array[0])):
        start_array[i][j] = [255,255,255,start_array[i][j][3]]

array_np = np.array(start_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
start_icon = ImageTk.PhotoImage(image)


sound_array = [[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[228,228,228],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[245,245,245],[255,255,255],[252,252,252],[252,252,252],[255,255,255],[251,251,251],[249,249,249],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[253,253,253],[254,254,254],[200,200,200],[252,252,252],[255,255,255],[253,253,253],[255,255,255],[226,226,226],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[251,251,251],[255,255,255],[254,254,254],[244,244,244],[246,246,246],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[250,250,250],[219,219,219],[249,249,249],[249,249,249],[255,255,255],[247,247,247],[255,255,255],[219,219,219],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[205,205,205],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[251,251,251],[118,118,118],[255,255,255],[248,248,248],[255,255,255],[255,255,255],[177,177,177],[253,253,253],[255,255,255],[253,253,253],[250,250,250],[255,255,255],[250,250,250],[254,254,254],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[208,208,208],[255,255,255],[253,253,253],[254,254,254],[255,255,255],[255,255,255],[183,183,183],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[173,173,173],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[241,241,241],[250,250,250],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[253,253,253],[252,252,252],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[109,109,109],[254,254,254],[255,255,255],[254,254,254],[253,253,253],[162,162,162],[253,253,253],[255,255,255],[255,255,255],[252,252,252],[197,197,197],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[254,254,254],[253,253,253],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[43,43,43],[252,252,252],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[255,255,255],[238,238,238],[238,238,238],[254,254,254],[248,248,248],[255,255,255],[224,224,224],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[253,253,253],[255,255,255],[255,255,255],[103,103,103],[251,251,251],[251,251,251],[253,253,253],[255,255,255],[251,251,251],[75,75,75],[255,255,255],[253,253,253],[255,255,255],[251,251,251],[133,133,133],[254,254,254],[255,255,255],[253,253,253],[254,254,254],[165,165,165],[255,255,255],[255,255,255],[255,255,255],[250,250,250],[244,244,244],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255]],[[250,250,250],[254,254,254],[255,255,255],[255,255,255],[252,252,252],[39,39,39],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[42,42,42],[248,248,248],[255,255,255],[255,255,255],[253,253,253],[96,96,96],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[142,142,142],[255,255,255],[255,255,255],[250,250,250],[255,255,255],[221,221,221],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[201,201,201],[187,187,187],[252,252,252],[255,255,255],[255,255,255],[146,146,146],[68,68,68],[255,255,255],[255,255,255],[253,253,253],[102,102,102],[249,249,249],[255,255,255],[252,252,252],[255,255,255],[167,167,167],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[202,202,202],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[249,249,249],[255,255,255],[253,253,253],[251,251,251],[252,252,252],[41,41,41],[251,251,251],[253,253,253],[252,252,252],[252,252,252],[45,45,45],[253,253,253],[251,251,251],[254,254,254],[156,156,156],[181,181,181],[255,255,255],[255,255,255],[255,255,255],[204,204,204],[253,253,253],[255,255,255],[251,251,251],[253,253,253],[197,197,197],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[247,247,247],[56,56,56],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[56,56,56],[250,250,250],[254,254,254],[253,253,253],[205,205,205],[123,123,123],[255,255,255],[253,253,253],[255,255,255],[232,232,232],[253,253,253],[255,255,255],[255,255,255],[254,254,254],[201,201,201],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[253,253,253],[255,255,255],[249,249,249],[51,51,51],[195,195,195],[253,253,253],[254,254,254],[255,255,255],[50,50,50],[254,254,254],[255,255,255],[253,253,253],[239,239,239],[104,104,104],[254,254,254],[255,255,255],[253,253,253],[244,244,244],[254,254,254],[253,253,253],[255,255,255],[254,254,254],[206,206,206],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[253,253,253],[255,255,255],[255,255,255],[253,253,253],[247,247,247],[49,49,49],[160,160,160],[253,253,253],[253,253,253],[255,255,255],[48,48,48],[255,255,255],[254,254,254],[255,255,255],[244,244,244],[100,100,100],[253,253,253],[251,251,251],[255,255,255],[249,249,249],[250,250,250],[255,255,255],[254,254,254],[255,255,255],[209,209,209],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253]],[[253,253,253],[255,255,255],[255,255,255],[254,254,254],[249,249,249],[249,249,249],[50,50,50],[201,201,201],[251,251,251],[249,249,249],[249,249,249],[54,54,54],[254,254,254],[254,254,254],[251,251,251],[236,236,236],[101,101,101],[255,255,255],[255,255,255],[252,252,252],[245,245,245],[253,253,253],[255,255,255],[254,254,254],[253,253,253],[201,201,201],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[252,252,252],[255,255,255],[244,244,244],[253,253,253],[71,71,71],[248,248,248],[251,251,251],[254,254,254],[251,251,251],[56,56,56],[253,253,253],[255,255,255],[255,255,255],[200,200,200],[133,133,133],[253,253,253],[255,255,255],[255,255,255],[224,224,224],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[197,197,197],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[255,255,255]],[[252,252,252],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[253,253,253],[33,33,33],[252,252,252],[255,255,255],[253,253,253],[244,244,244],[37,37,37],[255,255,255],[250,250,250],[251,251,251],[148,148,148],[197,197,197],[253,253,253],[254,254,254],[255,255,255],[197,197,197],[255,255,255],[252,252,252],[255,255,255],[255,255,255],[196,196,196],[254,254,254],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255]],[[255,255,255],[250,250,250],[255,255,255],[255,255,255],[251,251,251],[124,124,124],[216,216,216],[252,252,252],[249,249,249],[250,250,250],[114,114,114],[94,94,94],[255,255,255],[255,255,255],[255,255,255],[92,92,92],[249,249,249],[255,255,255],[252,252,252],[250,250,250],[164,164,164],[255,255,255],[253,253,253],[255,255,255],[252,252,252],[206,206,206],[252,252,252],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[253,253,253],[254,254,254],[255,255,255],[254,254,254],[253,253,253],[51,51,51],[255,255,255],[250,250,250],[245,245,245],[250,250,250],[58,58,58],[246,246,246],[254,254,254],[253,253,253],[251,251,251],[96,96,96],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[137,137,137],[253,253,253],[255,255,255],[254,254,254],[255,255,255],[236,236,236],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255]],[[253,253,253],[255,255,255],[254,254,254],[255,255,255],[75,75,75],[255,255,255],[253,253,253],[251,251,251],[252,252,252],[229,229,229],[148,148,148],[252,252,252],[253,253,253],[254,254,254],[247,247,247],[168,168,168],[252,252,252],[253,253,253],[255,255,255],[250,250,250],[175,175,175],[252,252,252],[255,255,255],[254,254,254],[246,246,246],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[254,254,254],[253,253,253],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[253,253,253],[254,254,254],[248,248,248],[249,249,249],[254,254,254],[23,23,23],[241,241,241],[255,255,255],[246,246,246],[249,249,249],[238,238,238],[251,251,251],[253,253,253],[255,255,255],[255,255,255],[222,222,222],[254,254,254],[254,254,254],[254,254,254],[254,254,254],[214,214,214],[253,253,253],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255]],[[254,254,254],[255,255,255],[255,255,255],[254,254,254],[252,252,252],[250,250,250],[251,251,251],[253,253,253],[255,255,255],[243,243,243],[255,255,255],[255,255,255],[245,245,245],[253,253,253],[96,96,96],[252,252,252],[254,254,254],[255,255,255],[254,254,254],[139,139,139],[255,255,255],[254,254,254],[252,252,252],[255,255,255],[204,204,204],[249,249,249],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[252,252,252],[252,252,252],[252,252,252],[252,252,252],[255,255,255],[249,249,249],[248,248,248],[254,254,254],[228,228,228],[255,255,255],[247,247,247],[251,251,251],[254,254,254],[253,253,253],[240,240,240],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[254,254,254],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[252,252,252],[253,253,253],[250,250,250],[249,249,249],[255,255,255],[255,255,255],[188,188,188],[252,252,252],[251,251,251],[249,249,249],[254,254,254],[153,153,153],[253,253,253],[255,255,255],[252,252,252],[255,255,255],[250,250,250],[255,255,255],[252,252,252],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[247,247,247],[247,247,247],[255,255,255],[249,249,249],[200,200,200],[245,245,245],[253,253,253],[251,251,251],[252,252,252],[245,245,245],[250,250,250],[250,250,250],[250,250,250],[255,255,255],[254,254,254],[202,202,202],[251,251,251],[254,254,254],[255,255,255],[255,255,255],[251,251,251],[254,254,254],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[250,250,250],[254,254,254],[253,253,253],[253,253,253],[255,255,255],[247,247,247],[249,249,249],[243,243,243],[249,249,249],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[250,250,250],[254,254,254],[255,255,255],[248,248,248],[254,254,254],[254,254,254],[248,248,248],[250,250,250],[250,250,250],[255,255,255],[251,251,251],[210,210,210],[255,255,255],[252,252,252],[252,252,252],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[251,251,251],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[249,249,249],[253,253,253],[255,255,255],[245,245,245],[255,255,255],[252,252,252],[254,254,254],[245,245,245],[254,254,254],[255,255,255],[246,246,246],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[251,251,251],[250,250,250],[255,255,255],[248,248,248],[252,252,252],[253,253,253],[248,248,248],[255,255,255],[253,253,253],[239,239,239],[251,251,251],[253,253,253],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]]]

for i in range(len(sound_array)):
    for j in range(len(sound_array[0])):
        sound_array[i][j] = [255,255,255,255-sound_array[i][j][0]]



array_np = np.array(sound_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
sound_icon = ImageTk.PhotoImage(image)



wind_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[239,239,239,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[53,53,53,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[230,230,230,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[224,224,224,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[39,39,39,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[230,230,230,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[170,170,170,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[128,128,128,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[89,89,89,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[128,128,128,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[53,53,53,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[153,153,153,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[201,201,201,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[209,209,209,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[246,246,246,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[251,251,251,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[235,235,235,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[128,128,128,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[159,159,159,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[195,195,195,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[224,224,224,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[31,31,31,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[136,136,136,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(wind_array)):
    for j in range(len(wind_array[0])):
        wind_array[i][j] = [255,255,255,255-wind_array[i][j][0]]



array_np = np.array(wind_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
wind_icon = ImageTk.PhotoImage(image)


"""
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
"""
#icon = Image.open('images/icon.ico')
#iconbg = ImageTk.PhotoImage(icon)
#root.state("zoomed")
root.resizable(False,False)
root.geometry(f'{window_width}x{window_height}+{99999}+{99999}')
#root.iconphoto(False,main_icon)
root.deiconify()
total_instances = 0
def create_instance():
    global total_instances
    total_instances += 1
    video_recorder = Instance(root)
    video_recorder.root.mainloop()
#tk.Button(text = "Create Instance", command = create_instance).place(x=0,y = 0, anchor = "nw")

create_instance()
root.mainloop()


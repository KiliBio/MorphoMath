#!/usr/bin/python
'''
Code written in Python 3.5 by KiliBio
'''
'''
Missions accomplished:
    General design ✓
    Point-specific mode ✓
    Ratio-specific mode
    Angle-specific mode
    Area-specific mode
    all to log_file ✓
'''

import tkinter as tk
import tkinter.messagebox
import csv
from tkinter import ttk
from PIL import ImageTk, Image, ImageGrab
from math import sqrt, floor
from datetime import datetime
import time


title = "MorphoMathv1.0"
the_font = ("Courier 10")
gen_padx = 5
gen_pady = 2

class MorphoMath(tk.Tk):
    # the MorphoMath class inherits from the Tk class in the tk module
    def __init__(self, *arg, **kwargs):  # the init function accepts arguments and keyword arguments, will always run
        '''__init__ function to initiate the automatic function to create the widgets'''
        tk.Tk.__init__(self, *arg, **kwargs)
        # sets the size of the main window automatically to the size of the screen
        self.master_width, self.master_height = self.winfo_screenwidth(), self.winfo_screenheight()
        print(self.master_width, self.master_height)
        self.geometry('%dx%d+0+0' % (self.master_width-18, self.master_height-85))
        # icon in the upper-left corner
        tk.Tk.iconbitmap(self,
                         default="C:/morphoMathicon2.ico")

        # title of the window
        tk.Tk.wm_title(self, title)

        ttk.Style().configure('button_design.TButton', foreground='grey5',
                              background='RoyalBlue2', font='Courier 11 bold')

        self.mainframe = tk.Frame(self)
        #self.mainframe["bg"] = "khaki2"
        self.mainframe.pack(side="top", fill="both", expand=True)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)  # weight --> prioritizes things
        self["bg"] = "khaki2"
        self.allframes = {}  # the allframes dictionary stores all frames and make them acessable to switch between windows

        for frame in (WarningPage, StartPage,
                      Point_spec_mode, Distance_spec_mode, Angles_spec_mode, Area_spec_mode):
            '''this for loop consists of all windows in the application'''
            self.specific_frame = frame(self.mainframe, self)

            self.allframes[frame] = self.specific_frame

            self.specific_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WarningPage)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.FileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.FileMenu)
        self.FileMenu.add_command(label="Point-Mode", command=None)
        # there is no controller here which could be accessed!
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Export...", command=None)
        self.FileMenu.add_command(label="Import...", command=None)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Quit", command=None)

        self.EditMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.EditMenu)
        self.EditMenu.add_command(label="Copy", command=None)
        self.EditMenu.add_command(label="Paste", command=None)
        self.EditMenu.add_command(label="Find", command=None)

        self.HelpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.HelpMenu)
        self.HelpMenu.add_command(label="Help...", command=None)

    def show_frame(self, cont):
        self.specific_frame = self.allframes[cont]
        self.specific_frame.tkraise()

    def get_page(self, page_class):
        return self.allframes[page_class]

class WarningPage(tk.Frame):  # Start Page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.warning_page_frame = tk.Frame(self)
        self.warning_page_frame.config(height=300, width=600)
        self.warning_page_frame.pack(anchor="center")

        self.betweenframe = tk.Frame(self.warning_page_frame)
        self.betweenframe.config(height=200)
        self.betweenframe.pack(anchor="center")
        self.textframe = tk.Frame(self.warning_page_frame)
        self.textframe.config(height=200)
        self.textframe.pack(fill="both",anchor="center")

        self.warninglabel = tk.Label(self.textframe)
        self.warninglabel["text"] = """WARNING: Use %s at your own risks!\n
        There is no promise of exact calculations or any kind of warranty!\n
        Check the source-code to make sure that the calculations are correct or in a way you want them to.""" % (title)
        self.warninglabel["font"] = "Courier 10"
        self.warninglabel["bg"] = "tomato"
        self.warninglabel.pack()

        self.buttonframe = tk.Frame(self.warning_page_frame)
        self.buttonframe.pack(anchor="center")

        self.agree_button = ttk.Button(self.buttonframe, command=lambda: controller.show_frame(StartPage))
        self.agree_button["style"] = 'button_design.TButton'
        self.agree_button["text"] = "Agree"
        self.agree_button["cursor"] = "circle"
        self.agree_button.pack(side="left", pady=50, padx=50)

        self.disagree_button = ttk.Button(self.buttonframe, command=quit)
        self.disagree_button["style"] = 'button_design.TButton'
        self.disagree_button["text"] = "Disagree"
        self.disagree_button["cursor"] = "circle"
        self.disagree_button.pack(side="right", pady=50, padx=50)

        self.textframe2 = tk.Frame(self.warning_page_frame)
        self.textframe2.config(height=200)
        self.textframe2.pack(fill="both", anchor="center")

        self.warninglabel = tk.Label(self.textframe2)
        self.warninglabel["text"] = """From the author of this program it is strongly recommended,\n
        to use this program and the results with an absolute critical evaluation."""
        self.warninglabel["font"] = "Courier 10"
        self.warninglabel.pack()

class StartPage(tk.Frame):  # Start Page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.startpagelabelframe = tk.Frame(self)
        self.startpagelabelframe.config(height=50)
        self.startpagelabelframe.pack(side="top")
        self.startpagelabelframe.grid_rowconfigure(0, weight=1)
        self.startpagelabelframe.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.startpagelabelframe)
        self.title_label["text"] = title
        self.title_label["font"] = "Courier 14 bold"
        self.title_label.pack(fill="both", anchor="center")

        self.startpagebuttonframe = tk.Frame(self)
        self.startpagebuttonframe.config(height=50)
        self.startpagebuttonframe.pack(side="top", fill="x", anchor="center")

        self.point_spec_button = ttk.Button(self.startpagebuttonframe, command=lambda: controller.show_frame(Point_spec_mode))
        self.point_spec_button["text"] = "Point Mode"
        self.point_spec_button["style"] = 'button_design.TButton'
        self.point_spec_button["cursor"] = "circle"
        self.point_spec_button.pack(side="left", anchor="center", padx=100, pady=50)

        self.distance_spec_button = ttk.Button(self.startpagebuttonframe, command=lambda: controller.show_frame(Distance_spec_mode))
        self.distance_spec_button["text"] = "Distance Mode"
        self.distance_spec_button["style"] = 'button_design.TButton'
        self.distance_spec_button["cursor"] = "circle"
        self.distance_spec_button.pack(side="left", anchor="center", padx=100, pady=50)

        self.angles_spec_button = ttk.Button(self.startpagebuttonframe, command=lambda: controller.show_frame(Angles_spec_mode))
        self.angles_spec_button["text"] = "Angle Mode"
        self.angles_spec_button["style"] = 'button_design.TButton'
        self.angles_spec_button["cursor"] = "circle"
        self.angles_spec_button.pack(side="right", anchor="center", padx=100, pady=50)

        self.area_spec_button = ttk.Button(self.startpagebuttonframe, command=lambda: controller.show_frame(Area_spec_mode))
        self.area_spec_button["text"] = "Area Mode"
        self.area_spec_button["style"] = 'button_design.TButton'
        self.area_spec_button["cursor"] = "circle"
        self.area_spec_button.pack(side="right", anchor="center", padx=100, pady=50)

        self.startpagelabelframe = tk.Frame(self)
        self.startpagelabelframe.config(height=50)
        self.startpagelabelframe.pack(side="top", fill="x", anchor="center")

        self.point_spec_label = tk.Label(self.startpagelabelframe, width=40, height=200)
        self.point_spec_label["text"] = "The Point Mode allows you to mark \n" \
                                        "specific morphological landmarks on \n" \
                                        "the plant.\n" \
                                        "The distances between all the points \n" \
                                        "and ratios between the all those \n" \
                                        "distances are than calculated and \n" \
                                        "stored in a separate csv-file."
        self.point_spec_label.pack(side="left", anchor="center", padx=10, pady=20)

        self.point_spex_label = tk.Label(self.startpagelabelframe, width=40, height=200)
        self.point_spex_label["text"] = "The Distance Mode allows you \n" \
                                        "to mark morphological \n" \
                                        "significant distances, \n" \
                                        "of which the ratio are directly \n" \
                                        "calculated and stored in an \n" \
                                        "additional separate csv-file."
        self.point_spex_label.pack(side="left", anchor="center", padx=10, pady=20)

        self.point_spet_label = tk.Label(self.startpagelabelframe, width=40, height=200)
        self.point_spet_label["text"] = "YOU NEED TO RELATE THIS \n" \
                                        "DATA TO SOMETHING TO \n" \
                                        "TO BECOME FROM VALUE!!! \n" \
                                        "The Area Mode allows \n" \
                                        "you to store one or \n" \
                                        "more specific areas in \n" \
                                        "a structure with morphological \n" \
                                        "relevant landmark data and \n" \
                                        "stores those values in a \n" \
                                        "separate csv.file."

        self.point_spet_label.pack(side="right", anchor="center", padx=10, pady=20)

        self.point_spex_label = tk.Label(self.startpagelabelframe, width=40, height=200)
        self.point_spex_label["text"] = "YOU NEED TO RELATE THIS \n" \
                                        "DATA TO SOMETHING TO \n" \
                                        "TO BECOME FROM VALUE!!! \n" \
                                        "The angle mode allows \n" \
                                        "you to store one or more\n" \
                                        "specific angles in a structure \n" \
                                        "with morphological relevant landmark \n" \
                                        "data and stores those values in \n" \
                                        "a separate csv.file"
        self.point_spex_label.pack(side="right", anchor="center", padx=10, pady=20)

class Point_spec_mode(tk.Frame):
    '''the Point-specific mode allow the user to specify an arbitrary amount of points and get a file of ratios'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.point_speclabelframe = tk.Frame(self)
        self.point_speclabelframe.config(height=40)
        self.point_speclabelframe.pack(side="top")
        self.point_speclabelframe.grid_rowconfigure(0, weight=1)
        self.point_speclabelframe.grid_columnconfigure(0, weight=1)

        self.main_label = tk.Label(self.point_speclabelframe)
        self.main_label["text"] = "Point specific mode"
        self.main_label["font"] = "Courier 11 bold"
        self.main_label.pack(fill="both", anchor="center")

        self.point_specpath_input_frame = tk.Frame(self)
        self.point_specpath_input_frame.config(height=50)
        self.point_specpath_input_frame.pack(side="top", fill="x", anchor="center")

        ### entry-field to enter the image path
        global pic_path
        self.pic_path = tk.Entry(self.point_specpath_input_frame)
        self.pic_path["bg"] = "mint cream"
        self.pic_path["fg"] = "grey25"
        self.pic_path["bd"] = 2
        self.pic_path["cursor"] = "xterm"
        self.pic_path["width"] = 80
        self.pic_path.delete(0, "end")
        self.pic_path.insert(0, "C:/input")
        self.pic_path.pack(side="left", fill="x", expand=True, anchor="center", padx=50, pady=10)
        self.pic_path.bind("<Return>", self.upload_by_enter)

        ### in the default-status the uploaded image will be resized, because the image should be taken by powerful
        ### cameras; the box should be checked if smaller structures are considered
        self.resize_decision = True
        self.resize_checkbox = ttk.Checkbutton(self.point_specpath_input_frame,
                                              command=self.image_resize_question)
        self.resize_checkbox["text"] = "Not Resize image"
        self.resize_checkbox.pack(side="left", anchor="center")

        ### upload button, which will create the canvas with the image specified in the image path entry field
        self.uploadbutton = ttk.Button(self.point_specpath_input_frame,
                                      command=self.image_to_canvas)
        self.uploadbutton["style"] = 'button_design.TButton'
        self.uploadbutton["cursor"] = "circle"
        self.uploadbutton["text"] = "✅"
        self.uploadbutton.pack(side="right", anchor="center", padx=50, pady=10)

    def upload_by_enter(self, event):
        '''this function sorely connects the "Press Enter" function the upload function'''
        self.image_to_canvas()

    def image_resize_question(self):
        '''this function will activated through checking the box and the image will not be resized'''
        self.resize_decision = False
        return self.resize_decision

    def image_to_canvas(self):
        '''this function loads the image'''
        try:
            '''if the image exists the image will be opened, if not an IOError will be returned'''
            f = open(self.pic_path.get())
            f.close()
            self.image_path = self.pic_path.get()

            ### initialing lists, which are used by the program to store the values of the points
            self.all_points = []
            self.x_cor_points = []
            self.y_cor_points = []
            self.point_names = []
            self.names_with_points = []
            self.distance_between_points = []
            self.pointname = "No Pointname given"

            ### options and entry fields on the right side
            ### everything has been packed into a canvas to be able to scroll around it with growing size, due to points
            self.right_side_canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
            self.right_side_canvas.config(width=self.winfo_screenwidth() - 1150,
                                          height=self.winfo_screenheight() - 135)

            self.point_specimagespec_frame = tk.Frame(self.right_side_canvas, background="#ffffff")
            self.verticalbar_right = tk.Scrollbar(self, orient="vertical", command=self.right_side_canvas.yview)
            self.right_side_canvas.configure(yscrollcommand=self.verticalbar_right.set)
            self.verticalbar_right.pack(side="right", fill="y")
            self.right_side_canvas.pack(side="right", fill="x", expand=True)

            self.right_side_canvas.create_window((4, 4), window=self.point_specimagespec_frame,
                                                 anchor="n", tags="self.frame")

            ### with every pressed "Enter" the Frame will be updated and made available for the scrollbar
            self.point_specimagespec_frame.bind("<Configure>", self.onFrameConfigure)

            self.populate()

            # self.right_side_canvas.config(scrollregion=(self.right_side_canvas.winfo_x(),
            #                                            self.right_side_canvas.winfo_y(),
            #                                            self.right_side_canvas.winfo_width(),
            #                                            self.right_side_canvas.winfo_height()))
        except IOError:
            tkinter.messagebox.showinfo("Error Message", "Image couldn't be found in image path.")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.right_side_canvas.configure(scrollregion=self.right_side_canvas.bbox("all"))

    def populate(self):
        ''' this function lets the sidebar grow with newly added labels'''
        ### head-label: tells the user that this is the point specifier
        self.spec_label = tk.Label(self.point_specimagespec_frame)
        self.spec_label["text"] = "Point specifier"
        self.spec_label["font"] = "Courier 8 bold"
        self.spec_label.pack(side="top", anchor="center", padx=5, pady=5)

        self.spec_label1 = tk.Label(self.point_specimagespec_frame)
        self.spec_label1["text"] = "1.Define point|2.Hit Enter|3.Mark"
        self.spec_label1["font"] = "Courier 8"
        self.spec_label1.pack(side="top", anchor="center", padx=5, pady=5)

        ### entry-field to enter the names of the points
        self.point_spec = tk.Entry(self.point_specimagespec_frame)
        self.point_spec["bg"] = "mint cream"
        self.point_spec["fg"] = "grey25"
        self.point_spec["bd"] = 2
        self.point_spec["cursor"] = "xterm"
        self.point_spec["width"] = 40
        self.point_spec.pack(side="top", anchor="center", padx=5, pady=5)
        self.point_spec.bind("<Return>", self.point_name_append)

        self.print_to_frame = tk.Frame(self.point_specimagespec_frame)
        self.print_to_frame.config(width=80, height=80)
        self.print_to_frame.pack(side="top", fill="x", anchor="center")

        self.between_label = tk.Label(self.print_to_frame)
        self.between_label.config(width=40, height=1)
        self.between_label["font"] = "Courier 8 bold"
        self.between_label["text"] = " "
        self.between_label.pack(side="bottom", anchor="center", pady=1)

        ### label to for the file specifier, which names the output file
        self.file_spec_label = tk.Label(self.point_specimagespec_frame)
        self.file_spec_label["text"] = "Name the Output File"
        self.file_spec_label["font"] = "Courier 8"
        self.file_spec_label.pack(side="top", anchor="center", padx=5, pady=5)

        ### Entry where the output file name is specified
        self.save_to_file_name = tk.Entry(self.point_specimagespec_frame)
        self.save_to_file_name["bg"] = "mint cream"
        self.save_to_file_name["fg"] = "grey25"
        self.save_to_file_name["bd"] = 2
        self.save_to_file_name["cursor"] = "xterm"
        self.save_to_file_name["width"] = 40
        self.save_to_file_name.pack(side="top", anchor="center", padx=5, pady=5)
        self.save_to_file_name.bind("<Return>", self.all_done_by_enter)

        self.all_done_button = ttk.Button(self.point_specimagespec_frame,
                                         command=self.all_done_func)
        self.all_done_button["style"] = 'button_design.TButton'
        self.all_done_button["cursor"] = "circle"
        self.all_done_button["text"] = "✅ ALL DONE ✅"
        self.all_done_button.pack(side="bottom", anchor="center", padx=5, pady=5)

        ### frame for the imagecanvas and the image all_points
        self.point_specimagecanvas_frame = tk.Frame(self)
        self.point_specimagecanvas_frame.config(width=1200)
        self.point_specimagecanvas_frame.pack(side="top", fill="x", anchor="center")

        self.image_resize(self.image_path)

        ### creates the Canvas where the image and scrollbars are stored
        self.photocanvas = tk.Canvas(self.point_specimagecanvas_frame, width=1150, height=1000)
        self.photocanvas.create_image(self.imagex.width() / 2, self.imagex.height() / 2,
                                      anchor="center", image=self.imagex, tags="bg_img")
        self.photocanvas.xview_moveto(0)
        self.photocanvas.yview_moveto(0)
        self.photocanvas["cursor"] = "crosshair"
        self.photocanvas["highlightthickness"] = 5

        self.horizontalbar = tk.Scrollbar(self.point_specimagecanvas_frame, orient=tk.HORIZONTAL)
        self.horizontalbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.verticalbar = tk.Scrollbar(self.point_specimagecanvas_frame, orient=tk.VERTICAL)
        self.verticalbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontalbar.config(command=self.photocanvas.xview)
        self.verticalbar.config(command=self.photocanvas.yview)
        self.photocanvas.config(width=950, height=1000)
        self.photocanvas.config(scrollregion=(2, 2, self.imagex.width(), self.imagex.height()))
        self.photocanvas.config(xscrollcommand=self.horizontalbar.set, yscrollcommand=self.verticalbar.set)
        self.photocanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ### binds left-mouse-button to the point and the right-mouse button to the graph method
        self.photocanvas.bind("<Button-1>", self.point)
        self.photocanvas.bind("<Button-3>", self.graph)

    def image_resize(self, image_path):
        ''' gets the image_path and stores it in the imagex variable '''
        if self.resize_decision == True:
            ### if the resizing_box remains empty the image will be resized according to this rules
            self.imagex = ImageTk.PhotoImage(file=image_path)

            ### this gets the dimensions of the inputted image
            self.originalwidth, self.originalheight = self.imagex.width(), self.imagex.height()

            ### resizing the image
            if self.imagex.width() > 1000:
                ### the size_factor is an individual measure, larger pictures will have a larger size_factor
                self.size_factor = floor(self.imagex.width() / 1000)

                ### and here is the size_factor applied
                image = Image.open(self.image_path)
                image = image.resize(
                    (self.imagex.width() // self.size_factor, self.imagex.height() // self.size_factor)
                    , Image.ANTIALIAS)
                self.imagex = ImageTk.PhotoImage(image)
            else:
                self.size_factor = 1
                pass
        else:
            ### if the resizing_box is checked the image remains in the same size and and size_factor will be 1
            self.imagex = ImageTk.PhotoImage(file=image_path)
            self.originalwidth, self.originalheight = self.imagex.width(), self.imagex.height()
            self.size_factor = 1

        self.manipulatedwidth, self.manipulatedheight = self.imagex.width(), self.imagex.height()

    def point_name_append(self, event):
        '''recieves the name of the points as specified by the user, 
        appends it to the list and prints it to the window'''

        ### recieves the point name from the entry area and appends it to the point_name list
        self.pointname = self.point_spec.get()
        self.point_names.append(self.pointname)

        self.value_label = tk.Label(self.print_to_frame)
        self.value_label.config(width=40, height=1)
        self.value_label["font"] = "Courier 8 bold"
        self.value_label["bg"] = "SeaGreen1"
        self.value_label["fg"] = "black"
        self.value_label.pack(side="top", anchor="center", pady=1)
        ### this adds the number of the point and the actual number to the point-list
        self.value_label.configure(text="(%d) %s" % (len(self.point_names), self.pointname))

        self.point_spec.delete(0, 'end')
        return self.point_names, self.pointname

    def point(self, event):
        '''this function creates a point(oval) around the clicked point'''
        self.x, self.y = self.photocanvas.canvasx(event.x), self.photocanvas.canvasy(event.y)
        self.x_cor, self.y_cor = int(self.x), int(self.y)
        self.last_point = self.photocanvas.create_oval(self.x_cor - 3, self.y_cor - 3,
                                                       self.x_cor + 3, self.y_cor + 3, fill="tomato")
        ### appending the x-coordinate to lists
        self.all_points.append(self.x_cor)
        self.x_cor_points.append(self.x_cor)

        ### appending the y-coordinate to lists
        self.all_points.append(self.y_cor)
        self.y_cor_points.append(self.y_cor)

        self.coor_label = tk.Label(self.print_to_frame)
        self.coor_label.config(width=40, height=1)
        self.coor_label["font"] = "Courier 8 bold"
        self.coor_label["bg"] = "CadetBlue1"
        self.coor_label["fg"] = "black"
        self.coor_label.pack(side="top", anchor="center", pady=1)
        self.coor_label.configure(
            text="(%d) X: %d  |  Y: %d" % ((len(self.all_points) / 2), self.x_cor, self.y_cor))

        try:
            ### if there are points in the all-points list, the point names will be displayed onto the screen
            self.label_on_canvas = tk.Label(self.photocanvas)
            self.label_on_canvas["font"] = "Courier 6"
            self.label_on_canvas["bg"] = "White"
            self.label_on_canvas["fg"] = "black"
            self.label_on_canvas["text"] = ""
            self.label_on_canvas.pack()
            self.label_on_canvas.configure(text="(%d) %s" % ((len(self.all_points) / 2), self.pointname))
            # self.label_on_canvas.configure(text="%s" % (self.point_names[(len(self.all_points) // 2) - 1]))

            ### if/else to arrange the coordinate value names away from the center
            ### which could possibly cover other important parts of the image
            if self.x_cor < (self.imagex.width() // 2):  # on left side
                if self.y_cor < (self.imagex.height() // 2):  # on top
                    self.photocanvas.create_window(self.x_cor - 35, self.y_cor - 35,
                                                   window=self.label_on_canvas)
                else:  # on bottom
                    self.photocanvas.create_window(self.x_cor - 35, self.y_cor + 35,
                                                   window=self.label_on_canvas)
            else:  # on right side
                if self.y_cor < (self.imagex.height() // 2):  # on top
                    self.photocanvas.create_window(self.x_cor + 35, self.y_cor - 35,
                                                   window=self.label_on_canvas)
                else:  # on bottom
                    self.photocanvas.create_window(self.x_cor + 35, self.y_cor + 35,
                                                   window=self.label_on_canvas)
        except IndexError:
            ### if no points have been named/identified an IndexError will occur
            tkinter.messagebox.showinfo("Error Message", "Marked points on Image hasn't been defined yet")
            self.label_on_canvas.configure(text="undefined point")
            self.photocanvas.create_window(self.x_cor - 35, self.y_cor - 35, window=self.label_on_canvas)
            self.photocanvas.delete(self.last_point)
            self.coor_label.destroy()
            del self.all_points[-2:]
            del self.x_cor_points[-2:]
            del self.y_cor_points[-2:]
        return self.all_points

    def graph(self, event):
        '''this function creates a line between the points just to physically see the distance 
        without effecting anything in the calculations'''
        global theline
        self.photocanvas.create_line(self.all_points, tags="theline", width=4, fill="tomato")

    def all_done_by_enter(self, event):
        '''this function will be called by hitting Enter in the output file name entry area'''
        self.all_done_func()

    def all_done_func(self):
        '''Handler: is called, when the "All done" Button is pressed or the Enter Button is hit; 
        initiates calculations and print to file function'''

        ### returns the user the time the program has been used to mark and specify the points
        enter_time = time.time()
        print("Enter Time: --- %d minutes %0.3f seconds ---" %
              (((enter_time - start_time) // 60), (enter_time - start_time) % 60))
        self.num_of_calcs(len(self.point_names))

        if self.all_points == [] or self.point_names == []:
            ### either no point has been marked on the foto or no points has been given a name
            tkinter.messagebox.showinfo("Error Message", "No points have been marked on the image \n"
                                                         "or none of the points have been named!")
        elif (len(self.all_points) / 2) != len(self.point_names):
            ### the number of marked points and the number of named points doesn't match
            tkinter.messagebox.showinfo("Error Message",
                                        "Number of marked points and Number of Named points doesn't match!")
        else:
            ### everything is ok --> visible part of the image-canvas will be printed and saved to the output folder
            self.snapsaveCanvas()
            with open('C:/output'
                              + self.save_to_file_name.get() + '.csv', "w") as self.csv_file:
                self.file_to_write = csv.writer(self.csv_file, lineterminator='\n')
                self.file_to_write.writerow(["--------MAIN INFORMATION ABOUT THE FILE--------"])
                self.file_to_write.writerow(["FILE NAME", self.save_to_file_name.get()])
                self.file_to_write.writerow(["PATH IMAGE", self.pic_path.get()])
                self.file_to_write.writerow(["DATE CREATED", str(datetime.now())])
                self.file_to_write.writerow(
                    ["ORIGINAL IMAGE DIMENSION", self.originalwidth, self.originalheight])
                self.file_to_write.writerow(["COMPRESSED IMAGE DIMENSION", self.manipulatedwidth,
                                             self.manipulatedheight, "Factor %s" % (self.size_factor)])

                ### calls the points and calculations function
                self.all_points_and_calculations_to_file()
                self.csv_file.close()
            calc_time = time.time()
            print("Calc Time: --- %d minutes %0.3f seconds ---" %
                  (((calc_time - enter_time) // 60), (calc_time - enter_time) % 60))

            ### terminates the program
            self.quit()

    def num_of_calcs(self, x):
        '''control function, which returns the numbers calculations the program performs'''
        number = x
        print('Number of points:', number)
        firstresult = 0
        secondresult = 0
        for i in range(0, number):
            firstresult += i
        print('Number of distances:', firstresult)
        for j in range(0, firstresult):
            secondresult += j
        print('Number of ratios:', secondresult)

    def all_points_and_calculations_to_file(self):
        '''this function stores all points, all calculation about the distances and ratios in the image'''
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["--------COORDINATES OF ALL POINTS--------"])
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["NAME OF THE POINT", "X-COORDINATE", "Y-COORDINATE"])

        for i in range(len(self.point_names)):
            ### appends in point name list: NAME, X, Y and prints those three values to the output file
            self.names_with_points.append(self.point_names[i])
            self.names_with_points.append(self.x_cor_points[i])
            self.names_with_points.append(self.y_cor_points[i])
            self.file_to_write.writerow([self.point_names[i], self.x_cor_points[i], self.y_cor_points[i]])

        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["--------DISTANCES BETWEEN POINTS--------"])
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["1ST POINT->2ND POINT", "DISTANCE"])

        while self.names_with_points != []:
            ### pops of the keys with their respective points from the first position
            key1 = self.names_with_points.pop(0)
            x1 = self.names_with_points.pop(0)
            y1 = self.names_with_points.pop(0)

            for i in range(0, len(self.names_with_points), 3):
                ### to calculate the distances all other distances between key1 are calculated
                key2 = self.names_with_points[i]
                x2 = self.names_with_points[i + 1]
                y2 = self.names_with_points[i + 2]

                ### distance result in a X-Y plane are simply calculated through the Pythagorean theorem
                result = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

                ### the distances are than stored in a list in a similar fashion DISTANCE : NUMBER VALUE
                self.distance_between_points.append('%s->%s' % (key1, key2))
                self.distance_between_points.append(result)
                self.file_to_write.writerow(['%s->%s' % (key1, key2), "%0.4f" % result])

        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["--------RATIO BETWEEN EACH DISTANCES--------"])
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["1ST DIST/2ND DIST", "RATIO"])

        while self.distance_between_points != []:
            ### the ratios are again calculated similarly
            ### the first distance is poped of with its value
            distance1 = self.distance_between_points.pop(0)
            num1 = self.distance_between_points.pop(0)
            number1 = float(num1)

            for i in range(0, len(self.distance_between_points), 2):
                ### distance1 is then compared to all other distances
                distance2 = self.distance_between_points[i]
                num2 = self.distance_between_points[i + 1]
                number2 = float(num2)
                normal_result = number1 / number2
                reversed_result = number2 / number1
                self.file_to_write.writerow(["%s/%s" % (distance1, distance2), "%0.4f" % (normal_result)])
                self.file_to_write.writerow(["%s/%s" % (distance2, distance1), "%0.4f" % (reversed_result)])
                self.file_to_write.writerow([""])

    def snapsaveCanvas(self):
        ''' this function is called, when all inputs by the user are done and takes a screenshot of the image canvas'''
        canvas = self.canvas_info()  # Get Window Coordinates of Canvas
        self.grabcanvas = ImageGrab.grab(bbox=canvas).save(
            'C:/output'
            + self.save_to_file_name.get() + '_image_out' + '.jpg')

    def canvas_info(self):
        '''part of the snapsaveCanvas function, gets the information about the visible canvas'''
        x = self.photocanvas.winfo_rootx() + self.photocanvas.winfo_x()
        y = self.photocanvas.winfo_rooty() + self.photocanvas.winfo_y()
        x1 = x + self.photocanvas.winfo_width()
        y1 = y + self.photocanvas.winfo_height()
        box = (x, y, x1, y1)
        return box

class Distance_spec_mode(tk.Frame):
    '''the Distance specific mode lets the user specify ratios that he/she thinks are significant to compare'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.point_speclabelframe = tk.Frame(self)
        self.point_speclabelframe.config(height=40)
        self.point_speclabelframe.pack(side="top")
        self.point_speclabelframe.grid_rowconfigure(0, weight=1)
        self.point_speclabelframe.grid_columnconfigure(0, weight=1)

        self.main_label = tk.Label(self.point_speclabelframe)
        self.main_label["text"] = "Distance specific mode"
        self.main_label["font"] = "Courier 11 bold"
        self.main_label.pack(fill="both", anchor="center")

        self.point_specpath_input_frame = tk.Frame(self)
        self.point_specpath_input_frame.config(height=50)
        self.point_specpath_input_frame.pack(side="top", fill="x", anchor="center")

        ### entry-field to enter the image path
        global pic_path
        self.pic_path = tk.Entry(self.point_specpath_input_frame)
        self.pic_path["bg"] = "mint cream"
        self.pic_path["fg"] = "grey25"
        self.pic_path["bd"] = 2
        self.pic_path["cursor"] = "xterm"
        self.pic_path["width"] = 80
        self.pic_path.delete(0, "end")
        self.pic_path.insert(0, "C:/output")
        self.pic_path.pack(side="left", fill="x", expand=True, anchor="center", padx=50, pady=10)
        self.pic_path.bind("<Return>", self.upload_by_enter)

        ### in the default-status the uploaded image will be resized, because the image should be taken by powerful
        ### cameras; the box should be checked if smaller structures are considered
        self.resize_decision = True
        self.resize_checkbox = ttk.Checkbutton(self.point_specpath_input_frame, command=self.image_resize_question)
        self.resize_checkbox["text"] = "Not Resize image"
        self.resize_checkbox.pack(side="left", anchor="center")

        ### upload button, which will create the canvas with the image specified in the image path entry field
        self.uploadbutton = ttk.Button(self.point_specpath_input_frame,
                                      command=self.image_to_canvas)
        self.uploadbutton["style"] = 'button_design.TButton'
        self.uploadbutton["cursor"] = "circle"
        self.uploadbutton["text"] = "✅"
        self.uploadbutton.pack(side="right", anchor="center", padx=50, pady=10)

    def upload_by_enter(self, event):
        '''this function sorely connects the "Press Enter" function the upload function'''
        self.image_to_canvas()

    def image_resize_question(self):
        '''this function will activated through checking the box and the image will not be resized'''
        self.resize_decision = False
        return self.resize_decision

    def image_to_canvas(self):
        '''this function loads the image'''
        try:
            '''if the image exists the image will be opened, if not an IOError will be returned'''
            f = open(self.pic_path.get())
            f.close()
            self.image_path = self.pic_path.get()

            ### initialing lists, which are used by the program to store the values of the points
            self.all_points = []
            self.x_cor_points = []
            self.y_cor_points = []
            self.distance_names = []
            self.name_and_distance = []
            self.pointname = "No Pointname given"

            ### options and entry fields on the right side
            ### everything has been packed into a canvas to be able to scroll around it with growing size, due to points
            self.right_side_canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
            self.right_side_canvas.config(width=self.winfo_screenwidth()-1150, height=self.winfo_screenheight()-135)

            self.point_specimagespec_frame = tk.Frame(self.right_side_canvas, background="#ffffff")
            self.verticalbar_right = tk.Scrollbar(self, orient="vertical", command=self.right_side_canvas.yview)
            self.right_side_canvas.configure(yscrollcommand=self.verticalbar_right.set)
            self.verticalbar_right.pack(side="right", fill="y")
            self.right_side_canvas.pack(side="right", fill="x", expand=True)

            self.right_side_canvas.create_window((4, 4), window=self.point_specimagespec_frame,
                                                 anchor="n", tags="self.frame")

            ### with every pressed "Enter" the Frame will be updated and made available for the scrollbar
            self.point_specimagespec_frame.bind("<Configure>", self.onFrameConfigure)

            self.populate()

            #self.right_side_canvas.config(scrollregion=(self.right_side_canvas.winfo_x(),
            #                                            self.right_side_canvas.winfo_y(),
            #                                            self.right_side_canvas.winfo_width(),
            #                                            self.right_side_canvas.winfo_height()))
        except IOError:
            tkinter.messagebox.showinfo("Error Message", "Image couldn't be found in image path.")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.right_side_canvas.configure(scrollregion=self.right_side_canvas.bbox("all"))

    def populate(self):
        ''' this function lets the sidebar grow with newly added labels'''
        ### head-label: tells the user that this is the point specifier
        self.spec_label = tk.Label(self.point_specimagespec_frame)
        self.spec_label["text"] = "Distance specifier"
        self.spec_label["font"] = "Courier 8 bold"
        self.spec_label.pack(side="top", anchor="center", padx=5, pady=5)

        self.spec_label1 = tk.Label(self.point_specimagespec_frame)
        self.spec_label1["text"] = "1.Define distance name|\n" \
                                   "2.Hit Enter|3.Mark both points"
        self.spec_label1["font"] = "Courier 8"
        self.spec_label1.pack(side="top", anchor="center", padx=5, pady=5)

        ### entry-field to enter the names of the points
        self.point_spec = tk.Entry(self.point_specimagespec_frame)
        self.point_spec["bg"] = "mint cream"
        self.point_spec["fg"] = "grey25"
        self.point_spec["bd"] = 2
        self.point_spec["cursor"] = "xterm"
        self.point_spec["width"] = 40
        self.point_spec.pack(side="top", anchor="center", padx=5, pady=5)
        self.point_spec.bind("<Return>", self.point_name_append)

        self.print_to_frame = tk.Frame(self.point_specimagespec_frame)
        self.print_to_frame.config(width=80, height=80)
        self.print_to_frame.pack(side="top", fill="x", anchor="center")

        self.between_label = tk.Label(self.print_to_frame)
        self.between_label.config(width=40, height=1)
        self.between_label["font"] = "Courier 8 bold"
        self.between_label["text"] = " "
        self.between_label.pack(side="bottom", anchor="center", pady=1)

        ### label to for the file specifier, which names the output file
        self.file_spec_label = tk.Label(self.point_specimagespec_frame)
        self.file_spec_label["text"] = "Name the Output File"
        self.file_spec_label["font"] = "Courier 8"
        self.file_spec_label.pack(side="top", anchor="center", padx=5, pady=5)

        ### Entry where the output file name is specified
        self.save_to_file_name = tk.Entry(self.point_specimagespec_frame)
        self.save_to_file_name["bg"] = "mint cream"
        self.save_to_file_name["fg"] = "grey25"
        self.save_to_file_name["bd"] = 2
        self.save_to_file_name["cursor"] = "xterm"
        self.save_to_file_name["width"] = 40
        self.save_to_file_name.pack(side="top", anchor="center", padx=5, pady=5)
        self.save_to_file_name.bind("<Return>", self.all_done_by_enter)

        self.all_done_button = ttk.Button(self.point_specimagespec_frame,
                                         command=self.all_done_func)
        self.all_done_button["style"] = 'button_design.TButton'
        self.all_done_button["text"] = "✅ ALL DONE ✅"
        self.all_done_button["cursor"] = "circle"
        self.all_done_button.pack(side="bottom", anchor="center", padx=5, pady=5)

        ### frame for the imagecanvas and the image all_points
        self.point_specimagecanvas_frame = tk.Frame(self)
        self.point_specimagecanvas_frame.config(width=1200)
        self.point_specimagecanvas_frame.pack(side="top", fill="x", anchor="center")

        self.image_resize(self.image_path)

        ### creates the Canvas where the image and scrollbars are stored
        self.photocanvas = tk.Canvas(self.point_specimagecanvas_frame, width=1150, height=1000)
        self.photocanvas.create_image(self.imagex.width() / 2, self.imagex.height() / 2,
                                      anchor="center", image=self.imagex, tags="bg_img")
        self.photocanvas.xview_moveto(0)
        self.photocanvas.yview_moveto(0)
        self.photocanvas["cursor"] = "crosshair"
        self.photocanvas["highlightthickness"] = 5

        self.horizontalbar = tk.Scrollbar(self.point_specimagecanvas_frame, orient=tk.HORIZONTAL)
        self.horizontalbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.verticalbar = tk.Scrollbar(self.point_specimagecanvas_frame, orient=tk.VERTICAL)
        self.verticalbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontalbar.config(command=self.photocanvas.xview)
        self.verticalbar.config(command=self.photocanvas.yview)
        self.photocanvas.config(width=950, height=1000)
        self.photocanvas.config(scrollregion=(2, 2, self.imagex.width(), self.imagex.height()))
        self.photocanvas.config(xscrollcommand=self.horizontalbar.set, yscrollcommand=self.verticalbar.set)
        self.photocanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ### binds left-mouse-button to the point and the right-mouse button to the graph method
        self.photocanvas.bind("<Button-1>", self.point)


    def image_resize(self, image_path):
        ''' gets the image_path and stores it in the imagex variable '''
        if self.resize_decision == True:
            ### if the resizing_box remains empty the image will be resized according to this rules
            self.imagex = ImageTk.PhotoImage(file=image_path)

            ### this gets the dimensions of the inputted image
            self.originalwidth, self.originalheight = self.imagex.width(), self.imagex.height()

            ### resizing the image
            if self.imagex.width() > 1000:
                ### the size_factor is an individual measure, larger pictures will have a larger size_factor
                self.size_factor = floor(self.imagex.width() / 1000)

                ### and here is the size_factor applied
                image = Image.open(self.image_path)
                image = image.resize((self.imagex.width() // self.size_factor, self.imagex.height() // self.size_factor)
                                     , Image.ANTIALIAS)
                self.imagex = ImageTk.PhotoImage(image)
            else:
                self.size_factor = 1
                pass
        else:
            ### if the resizing_box is checked the image remains in the same size and and size_factor will be 1
            self.imagex = ImageTk.PhotoImage(file=image_path)
            self.originalwidth, self.originalheight = self.imagex.width(), self.imagex.height()
            self.size_factor = 1

        self.manipulatedwidth, self.manipulatedheight = self.imagex.width(), self.imagex.height()

    def point_name_append(self, event):
        '''recieves the name of the points as specified by the user, 
        appends it to the list and prints it to the window'''

        ### recieves the point name from the entry area and appends it to the point_name list
        self.pointname = self.point_spec.get()
        self.distance_names.append(self.pointname)

        self.value_label = tk.Label(self.print_to_frame)
        self.value_label.config(width=40, height=1)
        self.value_label["font"] = "Courier 8 bold"
        self.value_label["bg"] = "SeaGreen1"
        self.value_label["fg"] = "black"
        self.value_label.pack(side="top", anchor="center", pady=1)
        ### this adds the number of the point and the actual number to the point-list
        self.value_label.configure(text="(%d) %s" % (len(self.distance_names), self.pointname))

        self.point_spec.delete(0, 'end')
        return self.distance_names, self.pointname

    def point(self, event):
        '''this function creates a point(oval) around the clicked point'''
        self.x, self.y = self.photocanvas.canvasx(event.x), self.photocanvas.canvasy(event.y)
        self.x_cor, self.y_cor  = int(self.x), int(self.y)
        self.last_point = self.photocanvas.create_oval(self.x_cor - 3, self.y_cor - 3,
                                                      self.x_cor + 3, self.y_cor + 3, fill="tomato")
        ### appending the x-coordinate to lists
        self.all_points.append(self.x_cor)
        self.x_cor_points.append(self.x_cor)

        ### appending the y-coordinate to lists
        self.all_points.append(self.y_cor)
        self.y_cor_points.append(self.y_cor)

        if (len(self.x_cor_points) % 2 == 0):
            ### if they are two or multiple of 2 x-coordinates the list a  line will be created between those points
            global theline
            self.photocanvas.create_line(self.all_points[-4], self.all_points[-3], self.all_points[-2],
                                         self.all_points[-1], tags="theline", width=2, fill="tomato")
            self.coor_label = tk.Label(self.print_to_frame)
            self.coor_label.config(width=40, height=1)
            self.coor_label["font"] = "Courier 8 bold"
            self.coor_label["bg"] = "CadetBlue1"
            self.coor_label["fg"] = "black"
            self.coor_label.pack(side="top", anchor="center", pady=1)
            self.coor_label.configure(text="(%d)X1:%d|Y1:%d-->X2:%d|Y2:%d" % ((len(self.all_points) / 4),
                                                                              self.all_points[-4], self.all_points[-3],
                                                                              self.all_points[-2],self.all_points[-1]))

            try:
                ### if there are points in the all-points list, the point names will be displayed onto the screen
                self.label_on_canvas = tk.Label(self.photocanvas)
                self.label_on_canvas["font"] = "Courier 6"
                self.label_on_canvas["bg"] = "White"
                self.label_on_canvas["fg"] = "black"
                self.label_on_canvas["text"] = ""
                self.label_on_canvas.pack()
                self.label_on_canvas.configure(text="(%d) %s" % ((len(self.all_points)/4), self.pointname))

                ### if/else to arrange the coordinate value names away from the center
                ### which could possibly cover other important parts of the image
                if self.x_cor < (self.imagex.width() // 2):     # on left side
                    if self.y_cor < (self.imagex.height() // 2):    # on top
                        self.photocanvas.create_window(self.x_cor - 25, self.y_cor - 25, window=self.label_on_canvas)
                    else:   # on bottom
                        self.photocanvas.create_window(self.x_cor - 25, self.y_cor + 25, window=self.label_on_canvas)
                else:   # on right side
                    if self.y_cor < (self.imagex.height() // 2):    # on top
                        self.photocanvas.create_window(self.x_cor + 25, self.y_cor - 25, window=self.label_on_canvas)
                    else:   # on bottom
                        self.photocanvas.create_window(self.x_cor + 25, self.y_cor + 25, window=self.label_on_canvas)
            except IndexError:
                ### if no points have been named/identified an IndexError will occur
                tkinter.messagebox.showinfo("Error Message", "Marked points on Image hasn't been defined yet")
                self.label_on_canvas.configure(text="undefined point")
                self.photocanvas.create_window(self.x_cor - 25, self.y_cor - 25, window=self.label_on_canvas)
                self.photocanvas.delete(self.last_point)
                self.coor_label.destroy()
                del self.all_points[-2:]
                del self.x_cor_points[-2:]
                del self.y_cor_points[-2:]
            return self.all_points

    def all_done_by_enter(self, event):
        '''this function will be called by hitting Enter in the output file name entry area'''
        self.all_done_func()

    def all_done_func(self):
        '''Handler: is called, when the "All done" Button is pressed or the Enter Button is hit; 
        initiates calculations and print to file function'''

        ### returns the user the time the program has been used to mark and specify the points
        enter_time = time.time()
        print("Enter Time: --- %d minutes %0.3f seconds ---" %
              (((enter_time - start_time) // 60), (enter_time - start_time) % 60))
        self.num_of_calcs(len(self.distance_names))

        if self.all_points == [] or self.distance_names == []:
            ### either no point has been marked on the foto or no points has been given a name
            tkinter.messagebox.showinfo("Error Message", "No points have been marked on the image \n"
                                                         "or none of the points have been named!")
        elif (len(self.all_points)/4) != len(self.distance_names):
            ### the number of marked points and the number of named points doesn't match
            tkinter.messagebox.showinfo("Error Message",
                                        "Number of marked points and Number of Named points doesn't match!")
        else:
            ### everything is ok --> visible part of the image-canvas will be printed and saved to the output folder
            self.snapsaveCanvas()
            with open('C:/output'
                              + self.save_to_file_name.get() + '.csv', "w") as self.csv_file:
                self.file_to_write = csv.writer(self.csv_file, lineterminator = '\n')
                self.file_to_write.writerow(["--------MAIN INFORMATION ABOUT THE FILE--------"])
                self.file_to_write.writerow(["FILE NAME", self.save_to_file_name.get()])
                self.file_to_write.writerow(["PATH IMAGE", self.pic_path.get()])
                self.file_to_write.writerow(["DATE CREATED", str(datetime.now())])
                self.file_to_write.writerow(["ORIGINAL IMAGE DIMENSION", self.originalwidth, self.originalheight])
                self.file_to_write.writerow(["COMPRESSED IMAGE DIMENSION", self.manipulatedwidth,
                                             self.manipulatedheight, "Factor %s" % (self.size_factor)])

                ### calls the points and calculations function
                self.all_points_and_calculations_to_file()
                self.csv_file.close()
            calc_time = time.time()
            print("Calc Time: --- %d minutes %0.3f seconds ---" %
                  (((calc_time - enter_time) // 60), (calc_time - enter_time) % 60))

            ### terminates the program
            self.quit()

    def num_of_calcs(self, x):
        '''control function, which returns the numbers calculations the program performs'''
        number = x*2
        print('Number of points:', number)
        firstresult = 0
        secondresult = 0
        for i in range(0, number):
            firstresult += i
        print('Number of distances:', firstresult)
        for j in range(0, firstresult):
            secondresult += j
        print('Number of ratios:', secondresult)

    def all_points_and_calculations_to_file(self):
        '''this function stores all points, all calculation about the distances and ratios in the image'''
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["--------COORDINATES OF ALL POINTS--------"])
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["NAME OF THE POINT", "X1-COORDINATE", "Y1-COORDINATE",
                                     "X2-COORDINATE", "Y2-COORDINATE", "DISTANCE"])

        for i in range(len(self.distance_names)):
            ### appends in point name list: NAME, X, Y and prints those three values to the output file
            self.name_and_distance.append(self.distance_names[i])

            self.x_zero = self.x_cor_points.pop(0)
            self.y_zero = self.y_cor_points.pop(0)
            self.x_one = self.x_cor_points.pop(0)
            self.y_one = self.y_cor_points.pop(0)

            result = sqrt((self.x_zero - self.x_one) ** 2 + (self.y_zero - self.y_one) ** 2)
            self.name_and_distance.append(result)
            self.file_to_write.writerow([self.distance_names[i], self.x_zero, self.y_zero,
                                         self.x_one, self.y_one, result])

        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["--------RATIO BETWEEN EACH DISTANCES--------"])
        self.file_to_write.writerow([""])
        self.file_to_write.writerow(["1ST DIST/2ND DIST", "RATIO"])

        while self.name_and_distance != []:
            ### the ratios are again calculated similarly
            ### the first distance is poped of with its value
            distance_name_zero = self.name_and_distance.pop(0)
            num1 = self.name_and_distance.pop(0)
            number1 = float(num1)

            for i in range(0, len(self.name_and_distance), 2):
                ### distance_name_zero is then compared to all other distances
                distance_name_one = self.name_and_distance[i]
                num2 = self.name_and_distance[i + 1]
                number2 = float(num2)
                normal_result = number1 / number2
                reversed_result = number2 / number1
                self.file_to_write.writerow(["%s/%s" % (distance_name_zero, distance_name_one), "%0.4f" % (normal_result)])
                self.file_to_write.writerow(["%s/%s" % (distance_name_one, distance_name_zero), "%0.4f" % (reversed_result)])
                self.file_to_write.writerow([""])

    def snapsaveCanvas(self):
        ''' this function is called, when all inputs by the user are done and takes a screenshot of the image canvas'''
        canvas = self.canvas_info()  # Get Window Coordinates of Canvas
        self.grabcanvas = ImageGrab.grab(bbox=canvas).save('C:/output'
                                                           + self.save_to_file_name.get() + '_image_out' + '.jpg')

    def canvas_info(self):
        '''part of the snapsaveCanvas function, gets the information about the visible canvas'''
        x = self.photocanvas.winfo_rootx()+self.photocanvas.winfo_x()
        y = self.photocanvas.winfo_rooty()+self.photocanvas.winfo_y()
        x1 = x+self.photocanvas.winfo_width()
        y1 = y+self.photocanvas.winfo_height()
        box = (x, y, x1, y1)
        return box

class Angles_spec_mode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title_label = tk.Label(self)
        self.title_label["text"] = title
        self.title_label["font"] = "Courier 14 bold"
        self.title_label.grid(columnspan=4, row=0, pady=gen_pady, padx=gen_padx)

        self.main_label = tk.Label(self)
        self.main_label["text"] = "Angles specific mode"
        self.main_label["font"] = the_font
        self.main_label.grid(columnspan=4, row=1, pady=gen_pady, padx=gen_padx)

        self.startpage_button = ttk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.startpage_button["text"] = "Startpage"
        self.startpage_button.grid(column=0, row=2)

        self.point_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Point_spec_mode))
        self.point_spec_button["text"] = "Point_spec_mode_file_get"
        self.point_spec_button.grid(column=1, row=2)

        self.distance_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Distance_spec_mode))
        self.distance_spec_button["text"] = "Distance_spec_mode"
        self.distance_spec_button.grid(column=2, row=2)

        self.area_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Area_spec_mode))
        self.area_spec_button["text"] = "Area_spec_mode"
        self.area_spec_button.grid(column=3, row=2)

class Area_spec_mode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title_label = tk.Label(self)
        self.title_label["text"] = title
        self.title_label["font"] = "Courier 14 bold"
        self.title_label.grid(columnspan=4, row=0, pady=gen_pady, padx=gen_padx)

        self.main_label = tk.Label(self)
        self.main_label["text"] = "Area specific mode"
        self.main_label["font"] = the_font
        self.main_label.grid(columnspan=4, row=1, pady=gen_pady, padx=gen_padx)

        self.startpage_button = ttk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.startpage_button["text"] = "Startpage"
        self.startpage_button.grid(column=0, row=2)

        self.point_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Point_spec_mode))
        self.point_spec_button["text"] = "Point_spec_mode_file_get"
        self.point_spec_button.grid(column=1, row=2)

        self.distance_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Distance_spec_mode))
        self.distance_spec_button["text"] = "Distance_spec_mode"
        self.distance_spec_button.grid(column=2, row=2)

        self.angles_spec_button = ttk.Button(self, command=lambda: controller.show_frame(Angles_spec_mode))
        self.angles_spec_button["text"] = "Angles_spec_mode"
        self.angles_spec_button.grid(column=3, row=2)

if __name__ == "__main__":
    start_time = time.time()
    application = MorphoMath()
    application.mainloop()
    end_time = time.time()
    print("Successful program execution")
    print("Total Time: --- %d minutes %0.3f seconds ---" %
          (((end_time - start_time) // 60), (end_time - start_time) % 60))


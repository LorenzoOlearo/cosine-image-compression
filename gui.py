import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.img = None
        self.img_dct = None
        self.scaling = 0

        self.title("cosine image compression")

        self.config(background = "white")

        self.resizable(width = True, height=True)

        control_frame = tk.Frame(self)
        control_frame.grid(row = 0, column = 0)
        image_frame = tk.Frame(self)
        image_frame.grid(row = 1, column = 0, sticky="news")
        
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)

        tk.Button(control_frame, text="Select Image", command=self.selectImage).grid(row=0, column=0)
        self.dct_button = tk.Button(control_frame, text="DCT", command=self.dct, state=tk.DISABLED)
        self.dct_button.grid(row=0, column=1)

        self.F_entry = tk.Entry(control_frame)
        self.F_entry.grid(row=1, column=0)
        self.F_entry.config(validate='key', validatecommand=(self.register(self.isPositiveInteger), '%P'))
        self.F_entry.insert(0, "8")

        self.d_string = tk.StringVar()
        self.d_string.trace_add("write", self.updateDctEnable)
        self.d_entry = tk.Entry(control_frame, textvariable=self.d_string)
        self.d_entry.grid(row=1, column=1)
        self.d_entry.config(validate='key', validatecommand=(self.register(self.isDValid), '%P'))
        self.d_entry.insert(0, "0")

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)

        self.canvas_original = tk.Canvas(image_frame)
        self.canvas_original.grid(row=0, column=0, sticky="news")

        self.canvas_dct = tk.Canvas(image_frame)
        self.canvas_dct.grid(row=0, column=1, sticky="news")

        self.canvas_label = tk.Label(self)
        self.canvas_label.grid(row=3, column=0)

        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(0, weight=1)

        self.bind("<MouseWheel>", self.zoom)
        self.bind("<Button-4>", self.zoom)
        self.bind("<Button-5>", self.zoom)

        self.mainloop()

    def selectImage(self):
        path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("Image File", '.png'), ("Image File", '.bmp')])
        try:
            self.img = ImageTk.PhotoImage(Image.open(path))
            self.img_dct = None
            self.scaling = 0
            self.canvas_original.create_image(0, 0, anchor='nw', image=self.img)
            self.canvas_label.config(text=path)
            self.canvas_dct.delete("all")

            self.updateDctEnable(None, None, None)
        except (Exception):
            self.img = None
            self.img_dct = None
            self.scaling = 0
            self.canvas_label.config(text="No image selected")
            self.canvas_original.delete("all")
            self.canvas_dct.delete("all")

            self.updateDctEnable(None, None, None)
            
    def zoom(self, event):
        if event.delta == 0:
            if event.num == 4:
                self.scaling += 1
            elif event.num == 5:
                self.scaling += -1
        else:
            self.scaling += int(event.delta/120)
        
        self.canvas_original.delete("all") 
        self.canvas_dct.delete("all")

        if self.scaling > 0:
            if self.img is not None:
                self.zoomed_img = self.img._PhotoImage__photo.zoom(self.scaling)
                self.canvas_original.create_image(0, 0, anchor='nw', image=self.zoomed_img)

            if self.img_dct is not None:
                self.zoomed_img_dct = self.img_dct._PhotoImage__photo.zoom(self.scaling)
                self.canvas_dct.create_image(0, 0, anchor='nw', image=self.zoomed_img_dct)
        
        if self.scaling < 0:
            if self.img is not None:
                self.zoomed_img = self.img._PhotoImage__photo.subsample(-self.scaling)
                self.canvas_original.create_image(0, 0, anchor='nw', image=self.zoomed_img)

            if self.img_dct is not None:
                self.zoomed_img_dct = self.img_dct._PhotoImage__photo.subsample(-self.scaling)
                self.canvas_dct.create_image(0, 0, anchor='nw', image=self.zoomed_img_dct)
            
        if self.scaling == 0:
            if self.img is not None:
                self.zoomed_img = self.img
                self.canvas_original.create_image(0, 0, anchor='nw', image=self.zoomed_img)

            if self.img_dct is not None:
                self.zoomed_img_dct = self.img_dct
                self.canvas_dct.create_image(0, 0, anchor='nw', image=self.zoomed_img_dct)

    def dct(self):
        # TODO call the dct function
        self.img_dct = self.img
        self.canvas_dct.create_image(0, 0, anchor='nw', image=self.img_dct)

    def isPositiveInteger(self, value):
        try:
            if int(value)>0:
                return True
            else:
                return False
        except:
            return False

    def isDValid(self, value):
        if value == '' or value == '0':
            return True
        return self.isPositiveInteger(value)

    def checkD(self):
        d = self.d_string.get()
        try:
            if int(d) >=0 and int(d) <= 2 * int(self.F_entry.get()) - 2:
                return True
            else:
                return False
        except:
            return False


    def updateDctEnable(self, v, index, mode):
        if self.img == None:
            self.dct_button.config(state=tk.DISABLED)
        elif self.checkD():
            self.d_entry.config(fg='black')
            self.dct_button.config(state=tk.NORMAL)
        else:
            self.d_entry.config(fg='red')
            self.dct_button.config(state=tk.DISABLED)
            

GUI()

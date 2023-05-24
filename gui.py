import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.img = None

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

        self.mainloop()

    def selectImage(self):
        path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("Image File", '.png'), ("Image File", '.bmp')])
        try:
            self.img = ImageTk.PhotoImage(Image.open(path))
            self.canvas_original.create_image(0, 0, anchor='nw', image=self.img)
            self.canvas_label.config(text=path)
            self.canvas_dct.delete("all")

            self.updateDctEnable(None, None, None)
        except (Exception):
            self.img = None
            self.canvas_label.config(text="No image selected")
            self.canvas_original.delete("all")
            self.canvas_dct.delete("all")

            self.updateDctEnable(None, None, None)
            
    

    def dct(self):
        # TODO call the dct function
        self.canvas_dct.create_image(0, 0, anchor='nw', image=self.img)

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

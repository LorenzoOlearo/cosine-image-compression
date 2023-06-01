import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class GUI(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

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

        self.F_string = tk.IntVar()
        self.F_string.trace_add("write", self.updateDEntryLimits)
        self.F_entry = tk.Entry(control_frame, textvariable=self.F_string)
        self.F_entry.config(state=tk.DISABLED, validate='key', validatecommand=(self.register(self.isFValid), '%P'))
        self.F_entry.grid(row=1, column=0)

        self.d_string = tk.IntVar()
        self.d_entry = tk.Scale(control_frame, orient=tk.HORIZONTAL, from_=0, to=0, variable=self.d_string)
        self.d_entry.grid(row=1, column=1)

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


        self.canvas_original.bind("<MouseWheel>", self.zoom)
        self.canvas_original.bind("<Button-4>", self.zoom)
        self.canvas_original.bind("<Button-5>", self.zoom)
        self.canvas_original.bind("<ButtonPress-1>", self.start_pan)
        self.canvas_original.bind("<B1-Motion>", self.pan)
        self.canvas_dct.bind("<MouseWheel>", self.zoom)
        self.canvas_dct.bind("<Button-4>", self.zoom)
        self.canvas_dct.bind("<Button-5>", self.zoom)
        self.canvas_dct.bind("<ButtonPress-1>", self.start_pan)
        self.canvas_dct.bind("<B1-Motion>", self.pan)
        self.bind("<Configure>", self.on_resize)

        self.box = (0, 0, self.canvas_original.winfo_width(), self.canvas_original.winfo_height())

    def start_pan(self, event):
        self.pan_x = event.x
        self.pan_y = event.y

    def pan(self, event):
        scale = 2 ** self.scaling
        x = (self.pan_x - event.x)/scale
        y = (self.pan_y - event.y)/scale

        box = (
            self.box[0] + x,
            self.box[1] + y,
            self.box[2] + x,
            self.box[3] + y
        )

        right_limit = max(self.img.width(), self.canvas_original.winfo_width()/scale)
        bottom_limit = max(self.img.height(), self.canvas_original.winfo_height()/scale)

        if box[0]<0:
            box = (0,
                   box[1],
                   box[2] - box[0],
                   box[3])

        if box[1]<0:
            box = (box[0],
                   0,
                   box[2],
                   box[3] - box[1])
            
        if box[2]>right_limit:
            box = (box[0] - (box[2] - right_limit),
                   box[1],
                   right_limit,
                   box[3])

        if box[3]>bottom_limit:
            box = (box[0],
                   box[1] - (box[3] - bottom_limit),
                   box[2],
                   bottom_limit)


        self.box = box
        self.pan_x = event.x
        self.pan_y = event.y

        self.redraw()

    def on_resize(self, event):
        self.box = (
            self.box[0],
            self.box[1],
            self.box[0] + self.canvas_original.winfo_width(),
            self.box[1] + self.canvas_original.winfo_height()
        )

    def selectImage(self):
        path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), ("Image File", '.png'), ("Image File", '.bmp')])
        try:
            self.img = ImageTk.PhotoImage(Image.open(path).convert('L'))
            self.img_dct = None
            self.scaling = 0
            self.canvas_label.config(text=path)
            self.F_entry.config(state=tk.NORMAL)
            self.dct_button.config(state=tk.NORMAL)
            self.box = (0, 0, self.canvas_original.winfo_width(), self.canvas_original.winfo_height())

        except (Exception):
            self.img = None
            self.img_dct = None
            self.scaling = 0
            self.canvas_label.config(text="No image selected")
            self.F_entry.config(state=tk.DISABLED)
            self.dct_button.config(state=tk.DISABLED)
            self.box = (0, 0, self.canvas_original.winfo_width(), self.canvas_original.winfo_height())

        
        self.redraw()

    def start(self):

        self.mainloop()

    def zoom(self, event):

        scaling = self.scaling

        box = self.box

        x = box[0] + (box[2] - box[0])/2
        y = box[1] + (box[3] - box[1])/2

        if event.delta == 0:
            if event.num == 4:
                
                scaling += 1

                x = box[0] + event.x / (2 ** self.scaling)
                y = box[1] + event.y / (2 ** self.scaling)
                

            elif event.num == 5:
                scaling += -1
        else:
            scaling += int(event.delta/120)
            x = box[0] + event.x / (2 ** self.scaling)
            y = box[1] + event.y / (2 ** self.scaling)

        scale = 2 ** (scaling-self.scaling)
        box =  (box[0] - x,
                box[1] - y,
                box[2] - x,
                box[3] - y)
        box =  (box[0] / scale,
                box[1] / scale,
                box[2] / scale,
                box[3] / scale)
        box =  (box[0] + x,
                box[1] + y,
                box[2] + x,
                box[3] + y)
        
        right_limit = max(self.img.width(), self.canvas_original.winfo_width()/scale)
        bottom_limit = max(self.img.height(), self.canvas_original.winfo_height()/scale)

        if box[0]<0:
            box = (0,
                   box[1],
                   box[2] - box[0],
                   box[3])

        if box[1]<0:
            box = (box[0],
                   0,
                   box[2],
                   box[3] - box[1])
            
        if box[2]>right_limit:
            box = (box[0] - (box[2] - right_limit),
                   box[1],
                   right_limit,
                   box[3])


        if box[3]>bottom_limit:
            box = (box[0],
                   box[1] - (box[3] - bottom_limit),
                   box[2],
                   bottom_limit)
        
        self.box = box
        self.scaling = scaling

        self.redraw()


    def redraw(self):

        self.canvas_original.delete("all") 
        self.canvas_dct.delete("all")
        maxsize = (self.canvas_original.winfo_width(), self.canvas_original.winfo_height())

        scale = 2**self.scaling

        if self.img is not None:
            img = ImageTk.getimage(self.img).copy()

            img = img.crop((self.box[0], self.box[1], min(img.width, self.box[2]), min(img.height, self.box[3])))
            img = img.resize((round(img.width*scale), round(img.height*scale)), Image.NEAREST)

            self.zoomed_img = ImageTk.PhotoImage(img)
            self.canvas_original.create_image(0, 0, anchor='nw', image=self.zoomed_img)
        

        if self.img_dct is not None:
            img = ImageTk.getimage(self.img_dct)
            if(img.width*scale > maxsize[0] or img.height*scale > maxsize[1]):
                img = img.crop(self.box)
            img = img.resize((round(img.width*scale), round(img.height*scale)), Image.NEAREST)
            
            
            self.zoomed_img_dct = ImageTk.PhotoImage(img)
            self.canvas_dct.create_image(0, 0, anchor='nw', image=self.zoomed_img_dct)

    def dct(self):
        # TODO call the dct function
        try:
            self.img_dct = self.controller.dct(self.img, self.F_string.get(), self.d_string.get())
            self.redraw()
        except Exception as e:
            messagebox.showerror("Error", "Invalid input")

    def isPositiveInteger(self, value):
        try:
            if int(value)>0:
                return True
            else:
                return False
        except:
            return False

    def isFValid(self, value):
        if value == '':
            return True
        try:
            F = int(value)
            if F > 0 and F <= min(self.img.width(), self.img.height()):
                return True
            else:
                return False
        except:
            return False
    
    def updateDEntryLimits(self, v, index, mode):
        if self.img == None:
            self.d_entry.config(from_=0, to=0, state=tk.DISABLED)
        else:
            try:
                self.d_entry.config(from_=0, to=2 * self.F_string.get() - 2, state=tk.NORMAL)
            except:
                self.d_entry.config(from_=0, to=2 * 1 - 2, state=tk.NORMAL)

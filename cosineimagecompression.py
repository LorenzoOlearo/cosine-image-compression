from gui import GUI

class CosineImageCompression():

    def __init__(self) -> None:
        self.gui = GUI(self)
        self.gui.start()

    def dct(self, image, F, d):
        return image
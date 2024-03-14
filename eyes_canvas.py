from abc import ABC, abstractmethod
import sys

class EyesCanvas(ABC):

    @abstractmethod
    def draw(self):
        pass

if sys.platform == "darwin":
    import tkinter as tk

    class MacOsEyesCanvas(EyesCanvas):
        def draw(self):
            pass
else:
    class SpiEyesCanvas(EyesCanvas):
        def draw(self):
            pass

class DumbEyesCanvas(EyesCanvas):
    def draw(self):
        pass

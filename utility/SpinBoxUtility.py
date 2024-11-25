#   Class created by: Tom Schimansky at: https://github.com/TomSchimansky/CustomTkinter/wiki/Create-new-widgets-(Spinbox)
#   Modified by Arnaud Kersual
import customtkinter
from typing import Union, Callable

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 frame,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.frame = frame
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand

        self.subtract_button = customtkinter.CTkButton(frame, text="-", font=("Roboto", 18, "bold"), width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(200, 0), pady=3)

        self.entry = customtkinter.CTkEntry(frame, width=width-(height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=0, columnspan=1, padx=(315, 40), pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(frame, text="+", font=("Roboto", 18, "bold"), width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=0, padx=(350, 0), pady=3)


    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            if not int(self.entry.get()) <= 0:
                value = int(self.entry.get()) - self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
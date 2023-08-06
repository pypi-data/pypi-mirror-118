import tkinter as tk
from tkinter import ttk
import math


# An API made by me to make making screens, etc. easier
# Mainly used for easier creation of buttons and entry boxes
class Screen:
    screen = None
    canvas = None
    texts = {}
    buttons = {}
    entry_boxes = {}
    __selected_box = None
    __current_char = " "

    def __init__(self, title="Screen", width=100, height=100):
        self.screen = tk.Tk()
        self.screen.title(title)
        self.screen.geometry("{}x{}".format(str(width), str(height)))
        self.canvas = tk.Canvas(self.screen, width=width, height=height)
        self.canvas.pack()

    def __show_cursor(self):
        self.screen.after(500, self.__hide_cursor)
        if not self.__selected_box is None:
            box = self.entry_boxes[self.__selected_box]
            self.canvas.itemconfigure(box["text_id"], text=box["text"] + "|")
            self.__current_char = "|"

    def __hide_cursor(self):
        self.screen.after(500, self.__show_cursor)
        if not self.__selected_box is None:
            box = self.entry_boxes[self.__selected_box]
            self.canvas.itemconfigure(box["text_id"], text=box["text"] + " ")
            self.__current_char = " "

    def run(self):
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<1>", self.on_click)
        self.canvas.bind_all("<KeyPress>", self.on_key)
        self.screen.after(3000, self.__show_cursor)
        self.screen.mainloop()

    def destroy(self):
        self.screen.destroy()

    def get_root(self):
        return self.screen

    def background_color(self, color=None):
        if color is None:
            return self.get_value("bg")
        self.configure_canvas("bg", color)

    def border_color(self, color=None):
        if color is None:
            return self.get_value("bg")
        self.configure_screen("bg", color)

    def configure_screen(self, key, value):
        self.screen[key] = value

    def configure_canvas(self, key, value):
        self.canvas[key] = value

    def get_value(self, key):
        return self.screen[key]

    def rectangle(self, x1, y1, x2, y2, fill="gray", outline="black"):
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)

    def text(self, x, y, name="", text="", fill="black", font="Arial 15", anchor="NW", justify="left", wrap=None):
        if wrap is None:
            id = self.canvas.create_text(x, y, text=text, fill=fill, font=font, justify=justify, anchor=anchor.lower())
        else:
            id = self.canvas.create_text(x, y, text=text, fill=fill, font=font, justify=justify, anchor=anchor.lower(), width=wrap)
        if not name == "":
            self.texts[name] = {
                "x": x,
                "y": y,
                "text": text,
                "id": id
            }
        return id

    def create_button(self, name, x1, y1, x2, y2, text="", event=None, default="green", hover="lime"):
        self.buttons[name] = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "text": text,
            "default_color": default,
            "hover_color": hover,
            "rectangle_id": self.rectangle(x1, y1, x2, y2, fill=default, outline=default),
            "text_id": self.text(math.floor((x2 + x1) / 2), math.floor((y2 + y1) / 2), text=text, fill=hover,
                                 anchor="C"),
            "event": event
        }

    def change_button_color(self, name, default="green", hover="lime"):
        self.buttons[name]["default_color"] = default
        self.buttons[name]["hover_color"] = hover

    def create_entry_box(self, name, x1, y1, x2, y2, defaulttext="", onupdate=None, background="white", outline="black",
                         textcolor="black"):
        self.entry_boxes[name] = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "text": defaulttext,
            "rectangle_id": self.rectangle(x1, y1, x2, y2, fill=background, outline=outline),
            "text_id": self.text(math.floor((x2 + x1) / 2), math.floor((y2 + y1) / 2), text=defaulttext, fill=textcolor,
                                 anchor="C"),
            "on_update": onupdate
        }

    def in_bounds(self, x, y, x1, y1, x2, y2):
        if ((x >= x1) and (x <= x2)) and ((y >= y1) and (y <= y2)):
            return True
        return False

    def on_move(self, event):
        x = event.x
        y = event.y
        for key in self.buttons:
            button = self.buttons[key]
            if self.in_bounds(x, y, button["x1"], button["y1"], button["x2"], button["y2"]):
                self.canvas.itemconfigure(button["rectangle_id"], fill=button["hover_color"])
                self.canvas.itemconfigure(button["text_id"], fill=button["default_color"])
            else:
                self.canvas.itemconfigure(button["rectangle_id"], fill=button["default_color"])
                self.canvas.itemconfigure(button["text_id"], fill=button["hover_color"])

    def on_click(self, event):
        x = event.x
        y = event.y
        toCall = []
        for key in self.entry_boxes:
            box = self.entry_boxes[key]
            if self.in_bounds(x, y, box["x1"], box["y1"], box["x2"], box["y2"]):
                if not self.__selected_box is None:
                    nBox = self.entry_boxes[self.__selected_box]
                    self.canvas.itemconfigure(nBox["text_id"], text=nBox["text"])
                self.__selected_box = key
            elif self.__selected_box == key:
                self.__selected_box = None
                self.canvas.itemconfigure(box["text_id"], text=box["text"])
        for key in self.buttons:
            button = self.buttons[key]
            if self.in_bounds(x, y, button["x1"], button["y1"], button["x2"], button["y2"]):
                if button["event"] is not None:
                    toCall.append(button["event"])
        for call in toCall:
            call()

    def on_key(self, event):
        if self.__selected_box is None:
            return
        char = event.char
        box = self.entry_boxes[self.__selected_box]
        if char == "\b":
            box["text"] = box["text"][:len(box["text"]) - 1]
        elif char == "":
            try:
                newTextList = box["text"].split()
                box["text"] = self.__replace_last(box["text"], newTextList[len(newTextList) - 1], "")
                box["text"] = box["text"][:-1]
            except IndexError:
                pass
        else:
            box["text"] = box["text"] + char
        self.canvas.itemconfigure(box["text_id"], text=box["text"] + self.__current_char)

        if not box["on_update"] is None:
            result = box["on_update"](box["text"])
            if not result is None:
                if type(result) == str:
                    box["text"] = result
                    self.canvas.itemconfigure(box["text_id"], text=result + self.__current_char)
                else:
                    raise SyntaxError("Provided result must be of type String")

    def get_entry_box_text(self, name):
        return self.entry_boxes[name]["text"]

    def set_entry_box_text(self, name, text):
        self.entry_boxes[name]["text"] = text
        self.canvas.itemconfigure(self.entry_boxes[name]["text_id"], text=text)

    def get_text_text(self, name):
        return self.texts[name]["text"]

    def get_text_id(self, name):
        return self.texts[name]["id"]

    def set_text_text(self, name, text):
        self.texts[name]["text"] = text
        self.canvas.itemconfigure(self.texts[name]["id"], text=text)

    def reset(self):
        self.canvas.delete("all")
        self.texts = {}
        self.buttons = {}
        self.entry_boxes = {}
        if not self.__selected_box is None:
            nBox = self.entry_boxes[self.__selected_box]
            self.canvas.itemconfigure(nBox["text_id"], text=nBox["text"])
        self.__selected_box = None

    def __replace_last(self, string, find, replace):
        reversed = string[::-1]
        replaced = reversed.replace(find[::-1], replace[::-1], 1)
        return replaced[::-1]

if __name__ == "__main__":
    import re

    def __typed(newText):
        return "".join(re.findall("[0-9]", newText))

    print("""
Welcome to ScreenAPI
    Version: Beta 1.0
    
©2021
    """)
    screen = Screen("ScreenAPI Example", 600, 600)
    screen.background_color("aqua")
    screen.border_color("blue")

    screen.text(300, 50, "Screen API", font="Arial 32 bold", anchor="C")
    screen.create_button("print_info", 200, 100, 400, 175, "INFO", lambda: print("""
Welcome to ScreenAPI
    Version: Beta 1.0

©2021
    """))

    screen.create_button("number", 200, 200, 400, 275, "LETTER", lambda: screen.set_entry_box_text("number_only", re.sub(
        re.compile("[aA-zZ]"), "", screen.get_entry_box_text("number_only"))))
    screen.create_entry_box("number_only", 100, 300, 500, 350, "Click above or type")
    screen.create_entry_box("force_number_only", 100, 375, 500, 425, "Try to type letters", onupdate=__typed)

    screen.run()

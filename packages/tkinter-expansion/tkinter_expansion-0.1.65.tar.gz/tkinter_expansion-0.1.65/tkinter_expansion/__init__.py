import tkinter as tk
from os import mkdir
import json
from . import GuiStyle
from .Identifiers import UnknownIdentifier

tmp_top_label = None
tmp_top = None


class DesignerThemeNotFound(Exception):
    pass


class Designer:
    def __init__(self, *args, **kwargs) -> None:
        """

        :param args: Any
        :param kwargs: available kwargs:
            master, width, height, title, show, share_locals, share_globals
        """
        self.identifiers2 = {"color": "background",
                        "bordercolor": "highlightbackground",
                        "bordercolorwidth": "highlightthickness",
                        "activecolor": "activebackground",
                        "textcolor": "foreground",
                        "activetextcolor": "activeforeground",
                        "disabledtextcolor": "disabledforeground",
                        "activebordercolor": "highlightcolor"}
        self.identifiers = [i for i in self.identifiers2]
        for a in self.identifiers2.values():
            self.identifiers.append(a)
        self.selected = ""
        self.changed_widgets = {}
        self.rgb_value = None
        self.var_data = None
        self.name = "default"
        self.var_name_data = None
        self.Thread1 = None
        self.kwargs = kwargs
        self.args = args
        self._color_data = ["activebackground",
                            "activeforeground",
                            "background",
                            "disabledforeground",
                            "foreground",
                            "highlightbackground",
                            "highlightcolor"]

        self._all_available_kwargs = ["master", "width", "height", "title", "show", "share_locals", "share_globals"]
        self._kwargs_fix = {"master": lambda: tk.Tk(),
                            "width": 400,
                            "height": 500,
                            "title": "Tkinter expansion designer",
                            "show": True,
                            "share_locals": None,
                            "share_globals": None}

        for i in self._all_available_kwargs:
            try:
                self.kwargs[i]
            except KeyError:
                self.kwargs[i] = self._kwargs_fix[i]
        self.share_locals = self.kwargs["share_locals"]
        self.share_globals = self.kwargs["share_globals"]
        self.window = tk.Toplevel(self.kwargs["master"])
        self.window.resizable(False, False)
        self.window.title(self.kwargs["title"])
        self.window.configure(width=self.kwargs["width"], height=self.kwargs["height"])

        self.ColorChoicePanel = tk.Label(self.window, background="white")
        self.ColorChoicePanel.place(x=0, y=0, relheight=0.25, width=self.kwargs["width"])
        self.ColorRedText = tk.Label(self.ColorChoicePanel, text="Red", background="white")
        self.ColorRedText.place(anchor="ne", x=275, y=25)
        self.ColorRedInput = tk.Entry(self.ColorChoicePanel, background="white")
        self.ColorRedInput.place(x=275, y=20, height=20, width=120)
        self.ColorGreenText = tk.Label(self.ColorChoicePanel, text="Green", background="white")
        self.ColorGreenText.place(anchor="ne", x=275, y=60)
        self.ColorGreenInput = tk.Entry(self.ColorChoicePanel, background="white")
        self.ColorGreenInput.place(x=275, y=55, height=20, width=120)
        self.ColorBlueText = tk.Label(self.ColorChoicePanel, text="Blue", background="white")
        self.ColorBlueText.place(anchor="ne", x=275, y=95)
        self.ColorBlueInput = tk.Entry(self.ColorChoicePanel, background="white")
        self.ColorBlueInput.place(x=275, y=90, height=20, width=120)
        self.Color = tk.Label(self.ColorChoicePanel, background="black")
        self.Color.place(x=12.5, y=12.5, height=100, width=100)

        self.ColorRedInput.insert(0, "0")
        self.ColorGreenInput.insert(0, "0")
        self.ColorBlueInput.insert(0, "0")

        self.ColorRedInput.bind("<KeyRelease>", lambda _: self.Color.configure(
            background=self._get_rgb(self.ColorRedInput,
                                     self.ColorGreenInput,
                                     self.ColorBlueInput)))
        self.ColorGreenInput.bind("<KeyRelease>", lambda _: self.Color.configure(
            background=self._get_rgb(self.ColorRedInput,
                                     self.ColorGreenInput,
                                     self.ColorBlueInput)))
        self.ColorBlueInput.bind("<KeyRelease>", lambda _: self.Color.configure(
            background=self._get_rgb(self.ColorRedInput,
                                     self.ColorGreenInput,
                                     self.ColorBlueInput)))

        self.Name = tk.Label(self.window, text="Name: ")
        self.Name.place(x=15, rely=0.26)

        self.ApplyButton = tk.Button(self.window, text="Apply")
        self.ApplyButton.place(x=265, y=455)

        self.SaveButton = tk.Button(self.window, text="Save")
        self.SaveButton.place(x=325, y=455)

        if self.kwargs["show"]:
            pass
        else:
            self.window.destroy()

        self.show = kwargs["show"]

    def set_rgb(self, what_to_change: tk.Event):
        what_to_change.widget.configure(background=self._get_rgb(self.ColorRedInput,
                                                                 self.ColorGreenInput,
                                                                 self.ColorBlueInput))

    def _get_rgb(self, *args: tk.Entry):
        final_values = []
        for i in args:
            self._term_i = i.get()
            try:
                final_values.append(int(self._term_i))
            except ValueError:
                final_values.append(0)
        return rgb_to_hex(final_values[0], final_values[1], final_values[2])

    def select_widget(self, part: tk.Event):
        if self.un_select():
            return
        yy = 0.29
        for i in self._color_data:
            self.tmp_Button = tk.Button(self.window, text=f"Change {i}", command=lambda y=i:
            self._color_parts(part, y))
            self.tmp_Button.place(x=14, rely=yy)
            yy += 0.06
        self.Name.configure(text=f"Name: {id(part.widget)}")
        self.var_data = _get_var_by_id(id(part.widget), self.share_globals)
        self.var_name_data = _get_var_by_name(self.var_data[0], self.share_locals)[0]
        try:
            if list(self.changed_widgets.items())[0].count(self.var_name_data) > 0:
                pass
            else:
                self.changed_widgets[self.var_name_data] = {}
        except IndexError:
            self.changed_widgets[self.var_name_data] = {}

    def _color_parts(self, part: tk.Event, value: str):
        self.selected = value
        try:
            self.rgb_value = hex_to_rgb(part.widget.cget(value).replace("#", ""))
        except tk.TclError:
            return
        self.ColorRedInput.delete(0, tk.END)
        self.ColorRedInput.insert(0, self.rgb_value[0])
        self.ColorGreenInput.delete(0, tk.END)
        self.ColorGreenInput.insert(0, self.rgb_value[1])
        self.ColorBlueInput.delete(0, tk.END)
        self.ColorBlueInput.insert(0, self.rgb_value[2])
        self.Color.configure(background=part.widget.cget(value))
        self.ApplyButton.configure(command=lambda: self._apply_values(part))
        self.SaveButton.configure(command=lambda: self.save(self.name))

    def _apply_values(self, part: tk.Event):
        self.apply_text = f"'{self._get_rgb(self.ColorRedInput, self.ColorGreenInput, self.ColorBlueInput)}'"
        exec("part.widget.configure(" + f"{self.selected}=" + self.apply_text + ")")
        self.changed_widgets[self.var_name_data][self.selected] = str(part.widget.cget(self.selected))
        print(self.changed_widgets)

    def un_select(self):
        try:
            self.Color.configure(background="black")
        except tk.TclError:
            return True
        self.Name.configure(text=f"Name: ")
        self.ColorRedInput.delete(0, tk.END)
        self.ColorRedInput.insert(0, "0")
        self.ColorGreenInput.delete(0, tk.END)
        self.ColorGreenInput.insert(0, "0")
        self.ColorBlueInput.delete(0, tk.END)
        self.ColorBlueInput.insert(0, "0")
        self.ApplyButton.configure(command=None)

    def save(self, name="default"):
        try:
            mkdir("themes")
        except FileExistsError:
            pass
        with open(f"themes/{name}.json", "w") as file:
            json.dump(self.changed_widgets, file)

    def load(self):
        give = False
        try:
            with open(f"themes/{self.name}.json") as file:
                data = json.load(file)
            for i in data:
                for ii in data[i]:
                    if ii not in self.identifiers:
                        raise UnknownIdentifier(f"Identifier \"{ii}\" was not found! To get all"
                                                          f" identifiers"
                                                          f" use print(tkinter_expansion.identifiers())")
            for x, y in data.items():
                self.changed_widgets[x] = {}
                for a, b in y.items():
                    self.changed_widgets[x][a] = str(b)
            return data
        except FileNotFoundError:
            give = True
        if give:
            raise DesignerThemeNotFound(f"Theme with name {self.name} was not found in themes folder!")

    def set_theme_name(self, name="default"):
        self.name = name


def rgb_to_hex(red: int, green: int, blue: int) -> str:
    """
    :param red: Red color value
    :param green: Green color value
    :param blue: Blue color value
    :return: converts red, green, blue into hex color format for tkinter
    """
    if red > 255:
        red = 255
    if green > 255:
        green = 255
    if blue > 255:
        blue = 255
    if red < 0:
        red = 0
    if green < 0:
        green = 0
    if blue < 0:
        blue = 0
    return '#%02x%02x%02x' % (red, green, blue)


def hex_to_rgb(hex_color: str) -> tuple:
    """

    :param hex_color: hex color value
    :return: rgb value from hex color
    """
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _get_var_by_id(id_of_var, global_share):
    return [x for x in list(global_share.values()) if id(x) == id_of_var]


def _get_var_by_name(var_data, shared_locals):
    return [x for x, y in shared_locals.items() if y == var_data]


def bind_help(panel, text):
    panel.bind("<Enter>", lambda _: panel.after(500, _show_hint(panel, text=text)))


def unbind_help(panel):
    panel.bind("<Leave>", lambda _: _hide_hint())


def _show_hint(panel, text: str):
    global tmp_top, tmp_top_label
    x = y = 0
    x += panel.winfo_rootx() + 25
    y += panel.winfo_rooty() + 20
    tmp_top = tk.Toplevel(panel)
    tmp_top.wm_overrideredirect(True)
    tmp_top.wm_geometry("+%d+%d" % (x, y))
    tmp_top_label = tk.Label(tmp_top, text=text, justify='left', background="#ffffff", relief='solid', borderwidth=1)
    tmp_top_label.pack(ipadx=1)


def identifiers():
    identifiers2 = {"color": "background",
                    "bordercolor": "highlightbackground",
                    "bordercolorwidth": "highlightthickness",
                    "activecolor": "activebackground",
                    "textcolor": "foreground",
                    "activetextcolor": "activeforeground",
                    "disabledtextcolor": "disabledforeground",
                    "activebordercolor": "highlightcolor"}
    identifiers = [i for i in identifiers2]
    for a in identifiers2.values():
        identifiers.append(a)
    return f"All supported identifiers: {', '.join(identifiers)}."


def _hide_hint():
    global tmp_top_label, tmp_top
    tmp_top_label.destroy()
    tmp_top.destroy()

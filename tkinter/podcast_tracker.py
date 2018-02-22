"""
A pet project I've been doing
"""

import tkinter  # interface
import tkinter.ttk
import tkinter.messagebox
import yaml  # database editing


class RootWindow:
    """Window Class."""

    def __init__(self, window):
        self.window = window
        self.widgets = {}

        # Window Methods:
        # This removes dashed line from the right-click menu.
        window.option_add("*tearOff", False)
        window.title("Podcast Tracker")

        # This allows child widgets to stretch.
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # Creates two main frames.

        for (frame, row) in (
                ("top_frame", 0,),
                ("bottom_frame", 1,),
        ):
            self.widgets[frame] = tkinter.ttk.Frame(window)
            self.widgets[frame].grid(row=row, sticky="nsew")

        # Creates main buttons.
        for (button, text, command, column) in (
                ("save_button", "Save", self.save_data, 0),
                ("add_button", "Add", lambda: self.new_window("Add"), 1)
        ):
            self.widgets[button] = tkinter.ttk.Button(
                self.widgets["top_frame"],
                text=text, command=command
            )
            self.widgets[button].grid(row=0, column=column, sticky="e")

        # Create the data treeview.
        self.tree = tkinter.ttk.Treeview(
            self.widgets["bottom_frame"], columns=(
                "Title",
                "Listened",
                "Theme",
                "Podcast",
            )
        )
        self.tree.bind("<Button-1>", self.left_mouse_button)
        self.tree.grid(row=0, column=0, sticky="nswe")

        # Tree headings and column width
        for (number, text, width) in (
                ("#0", "Date", 55),
                ("#1", "Listened", 55),
                ("#2", "Title", 300),
                ("#3", "Theme", 300),
                ("#4", "Podcast", 300),
        ):
            self.tree.heading(number, text=text)
            self.tree.column(number, width=width)

        # The scrollbar.
        self.scrollbar = tkinter.ttk.Scrollbar(
            self.widgets["bottom_frame"],
            orient="vertical",
            command=self.tree.yview,
        )
        self.scrollbar.grid(row=0, column=1, sticky="nse")

        # This feedbacks data to the scrollbar.
        self.tree["yscrollcommand"] = self.scrollbar.set

        # Right-click Menu
        self.menu = tkinter.Menu(window)

        # Menu options
        for (label, command) in (
                ("Delete", self.delete_entry),
                ("Edit", lambda: self.new_window("Edit")),
        ):
            self.menu.add_command(label=label, command=command)

        # Binding the Menu to the RMB
        window.bind("<3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.show_data()

    def apply_changes(self):
        """Writes the edited data into memory and reloads the page."""
        self.tree.item(
            self.tree.selection(),
            text=self.widgets["date_entry"].get()
        )
        self.tree.item(
            self.tree.selection(),
            values=(
                self.widgets["listened_entry"].get(),
                self.widgets["title_entry"].get(),
                self.widgets["theme_entry"].get(),
                self.widgets["podcast_entry"].get(),
            )
        )
        self.save_data()
        self.widgets["edit_window"].destroy()

    def clear_data(self):
        """Clears the table"""
        self.tree.delete(*self.tree.get_children())

    def delete_entry(self):
        """Deletes the selected item"""
        self.tree.delete(self.tree.selection())
        self.save_data()

    def left_mouse_button(self, event):
        """Binds stuff to lmb"""
        if (self.tree.identify("region", event.x,
                               event.y) == "heading"):
            if self.tree.identify("column", event.x, event.y) == "#0":
                self.sort_entries()

    def new_window(self, button):
        """Shows a new window to edit\add the entry."""

        # Creating Editing window
        self.widgets["edit_window"] = tkinter.Toplevel()
        self.widgets["edit_window"].geometry(
            "+{}+{}".format(
                self.tree.winfo_pointerx(),
                self.tree.winfo_pointery(),
            )
        )

        # Creates frames in the window
        for (frame, row) in (
                ("entries_frame", 0),
                ("buttons_frame", 1),
        ):
            self.widgets[frame] = tkinter.ttk.Frame(
                self.widgets["edit_window"]
            )
            self.widgets[frame].grid(row=row, column=0)

        # Entries Frame
        for (text, widget, row) in (
                ("Date", "date_entry", 0),
                ("Listened", "listened_entry", 1),
                ("Title", "title_entry", 2),
                ("Theme", "theme_entry", 3),
                ("Podcast", "podcast_entry", 4),
        ):
            label = tkinter.ttk.Label(self.widgets["edit_window"], text=text)
            label.grid(row=row, column=0)
            self.widgets[widget] = tkinter.ttk.Entry(
                self.widgets["edit_window"],
                width=60
            )
            self.widgets[widget].grid(row=row, column=1)

        # Buttons
        if button == "Add":
            text = "Add"
            command = self.write_data
        else:
            text = "Edit"
            command = self.apply_changes
        for (name, label, command, column) in (
                (
                    "CloseButton",
                    "Close",
                    self.widgets["edit_window"].destroy,
                    0,
                ),
                ("OtherButton", text, command, 1)
        ):
            name = tkinter.ttk.Button(
                self.widgets["edit_window"],
                text=label,
                command=command
            )
            name.grid(row=5, column=column)

        # Fetching the data from the tree
        if button != "Add":
            item_string = self.tree.item(self.tree.selection())
            item_text = {
                "date_entry": item_string["text"],
                "listened_entry": item_string["values"][0],
                "title_entry": item_string["values"][1],
                "theme_entry": item_string["values"][2],
                "podcast_entry": item_string["values"][3],
            }
            for key, value in item_text.items():
                self.widgets[key].insert(0, value)

            self.widgets["edit_window"].focus_set()

    def save_data(self):
        """Saves the data into the file."""
        # Creating a list which we are gonna save to file.
        newdata = []
        for item in self.tree.get_children():
            entry = {
                "Date": self.tree.item(item)["text"],
                "Listened": self.tree.item(item)["values"][0],
                "Title": self.tree.item(item)["values"][1],
                "Theme": self.tree.item(item)["values"][2],
                "Podcast": self.tree.item(item)["values"][3],
            }
            newdata.append(entry)

        # Dumping the data into the file.
        with open("data.txt", "w", encoding="UTF-8") as outputfile:
            outputfile.write(
                yaml.dump_all(
                    newdata,
                    allow_unicode=True,
                    default_flow_style=False
                )
            )

    def show_data(self):
        """Loads the data into the window."""
        data = list(
            yaml.load_all(
                open(
                    "data.txt",
                    "r",
                    encoding="UTF-8"
                )
            )
        )
        for item in data:
            self.tree.insert(
                "",
                "end",
                text=item["Date"],
                values=(
                    item["Listened"],
                    item["Title"],
                    item["Theme"],
                    item["Podcast"],
                )
            )

    def sort_entries(self):
        """Sorts Entries"""

        templist = []
        for item in self.tree.get_children():
            templist.append(self.tree.item(item))
        self.clear_data()
        for item in sorted(
                templist,
                key=lambda key: int(key["text"])
        ):
            self.tree.insert(
                "",
                "end",
                text=item["text"],
                values=(
                    item["values"][0],
                    item["values"][1],
                    item["values"][2],
                    item["values"][3],
                )
            )

    def write_data(self, ):
        """Adds data to the tree, sorts and saves."""

        new_entry = {
            "Date": self.widgets["date_entry"].get(),
            "Listened": self.widgets["listened_entry"].get(),
            "Title": self.widgets["title_entry"].get(),
            "Podcast": self.widgets["podcast_entry"].get(),
            "Theme": self.widgets["theme_entry"].get()
        }

        # Make sure that every entry is filled.
        if not all(new_entry.values()):
            tkinter.messagebox.showinfo("Error", "Fill all fields.")
        else:
            self.tree.insert(
                "",
                "end",
                text=new_entry["Date"],
                values=(
                    new_entry["Listened"],
                    new_entry["Title"],
                    new_entry["Theme"],
                    new_entry["Podcast"],
                )
            )
        self.sort_entries()
        self.save_data()


ROOT = tkinter.Tk()
RROOT = RootWindow(ROOT)
ROOT.mainloop()

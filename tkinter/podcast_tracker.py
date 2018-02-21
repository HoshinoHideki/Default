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

        # Window Methods:
        # This removes dashed line from the right-click menu.
        window.option_add("*tearOff", False)
        window.title("Podcast Tracker")
        
        #This allows child widgets to stretch.
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # Creates two main frames.
        for (frame, row) in (
            ("top_frame", 0,),
            ("bottom_frame", 1,),
        ):
            setattr(self, frame, tkinter.ttk.Frame(window))
            getattr(self, frame).grid(row=row, sticky="nsew")
        
        # Creates main buttons.
        for (button, text, command, column) in (
            ("save_button", "Save", self.save_data, 0),
            ("add_button", "Add", lambda: self.new_window("Add"), 1)            
        ):
            setattr(
                self,
                button,
                tkinter.ttk.Button(
                    self.top_frame,
                    text=text,
                    command=command,
                )    
            )
            getattr(self, button).grid(row=0, column=column, sticky="e")

        #Create the data treeview.
        self.tree = tkinter.ttk.Treeview(
            self.bottom_frame,
            columns=(
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
            ("#3", "Title", 300),
            ("#4", "Podcast", 300),
        ):
            self.tree.heading(number, text=text)
            self.tree.column(number, width=width)
        
        # The scrollbar.
        self.scrollbar = tkinter.ttk.Scrollbar(
            self.bottom_frame,
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
            ("Edit", lambda:self.new_window("Edit"))            
        ):
            self.menu.add_command(
                label = label,
                command = command,
            )

        # Binding the Menu to the RMB
        window.bind("<3>", lambda e: self.menu.post(e.x_root, e.y_root))
        
        self.show_data()

    def clear_data(self):
        """Clears the table"""
        self.tree.delete(*self.tree.get_children())
                
    def left_mouse_button(self, event):
        """Binds stuff to lmb"""
        if (
            self.tree.identify(
                "region",
                event.x,
                event.y
            ) == "heading" and
            self.identify(
                "column",
                event.x,
                event.y
            ) == "#0"
        ):
            self.sort_entries()

            self.new_entry_label = tkinter.ttk.Label(
                self,
                text="Add New Entry:"
            )
            self.new_entry_label.grid(row=0, column=0, columnspan=2)
            
            self.labels = (
                ("date_label", "Date:", "date_entry", 1),
                ("title_label", "Title:", "title_entry", 2),
                ("podcast_label", "Podcast:", "podcast_entry", 3),
                ("theme_label", "Theme:", "theme_entry", 4)
            )
            for (name, text, entry, row,) in self.labels:
                setattr(self, name, tkinter.ttk.Label(self, text=text))
                getattr(self, name).grid(row=row, column=0)
                setattr(self, entry, tkinter.ttk.Entry(self))
                getattr(self, entry).grid(row=row, column=1)

            self.buttons = (
                # (object, text, command, row)
                ("save_button", "Save", self.save_data, 0),
                ("add_button", "Add", self.add_data, 1)
            )
            for (name, text, command, column) in self.buttons:
                # creates buttons
                setattr(
                    self,
                    name,
                    tkinter.ttk.Button(
                        self,
                        text=text,
                        command=command
                    )
                )
                getattr(self, name).grid(row=5, column=column, sticky="nsw")

    def new_window(self, function):
        """Shows a new window to edit\add the entry."""
        
        # Creating Editing window
        self.edit_window = tkinter.Toplevel()
        self.edit_window.geometry(
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
            setattr(self, frame, tkinter.ttk.Frame(self.edit_window))
            getattr(self, frame).grid(row=row, column=0)
     
        #Entries Frame
        for (text, object, row) in (
            ("Date", "date_entry", 0),
            ("Listened", "listened_entry", 1),
            ("Title", "title_entry", 2),
            ("Theme", "theme_entry", 3),
            ("Podcast", "podcast_entry", 4),        
        ):
            label = tkinter.ttk.Label(self.edit_window, text=text)
            label.grid(row=row, column=0)
            setattr(self, object, tkinter.ttk.Entry(self.edit_window, width=60))
            getattr(self, object).grid(row=row, column=1)
        
        # Buttons
        if function == "Add":
            text = "Add"
            command = self.write_data
        else:
            text = "Edit"
            command = self.edit_data
        for (name, label, command, column) in (
            ("CloseButton", "Close", self.edit_window.destroy, 0),
            ("OtherButton", text, command, 1)
        ):
            name = tkinter.ttk.Button(
                self.edit_window,
                text=label,
                command=command
            )
            name.grid(row=5, column=column)
        
        # Fetching the data from the tree
        if function is not "Add":
            ItemString = self.tree.item(self.tree.selection())
            ItemText = {
                self.date_entry:        ItemString["text"],
                self.listened_entry:    ItemString["values"][0],
                self.title_entry:       ItemString["values"][1],
                self.theme_entry:       ItemString["values"][2],
                self.podcast_entry:     ItemString["values"][3],
            }
            for key, value in ItemText.items():
                key.insert(0, value)
        
            self.edit_window.focus_set()

    def write_data(self):
        new_entry = {
            "Date": date_entry.get(),
            "Title": title_entry.get(),
            "Podcast": podcast_entry.get(),
            "Theme": theme_entry.get()
        }

        # Make sure that every entry is filled.
        if not all(self.new_entry.values()):
            tkinter.messagebox.showinfo("Error", "Fill all fields.")
        else:
            
            RootWindow.BottomFrame.Treeview.insert(
                "",
                "end",
                text=newentry["Date"],
                values=(
                    newentry["Title"],
                    newentry["Theme"],
                    newentry["Podcast"]
                )
            )
            self.add_button["text"] = "Added."
        RootWindow.sort_entries()

    def delete_entry(self):
        """Deletes the selected item"""
        self.tree.delete(self.tree.selection())

    def edit_data(self):
        """Writes the edited data into memory and reloads the page."""
        self.tree.item(
            self.tree.selection(),
            text=self.edit_window.date_entry.get()
        )
        self.tree.item(
            self.tree.selection(),
            values=(
                title_entry.get(),
                listened_entry.get(),
                theme_entry.get(),
                podcast_entry.get(),
            )
        )
        self.save_data()
        self.edit_window.destroy()

    def edit_entry(self):
        """Creates the editing window with which to edit data."""

        # Fetching the data from the tree
        ItemString = self.tree.item(self.tree.selection())
        ItemText = {
            "Date":     ItemString["text"],
            "Title":    ItemString["values"][0],
            "Theme":    ItemString["values"][1],
            "Podcast":  ItemString["values"][2],
        }

        # Creating the window
        self.edit_window = tkinter.Toplevel()  # creates new window
        self.edit_window.title("Editing an entry.")

        # Buttons
        edit_windowButtons = (
            ("EditEntryCloseButton", "Close", self.edit_window.destroy, 0),
            ("EditEntryEditButton", "Edit", self.edit_data, 1)
        )
        for (
                ButtonName,
                ButtonLabel,
                ButtonCommand,
                ButtonColumn
        ) in edit_windowButtons:
            setattr(
                self,
                ButtonName,
                tkinter.ttk.Button(
                    self.edit_window,
                    text=ButtonLabel,
                    command=ButtonCommand
                )
            )
            #getattr(self, ButtonName).grid(row=4, column=ButtonColumn)

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
        templist = []
        for item in self.tree.get_children():
            templist.append(self.tree.item(item))
        self.clear_data()
        for item in sorted(
                templist,
                key=lambda item: int(item["text"])
        ):
            self.tree.insert(
                "",
                "end",
                text=item["text"],
                values=(
                    item["values"][0],
                    item["values"][1],
                    item["values"][2],
                )
            )

    def save_data():
        """Saves the data into the file."""
        # Creating a list which we are gonna save to file.
        newdata = []
        for item in self.tree.get_children():
            entry = {
                "Date":     self.tree.item(item)["text"],
                "Title":    self.tree.item(item)["values"][0],
                "Listened": self.tree.item(item)["values"][1],
                "Theme":    self.tree.item(item)["values"][2],
                "Podcast":  self.tree.item(item)["values"][3],
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
        self.save_button["text"] = "Saved."
        

class EditFrame(tkinter.ttk.Frame):
    """Same Frame for both Editing and Saving to save typing."""
    def __init__(self, master):
        tkinter.ttk.Frame.__init__(self, master)
        
        # Creating variables from entry names
        self.content = (
            ("Date", "date_entry", 0),
            ("Title", "title_entry", 1),
            ("Listened", "listened_entry", 2),
            ("Theme", "theme_entry", 3),
            ("Podcast", "podcast_entry", 4),
        )
        
        for (text, object, row) in self.content:
            label = tkinter.ttk.Label(self, text=text)
            label.grid(row=row, column=0)
            object = tkinter.ttk.Entry(self)
            object.grid(row=row, column=1)
        
       
        
root = tkinter.Tk()
rroot = RootWindow(root)

root.mainloop()

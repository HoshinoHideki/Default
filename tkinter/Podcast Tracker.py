import tkinter  # interface
import tkinter.ttk
import tkinter.messagebox
import yaml  # database editing

class CreateRootWindow:
    """Window Class."""
    def __init__(self, window):
        self.window = window
        
        # This removes dashed line from the menu.
        window.option_add("*tearOff", False)
        
        # Title.
        window.title("Podcast Tracker")
       
        # Creates main frame.
        self.tabs = tkinter.ttk.Notebook(window)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        # Creates main entries tab & its text label.
        self.tablist = (
            ("entries", "Entries"),
            ("add", "Add")
        )
        for (tab_name, tab_label) in self.tablist:
            setattr(self, tab_name, tkinter.ttk.Frame(self.tabs))
            self.tabs.add(getattr(self, tab_name), text=tab_label)

        # Creates the data table.
        self.tree = tkinter.ttk.Treeview(
            self.entries,
            columns=(
                "Title",
                "Theme",
                "Podcast"
            )
        )
        self.tree.bind("<Button-1>", self.left_mouse_button)
        
        # Setting the names for the column headings.
        self.treeheadings = (
            ("#0","Date"),
            ("#1","Title"),
            ("#2","Title"),
            ("#3","Podcast")
        )
        for (heading_number, heading_title) in self.treeheadings:
            self.tree.heading(heading_number, text=heading_title)
        self.tree.column("#0", width=55)
        self.tree.grid(row=0, column=0, sticky="nsw")

        # The scrollbar.
        self.scrollbar = tkinter.ttk.Scrollbar(
            self.entries,
            orient="vertical",
            command=self.tree.yview
        )
            
        # This feedbacks data to the scrollbar.
        self.tree["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.grid(row=0, column=1, sticky="nes")

        # Adding Labels and Entries.
        self.new_entry_label = tkinter.ttk.Label(
            self.add,
            text="Add New Entry:"
        )
        self.new_entry_label.grid(row=0, column=0)

        self.addwindow_entries = (
            ("date_label", "Date:", "date_entry", 1),
            ("title_label", "Title:", "title_entry", 2),
            ("podcast_label", "Podcast:", "podcast_entry", 3),
            ("theme_label", "Theme:", "theme_entry", 4)
        )
        for (
            label_name,
            label_text,
            entry_name,
            entry_row
        ) in self.addwindow_entries:
            setattr(
                self,
                label_name,
                tkinter.ttk.Label(self.add, text=label_text)
            )
            getattr(self, label_name).grid(row=entry_row, column=0)
            setattr(
                self,
                entry_name,
                tkinter.ttk.Entry(self.add)
            )
            getattr(self, entry_name).grid(row=entry_row, column=1)
           
        self.add_buttons = (
            ("save_button", "Save", self.save_data, 0),
            ("add_button", "Add", self.add_data, 1)
        )
        for (
            button_name,
            button_text,
            button_command,
            button_column
        )in self.add_buttons:
            setattr(
                self,
                button_name,
                tkinter.ttk.Button(
                    self.add,
                    text=button_text,
                    command=button_command
                )
            )
            getattr(self, button_name).grid(row=5, column=button_column)

        # Right-click Menu
        self.menu = tkinter.Menu(window)

        # Binding the Menu to the RMB
        window.bind("<3>", lambda e: self.menu.post(e.x_root, e.y_root))

        # Menu options
        self.menu_options = (
            ("Delete", self.delete_entry),
            ("Edit", self.edit_entry)
        )
        for menu_label, menu_command in self.menu_options:
            getattr(self, "menu").add_command(
                label=menu_label,
                command= menu_command
            )
        
        # This makes sure widgets stretch to the window
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        self.entries.grid_rowconfigure(0, weight=1)
        self.entries.grid_columnconfigure(0, weight=1)

        self.show_data()

    def left_mouse_button(self, event):
        """Binds stuff to lmb"""
        if self.tree.identify("region", event.x, event.y) == "heading" and \
        self.tree.identify("column", event.x, event.y) == "#0":
            self.sort_entries()

    def add_data(self):
        """Adds new entry into the list."""
        newentry = {
            "Date": self.date_entry.get(),
            "Title": self.title_entry.get(),
            "Podcast": self.podcast_entry.get(),
            "Theme": self.theme_entry.get()
        }

        # Make sure that every entry is filled.
        if not all(newentry.values()):
            tkinter.messagebox.showinfo("Error", "Fill all fields.")
        else:
            self.tree.insert(
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
        self.sort_entries()            
 
    def clear_data(self):
        """Clears the table"""
        self.tree.delete(*self.tree.get_children())

    def delete_entry(self):
        """Deletes the selected item"""
        self.tree.delete(self.tree.selection())

    def edit_data(self):
        """Writes the edited data into memory and reloads the page."""
        self.tree.item(
            self.tree.selection(),
            text=self.EditEntryDateEntry.get()
        )
        self.tree.item(
                self.tree.selection(),
                values=(
                    self.EditEntryTitleEntry.get(),
                    self.EditEntryThemeEntry.get(),
                    self.EditEntryPodcastEntry.get()
                )
        )
        self.save_data()
        self.EditWindow.destroy()

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
        self.EditWindow = tkinter.Toplevel()  # creates new window
        self.EditWindow.title("Editing an entry.")
        
       
        # Creating variables from entry names
        self.EditWindowContent = ("Date", "Title", "Theme", "Podcast")
        edit_entries = []
        for item in self.EditWindowContent:
            edit_entries.append(
                (
                    "EditEntry{}Label".format(item),
                    "{}: ".format(item),
                    "EditEntry{}Entry".format(item),
                    ItemText[item],
                    self.EditWindowContent.index(item)
                )
            )
        for (
            EditLabelName,
            EditLabelText,
            EditLabelEntry,
            EditEntryText,
            EditLabelRow
        ) in edit_entries:
            setattr(
                self,
                EditLabelName,
                tkinter.ttk.Label(self.EditWindow, text=EditLabelText)
            )
            setattr(
                self,
                EditLabelEntry,
                tkinter.ttk.Entry(self.EditWindow)
            )
            getattr(self, EditLabelEntry).insert(0, EditEntryText)
            getattr(self, EditLabelName).grid(row=EditLabelRow, column=0)
            getattr(self, EditLabelEntry).grid(row=EditLabelRow, column=1)
            
        # Buttons
        EditWindowButtons = (
            ("EditEntryCloseButton", "Close", self.EditWindow.destroy, 0),
            ("EditEntryEditButton", "Edit", self.edit_data, 1)
        )
        for (
            ButtonName, 
            ButtonLabel, 
            ButtonCommand, 
            ButtonColumn
        ) in EditWindowButtons:
            setattr(
                self, 
                ButtonName, 
                tkinter.ttk.Button(
                    self.EditWindow,
                    text=ButtonLabel,
                    command=ButtonCommand
                )
            )
            getattr(self, ButtonName).grid(row=4, column=ButtonColumn)

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
                    item["Title"],
                    item["Theme"],
                    item["Podcast"]
                )
            )            

    def sort_entries(self):    
        templist = []
        for item in self.tree.get_children():
            templist.append(self.tree.item(item))
        self.clear_data()
        for item in sorted(
            templist,
            key = lambda item: int(item["text"])
        ):
            self.tree.insert(
                "",
                "end",
                text=item["text"],
                values=(
                    item["values"][0],
                    item["values"][1],
                    item["values"][2]
                )
            )

    def save_data(self):
        """Saves the data into the file."""
        # Creating a list which we are gonna save to file.
        newdata = []
        for item in self.tree.get_children():
            entry = {
                "Date": self.tree.item(item)["text"],
                "Title": self.tree.item(item)["values"][0],
                "Theme": self.tree.item(item)["values"][1],
                "Podcast": self.tree.item(item)["values"][2]
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

root = tkinter.Tk()
rroot = CreateRootWindow(root)

root.mainloop()

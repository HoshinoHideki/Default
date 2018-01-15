import tkinter  # interface
import tkinter.ttk
import tkinter.messagebox
import yaml  # database editing
import time # pauses
import operator


class CreateRootWindow:
    """Window Class."""
    def __init__(self, window):
        self.window = window
        
        # This removes dashed line from the menu.
        window.option_add('*tearOff', False)
        
        # Title.
        window.title("Podcast Tracker")

        # Creating stuff.
        # Tabs frame.
        self.tabs = tkinter.ttk.Notebook(window)

        # Entries tab & text label.
        self.entries = tkinter.ttk.Frame(window)
        self.tabs.add(self.entries, text="Entries")
        self.tabs.grid(row=0, column=0, sticky="nsew")

        # New entries tab & text label.
        self.add = tkinter.ttk.Frame(self.tabs)
        self.tabs.add(self.add, text="Add")

        # The table.
        self.tree = tkinter.ttk.Treeview(
            self.entries,
            columns=(
                "Title",
                "Theme",
                "Podcast"
                )
            )
        
        # Setting the names for the column headings.
        self.tree.heading("#0", text="Date")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Theme", text="Theme")
        self.tree.heading("Podcast", text="Podcast")
        self.tree.grid(row=0, column=0, sticky="nsew")

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

        # Date Label.
        self.date_label = tkinter.ttk.Label(self.add, text="Date:")
        self.date_label.grid(row=1, column=0)

        # Date Entry.
        self.date_entry = tkinter.ttk.Entry(self.add)
        self.date_entry.grid(row=1, column=1)

        # Title Label.
        self.title_label = tkinter.ttk.Label(self.add, text="Title:")
        self.title_label.grid(row=2, column=0)

        # Title Entry.
        self.title_entry = tkinter.ttk.Entry(self.add)
        self.title_entry.grid(row=2, column=1)

        # Podcast Label.
        self.podcast_label = tkinter.ttk.Label(self.add, text="Podcast:")
        self.podcast_label.grid(row=3, column=0)

        # Podcast Entry.
        self.podcast_entry = tkinter.ttk.Entry(self.add)
        self.podcast_entry.grid(row=3, column=1)

        # Theme Label.
        self.theme_label = tkinter.ttk.Label(self.add, text="Theme:")
        self.theme_label.grid(row=4, column=0)

        # Theme Entry.
        self.theme_entry = tkinter.ttk.Entry(self.add)
        self.theme_entry.grid(row=4, column=1)

        # Adding the Save Button.
        self.save_button = tkinter.ttk.Button(
            self.add,
            text="Save (test)",
            command=self.save_data)
        self.save_button.grid(row=5, column=0)
        
        # Button for adding an entry.
        self.add_button = tkinter.ttk.Button(
            self.add,
            text="Add (test)",
            command=lambda: self.add_data()
            )
        self.add_button.grid(row=5, column=1)

        # Right-click Menu
        self.menu = tkinter.Menu(window)

        # Binding the Menu to the RMB
        window.bind('<3>', lambda e: self.menu.post(e.x_root, e.y_root))

        # Menu options
        self.menu.add_command(
            label="Delete",
            command=lambda: self.delete_entry()
            )
        self.menu.add_command(
            label="Edit",
            command=lambda: self.edit_entry()
            )
        
        #testing the bindings
        def testcallback(event):
            if self.tree.identify("region", event.x, event.y) == "heading" and \
            self.tree.identify("column", event.x, event.y) == "#0":
                templist = []
                for item in self.tree.get_children():
                    templist.append(self.tree.item(item))
                self.clear_data()
                for item in sorted(templist, key = lambda item: int(item["text"])):
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
        self.tree.bind("<Button-1>", testcallback)
       
        
        # This makes sure widgets stretch to the window
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        self.entries.grid_rowconfigure(0, weight=1)
        self.entries.grid_columnconfigure(0, weight=1)

        self.show_data()
    
    def delete_entry(self):
        """Deletes the selected item"""
        self.tree.delete(self.tree.selection())

    def edit_entry(self):
        """Creates the editing window with which to edit data."""
        ItemString = self.tree.item(self.tree.selection())
        self.EditWindow = tkinter.Toplevel()  # creates new window
        self.EditWindow.title("Editing an entry...")
        
       
        # This creates labels and entries.
        # Date
        self.EditEntryDateLabel = tkinter.ttk.Label(
            self.EditWindow,
            text="Date:"
            )
        self.EditEntryDateLabel.grid(row=0, column=0)
        
        self.EditEntryDateEntry = tkinter.ttk.Entry(self.EditWindow)
        self.EditEntryDateEntry.insert(0, ItemString["text"])
        self.EditEntryDateEntry.grid(row=0, column=1)        
        
        # Title
        self.EditEntryTitleLabel = tkinter.ttk.Label(
            self.EditWindow,
            text="Title:"
            )
        self.EditEntryTitleLabel.grid(row=1, column=0)
 
        self.EditEntryTitleEntry = tkinter.ttk.Entry(self.EditWindow)
        self.EditEntryTitleEntry.insert(0, ItemString["values"][0])
        self.EditEntryTitleEntry.grid(row=1, column=1)  
 
        # Theme
        self.EditEntryThemeLabel = tkinter.ttk.Label(
            self.EditWindow,
            text="Theme:"
            )
        self.EditEntryThemeLabel.grid(row=2, column=0)        

        self.EditEntryThemeEntry = tkinter.ttk.Entry(self.EditWindow)
        self.EditEntryThemeEntry.insert(0, ItemString["values"][1])
        self.EditEntryThemeEntry.grid(row=2, column=1)
        
        # Podcast
        self.EditEntryPodcastLabel = tkinter.ttk.Label(
            self.EditWindow,
            text="Podcast:"
            )
        self.EditEntryPodcastLabel.grid(row=3, column=0)
        
        self.EditEntryPodcastEntry = tkinter.ttk.Entry(self.EditWindow)
        self.EditEntryPodcastEntry.insert(0, ItemString["values"][2])
        self.EditEntryPodcastEntry.grid(row=3, column=1)
        
        # Close Button
        self.EditEntryCloseButton = tkinter.ttk.Button(
            self.EditWindow,
            text="Close",
            command=self.EditWindow.destroy
            )
        self.EditEntryCloseButton.grid(row=4, column=0)
        
        # Edit Button
        self.EditEntryEditButton = tkinter.ttk.Button(
            self.EditWindow,
            text="Edit",
            command= lambda:self.edit_data()
            )
        self.EditEntryEditButton.grid(row=4, column=1)
    
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
        self.reload_data()
        self.EditWindow.destroy()

    def show_data(self):
        """Loads the data into the window."""
        data = list(yaml.load_all(open(
            "newtestdata.txt",
            "r",
            encoding="UTF-8"
            )))

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

    def save_data(self):
        """Saves the data into the file."""
        # Creating a list which we are gonna save to file.
        newdata = []
        for item in self.tree.get_children():
            raw_item = self.tree.item(item)
            entry = {
                "Date": raw_item["text"],
                "Title": raw_item["values"][0],
                "Theme": raw_item["values"][1],
                "Podcast": raw_item["values"][2]
                }
            newdata.append(entry)

        # Dumping the data into the file.
        with open("newtestdata.txt", "w", encoding="UTF-8") as outputfile:
            outputfile.write(
                yaml.dump_all(
                    newdata,
                    allow_unicode=True,
                    default_flow_style=False
                    )
                )
        self.save_button["text"] = "Saved."
        self.reload_data()
        self.save_button.after(5000)
        self.save_button["text"] = "Save."

    def clear_data(self):
        """Clears the table"""
        self.tree.delete(*self.tree.get_children())

    def reload_data(self):
        """Reloads the table"""
        self.clear_data()
        self.show_data()

    def add_data(self):
        """Adds new entry into the list."""
        newdate = self.date_entry.get()
        newtitle = self.title_entry.get()
        newpodcast = self.podcast_entry.get()
        newtheme = self.theme_entry.get()
        newentry = {
            "Date": newdate,
            "Title": newtitle,
            "Podcast": newpodcast,
            "Theme": newtheme
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

root = tkinter.Tk()
rroot = CreateRootWindow(root)

root.mainloop()

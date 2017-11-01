import tkinter             # interface
import tkinter.ttk         # 
import tkinter.messagebox  # 
import yaml                # database editing


class CreateRootWindow:
    """Window Class."""
    def __init__(self, window):
        self.window = window
        window.option_add('*tearOff', False)
        # Title
        window.title("Podcast Tracker")
        
        # Creating stuff
        # Tabs frame
        self.tabs = tkinter.ttk.Notebook(window)
        
        # Entries tab & text label
        self.entries = tkinter.ttk.Frame(window)
        self.tabs.add(self.entries, text="Entries")
        self.tabs.grid(row=0, column=0, sticky="nsew")
        
        # New entries tab & text label
        self.add = tkinter.ttk.Frame(self.tabs)
        self.tabs.add(self.add, text="Add")
        
        # The table
        self.tree = tkinter.ttk.Treeview(
            self.entries,
            columns=("Title", "Theme", "Podcast")
            )
        self.tree.heading("#0", text="Date")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Theme", text="Theme")
        self.tree.heading("Podcast", text="Podcast")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # The scrollbar
        self.scrollbar = tkinter.ttk.Scrollbar(
            self.entries,
            orient="vertical",
            command=self.tree.yview
            )
        # This feedbacks data to the scrollbar
        self.tree["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.grid(row=0, column=1, sticky="nes")
        
        # Adding Labels and Entries
        self.new_entry_label = tkinter.ttk.Label(
            self.add,
            text="Add New Entry:"
            )
        self.new_entry_label.grid(row=0, column=0)

        # Date Label
        self.date_label = tkinter.ttk.Label(
            self.add,
            text="Date:"
            )
        self.date_label.grid(row=1, column=0)

        # Date Entry
        self.date_entry = tkinter.ttk.Entry(self.add)
        self.date_entry.grid(row=1, column=1,)

        # Title Label
        self.title_label = tkinter.ttk.Label(
            self.add,
            text="Title:"
            )
        self.title_label.grid(row=2, column=0)
        
        # Title Entry
        self.title_entry = tkinter.ttk.Entry(self.add)
        self.title_entry.grid(row=2, column=1)
        
        # Podcast Label
        self.podcast_label = tkinter.ttk.Label(
            self.add,
            text="Podcast:"
            )
        self.podcast_label.grid(row=3, column=0)
        
        # Podcast Entry.
        self.podcast_entry = tkinter.ttk.Entry(self.add)
        self.podcast_entry.grid(row=3, column=1)
        
        # Theme Label.
        self.theme_label = tkinter.ttk.Label(
            self.add,
            text="Theme:"
            )
        self.theme_label.grid(row=4, column=0)
        
        # Theme Entry.
        self.theme_entry = tkinter.ttk.Entry(self.add)
        self.theme_entry.grid(row=4, column=1)
        
        # Adding the Save Button
        self.save_button = tkinter.ttk.Button(
            self.add,
            text="Save (test)",
            command=save_data)
        self.save_button.grid(row=5, column=0)
        
        self.add_button = tkinter.ttk.Button(
            self.add,
            text="Add (test)",
            command= lambda: add_data(self))
        self.add_button.grid(row=5, column=1)
        
        # Right-click Menu
        menu = tkinter.Menu(root)
        menu.add_command(
            label="Delete",
            command = lambda:self.delete_entry()
            )
        root.bind('<3>', lambda e: menu.post(e.x_root, e.y_root))
        
        # This makes sure widgets stretch to the window
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        self.entries.grid_rowconfigure(0, weight=1)
        self.entries.grid_columnconfigure(0, weight=1)
        
    def delete_entry(self):
        print(self.tree.item(
            self.tree.selection())
            )
        self.tree.delete(self.tree.selection())


def show_data():
    """Loads the data into the window."""
    for item in data:
        rroot.tree.insert(
            "",
            "end",
            text=item["Date"],
            values=(
                item["Title"],
                item["Theme"],
                item["Podcast"]
                )
            )


def save_data():
    """Saves the data into the file."""
    with open("testdata.txt", "w", encoding="UTF-8") as outputfile:
        outputfile.write(yaml.dump_all(
            data,
            allow_unicode=True,
            default_flow_style=False
            )
        )
    rroot.save_button["text"] = "Saved."
    reload_data(rroot)


def add_data(app):
    """Adds new entry into the list."""
    NewDate = app.date_entry.get()
    NewTitle = app.title_entry.get()
    NewPodcast = app.podcast_entry.get()
    NewTheme = app.theme_entry.get()
    NewEntry = {
        "Date" : NewDate,
        "Title" : NewTitle,
        "Podcast" : NewPodcast,
        "Theme" : NewTheme}
    
    # Make sure if every entry is filled
    if not all(NewEntry.values()):
        tkinter.messagebox.showinfo("Error", "Fill all fields.")
    else:
        data.append(NewEntry)
        app.add_button["text"] = "Added."


def clear_data(app):
    app.tree.delete(*app.tree.get_children())


def reload_data(app):
    clear_data(app)
    show_data()




    
# Loads the data into the application.
data = list(yaml.load_all(open("testdata.txt", "r", encoding="UTF-8")))


root = tkinter.Tk()
rroot = CreateRootWindow(root)

show_data()
root.mainloop()

import tkinter      # interface
import tkinter.ttk  # interface
import yaml         # database editing


class CreateRootWindow:
    def __init__(self, window):
        self.window = window
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
            orient='vertical',
            command=self.tree.yview
            )
        # This feedbacks data to the scrollbar
        self.tree['yscrollcommand'] = self.scrollbar.set
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
        
    
        
		
	    # This makes sure widgets stretch to the window
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        self.entries.grid_rowconfigure(0, weight=1)
        self.entries.grid_columnconfigure(0, weight=1)


def show_data():
    """Loads the data into the window."""
    for item in data:
        rroot.tree.insert(
            "",
            'end',
            text=item[0]['Date'],
            values=(
                item[0]["Title"],
                item[0]['Theme'],
                item[0]["Podcast"]
                )
            )


def save_data(data):
    """Saves the data into the file."""
    with open("newdata.txt", "w", encoding="UTF-8") as outputfile:
        outputfile.write(yaml.dump_all(
            data,
            allow_unicode=True,
            default_flow_style=False
            )
        )
    rroot.save_button["text"] = "Saved."

data = yaml.load_all(open("testdata.txt", "r", encoding="UTF-8"))
root = tkinter.Tk()
rroot = CreateRootWindow(root)
# Loads the data into the application.

show_data()
root.mainloop()

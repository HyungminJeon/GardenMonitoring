import os
import tkinter as tk
import tkinter.ttk as ttk

import botocore
from ttkthemes import ThemedTk
import webbrowser
import boto3

# Just simply import the azure.tcl file


button_names = {
    "0": "1. View gardens",
    "1": "2. Create a new garden",
    "2": "3. Sync garden data",
    "3": "4. Start garden monitoring",
}

"""
guitest.py was built with the help from the following
Example script and assets, for testing the Azure ttk theme.
Any additional implementation is original work created by
Capstone, Group 7 (AGM), at Bellevue College.
Original Author: rdbende
License: MIT license
Source: https://github.com/rdbende/ttk-widget-factory
"""


# import tkinter as tk
# from tkinter import ttk

class App(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # AccountInfo
        # Create a client for the IAM service
        self.iam_client = boto3.client('iam')

        # Call the get_user method to retrieve the IAM user information
        self.user_info = self.iam_client.get_user()

        self.gardens = {}
        self.session = boto3.Session()
        self.s3_client = self.session.client('s3')
        self.s3 = self.session.resource('s3')
        # Get the user's email (if available)
        try:
            self.email = self.user_info['User']['Email']
        except KeyError:
            self.email = 'Email not available'
        for bucket in self.s3.buckets.all():
            # existing s3 buckets will default to a non-active status
            if bucket.name not in self.gardens:
                self.gardens[bucket.name] = "non-active"

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "Select Garden"]
        for i, (name, status) in enumerate(self.gardens.items()):
            garden = {"name": name, "garden id": i + 1}
            self.option_menu_list.append(garden)

        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.progress_percentage = 50.0
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=False)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=self.progress_percentage)

        # Create widgets :)
        self.setup_widgets()




    def setup_widgets(self):

        # Create a Frame for the Checkbuttons
        self.account_frame = ttk.LabelFrame(self, text="Account", padding=(20, 10))
        self.account_frame.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.account_name = ttk.Label(
            self.account_frame, text=str("username:      " + self.user_info['User']['UserName'])
        )
        self.account_name.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.account_email = ttk.Label(
            self.account_frame, text=str("email:      " + self.email)
        )
        self.account_email.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.account_frame, text="Allow automatic uploads to AWS", variable=self.var_1
        )
        self.check_2.grid(row=3, column=0, padx=5, pady=50, sticky="nsew")

        self.dashboard = ttk.Button(self.account_frame, style="Accent.TButton", text="Go to my AGM Dashboard",
                                    command=lambda: webbrowser.open("http://localhost:3000/garden"))
        self.dashboard.grid(row=4, column=0, padx=5, pady=20, sticky="nsew")

        # log out Button
        self.button = ttk.Button(self.account_frame, text="Log out")
        self.button.grid(row=6, column=0, padx=5, pady=20, sticky="nsew")

        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        # Entry
        self.garden_entry = ttk.Entry(self.widgets_frame)
        self.garden_entry.insert(0, "Garden Name")
        self.garden_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        # Add Garden Button
        self.button2 = ttk.Button(self.widgets_frame, text="Add Garden",
                                  command=lambda: self.new_user_garden(self.garden_entry.get()))
        self.button2.grid(row=2, columnspan=1, padx=5, pady=10, sticky="nsew")

        # Remove Garden Button
        self.button3 = ttk.Button(self.widgets_frame, text="Remove Garden",
                                  command=lambda: self.remove_user_garden(self.garden_entry.get()))
        self.button3.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")

        # # Spinbox
        # self.spinbox = ttk.Spinbox(self.widgets_frame, from_=0, to=100, increment=0.1)
        # self.spinbox.insert(0, "Spinbox")
        # self.spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Combobox
        # self.combobox = ttk.Combobox(self.widgets_frame, values=self.combo_list)
        # self.combobox.current(0)
        # self.combobox.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Read-only combobox
        # self.readonly_combo = ttk.Combobox(
        #     self.widgets_frame, state="readonly", values=self.readonly_combo_list
        # )
        # self.readonly_combo.current(0)
        # self.readonly_combo.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Menu for the Menubutton
        # self.menu = tk.Menu(self)
        # self.menu.add_command(label="Menu item 1")
        # self.menu.add_command(label="Menu item 2")
        # self.menu.add_separator()
        # self.menu.add_command(label="Menu item 3")
        # self.menu.add_command(label="Menu item 4")

        # # Menubutton
        # self.menubutton = ttk.Menubutton(
        #     self.widgets_frame, text="Menubutton", menu=self.menu, direction="below"
        # )
        # self.menubutton.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # OptionMenu
        self.optionmenu = ttk.OptionMenu(
            self.widgets_frame, self.var_4, *self.option_menu_list
        )
        self.optionmenu.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        self.update_option_list()

        # Accentbutton
        self.accentbutton = ttk.Button(
            self.widgets_frame, text="Start Garden Monitoring", style="Accent.TButton"
        )
        self.accentbutton.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # Togglebutton
        self.togglebutton = ttk.Checkbutton(
            self.widgets_frame, text="Ready", style="Toggle.TButton"
        )
        self.togglebutton.grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # Switch
        self.switch = ttk.Checkbutton(
            self.widgets_frame, text="Tello Connected", style="Switch.TCheckbutton", state="disabled"
        )
        self.switch.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=1, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)

        # Treeview headings
        self.treeview.heading("#0", text="Garden Name", anchor="center")
        self.treeview.heading(1, text="Status", anchor="center")
        # self.treeview.heading(2, text="Column 3", anchor="center")

        # Define treeview data
        treeview_data = [
            ("", 1, f"Garden A", "Inactive"),
            (1, 2, "plant1", "Not_Captured"),
            (1, 3, "plant2", "Not_Captured"),
            (1, 4, "plant3", "Not_Captured"),
            (1, 5, "plant4", "Not_Captured"),
            ("", 6, "Garden B", "Inactive"),
            (6, 7, "plant", "Not_Captured"),
            (6, 8, "Sub-Garden B", "Inactive"),
            (8, 9, "plant", "Not_Captured"),
            (8, 10, "plant", "Not_Captured"),
            (8, 11, "plant", "Not_Captured"),
            (6, 12, "plant", "Not_Captured"),
            (6, 13, "plant", "Not_Captured")
        ]

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

        # Select and scroll
        self.treeview.selection_set(10)
        self.treeview.see(7)

        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Monitoring Progress")

        # Scale
        # self.scale = ttk.Scale(
        #     self.tab_1,
        #     from_=100,
        #     to=0,
        #     variable=self.var_5,
        #     command=lambda event: self.var_5.set(self.scale.get()),
        # )
        # self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

        # Progressbar
        self.progress = ttk.Progressbar(
            self.tab_1, value=0, variable=self.var_5, mode="determinate"
        )
        self.progress.grid(row=0, column=0, columnspan=2, padx=(10, 20), pady=(20, 0), sticky="ew")

        # Label
        self.label = ttk.Label(
            self.tab_1,
            text=f"Current progress =  {self.var_5}%",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label.grid(row=1, column=0, pady=10, columnspan=2)

        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="Garden 1 Images")

        # Tab #3
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text="Garden 2 Images")

        # Tab #4
        self.logs = ttk.Frame(self.notebook)
        self.notebook.add(self.logs, text="Monitoring Logs")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

    def update_option_list(self):
        # check for new bucket names not in gardens dictionary
        for bucket in self.s3.buckets.all():
            # new buckets default to a non-active status
            if bucket.name not in self.gardens:
                self.gardens[bucket.name] = "non-active"

        # create a list of garden names
        # include dictionaries in the option_menu_list and then extract the "name" value from each dictionary
        garden_names = [garden["name"] for garden in self.option_menu_list if isinstance(garden, dict)]

        # add new gardens to the option menu
        for name, status in self.gardens.items():
            if name not in garden_names:
                garden = {"name": name, "garden id": len(self.option_menu_list) + 1}
                self.option_menu_list.append(garden)
                garden_names.append(name)
                self.optionmenu['menu'].add_command(label=name,
                                                    command=lambda value=name: self.selected_garden.set(value))

        # Remove gardens from the option menu that are no longer in self.gardens
        menu = self.optionmenu['menu']
        for i in range(menu.index('end')):
            label = menu.entrycget(i, 'label')
            if label not in self.gardens:
                menu.delete(i)

        # clear the current option menu and repopulate it with the updated garden list
        self.optionmenu['menu'].delete(0, tk.END)
        for garden in self.option_menu_list:
            if isinstance(garden, dict):
                self.optionmenu['menu'].add_command(label=garden['name'],
                                                    command=lambda value=garden['name']: self.selected_garden.set(
                                                        value))


    def new_user_garden(self, garden_name):
        response = "new_user_garden empty response"
        garden_created = False
        try:
            response = self.s3_client.create_bucket(
                Bucket=garden_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-2',
                },
            )
        except self.s3_client.exceptions.ClientError:
            print("Invalid bucket name\n")
        except self.s3_client.exceptions.BucketAlreadyExists:
            print("Garden name already exists\n")
        else:
            garden_created = True
        # add new garden to the option list
        self.update_option_list()
        print(response)


    def remove_user_garden(self, garden_name):
        response = "remove_user_garden empty response"
        try:
            response = self.s3_client.delete_bucket(
                Bucket=garden_name,
            )
            # Remove the garden from the gardens dictionary
            if garden_name in self.gardens:
                self.gardens.pop(garden_name)

                # Remove the garden from the option menu list
            for i, garden in enumerate(self.option_menu_list):
                if isinstance(garden, dict) and garden['name'] == garden_name:
                    self.option_menu_list.pop(i)
                    break

        except self.s3_client.exceptions.ClientError:
            print("Invalid bucket name\n")
        except botocore.exceptions.ParamValidationError as e:
            # handle the exception here
            print("ParamValidationError: {}".format(str(e)))

        # Update the option menu list
        self.gardens.pop(garden_name, None)
        self.update_option_list()
        print(response)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("AGM-Pilot")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()

import pandas as pd
from tkinter import filedialog
from tkinter import Tk, Label, Button

class EmployeeRoster:
    def __init__(self, master):
        self.master = master
        master.title("Employee Roster")

        self.label = Label(master, text="Select two employee rosters to compare")
        self.label.grid(row=0, column=0, columnspan=2)

        self.select_button = Button(master, text="Select files", command=self.select_files)
        self.select_button.grid(row=1, column=0, columnspan=2)

        self.compare_button = Button(master, text="Compare rosters", command=self.compare_files)
        self.compare_button.grid(row=2, column=0, columnspan=2)

        self.joined_label = Label(master, text="")
        self.joined_label.grid(row=3, column=0)

        self.left_label = Label(master, text="")
        self.left_label.grid(row=3, column=1)

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")))
        # clear labels each time new files are selected
        self.joined_label['text'] = ""
        self.left_label['text'] = ""

    def compare_files(self):
        try:
            if len(self.filepaths) != 2:
                raise ValueError("Please select exactly two files")
            
            roster1 = pd.read_csv(self.filepaths[0])
            roster2 = pd.read_csv(self.filepaths[1])

            # check for required columns in both files
            for df in [roster1, roster2]:
                if 'first name' not in df or 'last name' not in df:
                    raise ValueError("Both files should have 'first name' and 'last name' columns")

            roster1['fullname'] = roster1['first name'] + ' ' + roster1['last name']
            roster2['fullname'] = roster2['first name'] + ' ' + roster2['last name']

            roster1_set = set(roster1['fullname'])
            roster2_set = set(roster2['fullname'])

            joined = roster2_set - roster1_set
            left = roster1_set - roster2_set

            self.joined_label['text'] = "Employees who joined:\n" + '\n'.join(joined)
            self.left_label['text'] = "Employees who left:\n" + '\n'.join(left)
        except Exception as e:
            # reset labels in case of error
            self.joined_label['text'] = ""
            self.left_label['text'] = ""
            # show error message in a label
            self.error_label = Label(self.master, text=f"Error: {str(e)}")
            self.error_label.grid(row=4, column=0, columnspan=2)

root = Tk()
app = EmployeeRoster(root)
root.mainloop()

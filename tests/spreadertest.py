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

        self.file_label = Label(master, text="")
        self.file_label.grid(row=4, column=0, columnspan=2)

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")))
        # clear labels each time new files are selected
        self.joined_label['text'] = ""
        self.left_label['text'] = ""
        self.file_label['text'] = f"Selected files: {self.filepaths}"

    def read_and_validate_file(self, filepath):
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            raise ValueError(f"File not found: {filepath}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"File is empty: {filepath}")

        required_columns = ['first name', 'last name', 'email']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"File {filepath} should have 'first name', 'last name', and 'email' columns")

        df['fullname'] = df['first name'] + ' ' + df['last name']

        return df

    def compare_files(self):
        try:
            if len(self.filepaths) != 2:
                raise ValueError("Please select exactly two files")
            
            roster1 = self.read_and_validate_file(self.filepaths[0])
            roster2 = self.read_and_validate_file(self.filepaths[1])

            roster1_emails = set(roster1['email'])
            roster2_emails = set(roster2['email'])

            joined_emails = roster2_emails - roster1_emails
            left_emails = roster1_emails - roster2_emails

            joined = roster2[roster2['email'].isin(joined_emails)]
            left = roster1[roster1['email'].isin(left_emails)]

            joined_names = set(joined['fullname'].tolist())
            left_names = set(left['fullname'].tolist())

            # Names that appear in both categories
            both_categories = joined_names & left_names

            # Subtract names that appear in both categories
            joined_names -= both_categories
            left_names -= both_categories

            self.joined_label['text'] = "Employees who joined:\n" + '\n'.join(joined_names)
            self.left_label['text'] = "Employees who left:\n" + '\n'.join(left_names)
        except Exception as e:
            # reset labels in case of error
            self.joined_label['text'] = ""
            self.left_label['text'] = ""
            self.file_label['text'] = f"Error: {str(e)}"

root = Tk()
app = EmployeeRoster(root)
root.mainloop()

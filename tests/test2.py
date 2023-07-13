import pandas as pd
from tkinter import filedialog
from tkinter import Tk, Label, Frame, Button, Text, Scrollbar

class EmployeeRoster:
    def __init__(self, master):
        self.master = master
        master.title("Employee Roster")

        self.label = Label(master, text="Select two employee rosters to compare", font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.select_button = Button(master, text="Select files", command=self.select_files, font=("Helvetica", 14))
        self.select_button.grid(row=1, column=0, columnspan=2)

        self.compare_button = Button(master, text="Compare rosters", command=self.compare_files, font=("Helvetica", 14))
        self.compare_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a Frame for text widgets and their scrollbars
        self.text_frame = Frame(master)
        self.text_frame.grid(row=3, column=0, columnspan=2)

        # Initialize Scrollbar
        self.scrollbar = Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Initialize Text Widget
        self.text_widget = Text(self.text_frame, width=50, height=10, yscrollcommand=self.scrollbar.set, font=("Helvetica", 12))
        self.text_widget.pack()

        # Configure the scrollbars to move with the text widget
        self.scrollbar.config(command=self.text_widget.yview)

        # Initially clear text widget
        self.text_widget.delete(1.0, "end")

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")))
        self.text_widget.delete(1.0, "end")

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

    # ... rest of your class definition ...

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

            # Check for name matches in 'joined' and 'left' categories to identify email changes
            email_changes = {name: {"old_email": left[left['fullname'] == name]['email'].values[0],
                                    "new_email": joined[joined['fullname'] == name]['email'].values[0]}
                            for name in joined_names & left_names}

            # Subtract names that appear in both categories
            joined_names -= set(email_changes.keys())
            left_names -= set(email_changes.keys())

            self.joined_label['text'] = "Employees who joined:\n" + '\n'.join(joined_names)
            self.left_label['text'] = "Employees who left:\n" + '\n'.join(left_names)

            # Display email changes
            self.email_changes_label['text'] = "Email changes:\n" + '\n'.join(
                [f"{name}: {info['old_email']} -> {info['new_email']}" for name, info in email_changes.items()])
            
            name_changes = {email: {"old_name": roster1[roster1['email'] == email]['fullname'].values[0],
                        "new_name": roster2[roster2['email'] == email]['fullname'].values[0]}
                 for email in roster1_emails & roster2_emails 
                 if roster1[roster1['email'] == email]['fullname'].values[0] != 
                    roster2[roster2['email'] == email]['fullname'].values[0]}
            
            self.name_changes_label['text'] = "Name changes:\n" + '\n'.join([f"{email}: {info['old_name']} -> {info['new_name']}" for email, info in name_changes.items()])

    
            
            self.text_widget.delete(1.0, "end")
            self.text_widget.insert("end", "Employees who joined:\n")
            self.text_widget.insert("end", '\n'.join(joined_names) + "\n\n")
            self.text_widget.insert("end", "Employees who left:\n")
            self.text_widget.insert("end", '\n'.join(left_names) + "\n\n")
            self.text_widget.insert("end", "Email changes:\n")
            self.text_widget.insert("end", '\n'.join([f"{name}: {info['old_email']} -> {info['new_email']}" for name, info in email_changes.items()]) + "\n")
            
        except Exception as e:
            self.text_widget.delete(1.0, "end")
            self.text_widget.insert("end", f"Error: {str(e)}")

root = Tk()
app = EmployeeRoster(root)
root.mainloop()

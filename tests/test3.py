import pandas as pd
from tkinter import filedialog
from tkinter import Tk, Label, Frame, Button, Text, Scrollbar, Menu, messagebox


class EmployeeRoster:
    def __init__(self, master):
        self.master = master
        master.title("Comparerator")

        self.label = Label(master, text="Select two rosters to compare", font=("Apple", 16, "bold"), bg="White Smoke")
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

        self.select_button = Button(master, text="Select files", command=self.select_files, font=("Apple", 14),  )
        self.select_button.grid(row=2, column=0, columnspan=4)

        self.compare_button = Button(master, text="Compare rosters", command=self.compare_files, font=("Apple", 14))
        self.compare_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.widgets = {
            "joined": self.create_scrollable_text(master, "Employees who joined:", 4, 0),
            "left": self.create_scrollable_text(master, "Employees who left:", 4, 1),
            "email_changes": self.create_scrollable_text(master, "Email changes:", 4, 2),
            "name_changes": self.create_scrollable_text(master, "Name changes:", 4, 3),
        }

                # Custom menu frame
        self.menu_frame = Frame(master, bg="gainsboro")
        self.menu_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Help Button
        self.help_button = Button(self.menu_frame, text="Help", command=self.display_help, font=("Apple", 14), bg="gray")
        self.help_button.pack(side="left", padx=5, pady=5)

        # Info Button
        self.info_button = Button(self.menu_frame, text="Info", command=self.display_info, font=("Apple", 14), bg="gainsboro")
        self.info_button.pack(side="left", padx=5, pady=5)

        self.label = Label(master, text="Select two rosters to compare", font=("Apple", 16, "bold"), bg="White Smoke")
        self.label.grid(row=1, column=0, columnspan=4, pady=10)

    def create_scrollable_text(self, master, label_text, row, column):
        label = Label(master, text=label_text, font=("Apple", 14, "bold"), bg="gainsboro")
        label.grid(row=row, column=column, padx=10, sticky="nw")

        frame = Frame(master)
        frame.grid(row=row+1, column=column, padx=10, sticky="nsew")

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = Text(frame, width=40, height=37, yscrollcommand=scrollbar.set, font=("Apple", 12))
        text_widget.pack(fill="both", expand=True)

        scrollbar.config(command=text_widget.yview)

        text_widget.delete(1.0, "end")

        return label, text_widget
    
    def display_help(self):
        help_text = "Employee Roster Comparison Tool\n This tool allows you to compare two employee rosters and find out which employees have joined, left, or made changes to their information.\n\n\n Help and Info sections \n\nHow to Use Run the program.\n Click the Select files button and choose two CSV files to compare.\n The CSV files should have 'first name', 'last name', and 'email' columns.\n Click the Compare rosters button.\n The program will then compare the two rosters and display the following:\n -Employees who joined\n -Employees who left\n -Changes in email\n -Changes in name \nCheck the total count of employees in the old roster, the new roster, the ones that left, and the ones that joined, by clicking the Info button on the menu. \nFor more details on how to use the program, reach out to\n Tyler W. Clark at tclark@hudsonalpha.org."
        messagebox.showinfo("Help", help_text)

    def display_info(self):
        try:
            roster1 = self.read_and_validate_file(self.filepaths[0])
            roster2 = self.read_and_validate_file(self.filepaths[1])
            total_old = len(roster1)
            total_new = len(roster2)
            total_joined = len(set(roster2['email']) - set(roster1['email']))
            total_left = len(set(roster1['email']) - set(roster2['email']))
        except Exception as e:
            messagebox.showinfo("Info", f"Error: {str(e)}")
            return

        info_text = f"Total employees in old roster: {total_old}\n" \
                    f"Total employees in new roster: {total_new}\n" \
                    f"Total employees left: {total_left}\n" \
                    f"Total employees joined: {total_joined}"
        messagebox.showinfo("Info", info_text)


    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")))
        for widget in self.widgets.values():
            label, text_widget = widget
            text_widget.delete(1.0, "end")

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

            # Check for name matches in 'joined' and 'left' categories to identify email changes
            email_changes = {name: {"old_email": left[left['fullname'] == name]['email'].values[0],
                                    "new_email": joined[joined['fullname'] == name]['email'].values[0]}
                            for name in joined_names & left_names}

            # Subtract names that appear in both categories
            joined_names -= set(email_changes.keys())
            left_names -= set(email_changes.keys())

            name_changes = {email: {"old_name": roster1[roster1['email'] == email]['fullname'].values[0],
                        "new_name": roster2[roster2['email'] == email]['fullname'].values[0]}
                for email in roster1_emails & roster2_emails 
                if roster1[roster1['email'] == email]['fullname'].values[0] != 
                    roster2[roster2['email'] == email]['fullname'].values[0]}   

            # Clear all text widgets
            for widget in self.widgets.values():
                label, text_widget = widget
                text_widget.delete(1.0, "end")

            # Write results to text widgets
            self.write_to_text_widget("joined", '\n'.join(sorted(joined_names)))
            self.write_to_text_widget("left", '\n'.join(sorted(left_names)))
            self.write_to_text_widget("email_changes", '\n'.join(sorted([f"{name}:\n {info['old_email']} \n-> {info['new_email']}\n" for name, info in email_changes.items()])))
            self.write_to_text_widget("name_changes", '\n'.join(sorted([f"{email}: {info['old_name']} -> {info['new_name']}" for email, info in name_changes.items()])))

        except Exception as e:
            for widget in self.widgets.values():
                label, text_widget = widget
                text_widget.delete(1.0, "end")
                text_widget.insert("end", f"Error: {str(e)}")



    def write_to_text_widget(self, widget_key, text):
        label, text_widget = self.widgets[widget_key]
        text_widget.insert("end", text)



root = Tk()
root.geometry('1400x800')
root.config(bg="White Smoke")
root.resizable(False, False)
app = EmployeeRoster(root)
root.mainloop()
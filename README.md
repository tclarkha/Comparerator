# Comparerator
Employee Roster Comparison Tool

This tool allows you to compare two employee rosters and find out which employees have joined, left, or made changes to their information.

Features
- Select two CSV files to compare
- See employees who joined, left, or made changes to their name or email
- See the total count of old employees, new employees, those who left and those who joined

# How to use
Click the Select files button and choose two CSV files to compare. The CSV files should have 'first name', 'last name', and 'email' columns.
Make sure to select the **OLD roster first, and the NEW roster second.** 
Click the Compare rosters button. 

The program will then compare the two rosters and display the following:
- Employees who joined
- Employees who left
- Changes in email
- Changes in name

Check the total count of employees in the old roster, the new roster, the ones that left, and the ones that joined, by clicking the Info button on the menu.

For more details on how to use the program, click the Help button on the menu.

Requirements
- Python 3
- pandas
- Tkinter

# Installation

Install Python 3 and pip if you haven't already.

Clone this repository or download the Python script.

Install the requirements with pip:

sh
pip install -r requirements.txt
Run the script:

sh
python employee_roster.py
Note: This program is tested on Python 3.8 and pandas 1.2.4. For the user interface, Tkinter which is the standard Python interface to the Tk GUI toolkit, is used.


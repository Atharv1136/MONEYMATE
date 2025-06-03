import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt  # Added import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Global variables
initial_balance = 0.0
expenses = []

# Function to set initial balance
def set_initial_balance():
    global initial_balance
    try:
        initial_balance = float(initial_balance_entry.get())
        initial_balance_label.config(text=f"Initial Balance: ₹ {initial_balance:.2f}")
        salary_window.destroy()  # Close the salary window
        expense_window.deiconify()  # Show the expense window
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid initial balance.")

# Function to add an expense
def add_transaction():
    description = description_entry.get()
    amount = amount_entry.get()

    if description and amount:
        expenses.append((description, float(amount)))
        tree.insert("", tk.END, values=(description, amount))
        description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

        # Update total money and balance
        total_money.set(f"Total Money: ₹ {initial_balance:.2f}")
        balance = calculate_balance()
        balance_label.config(text=f"Balance: ₹ {balance:.2f}")

        # Schedule the next update after 30 seconds
        expense_window.after(30000, add_transaction)

# Function to delete selected expense
def delete_transaction():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        index = selected_item[0][1:]
        del expenses[int(index)]

        # Update total money and balance
        total_money.set(f"Total Money: ₹ {initial_balance:.2f}")
        balance = calculate_balance()
        balance_label.config(text=f"Balance: ₹ {balance:.2f}")

# Function to show analysis window with pie chart
def show_analysis():
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Expense Analysis")

    # Calculate total expenses
    total_expenses = sum(expense[1] for expense in expenses)

    # Calculate remaining balance
    remaining_balance = initial_balance - total_expenses

    # Display total balance remaining
    balance_label = ttk.Label(analysis_window, text=f"Remaining Balance: ₹ {remaining_balance:.2f}", font=('Arial', 12, 'bold'))
    balance_label.pack(pady=10)

    # Create a pie chart
    categories = [expense[0] for expense in expenses]
    amounts = [expense[1] for expense in expenses]

    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Expense Categories")
    plt.axis('equal')

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=analysis_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to calculate balance
def calculate_balance():
    total_expenses = sum(expense[1] for expense in expenses)
    return initial_balance - total_expenses

# Create the main window
root = tk.Tk()
root.title("Budget Management App")

# Adding image and text to start tab
start_tab = ttk.Frame(root)
start_tab.grid(row=0, column=0, padx=10, pady=10)

# Load and display the image
image = Image.open("LOGO.png")  # Change "LOGO.png" to the path of your image file
photo = ImageTk.PhotoImage(image)
image_label = ttk.Label(start_tab, image=photo)
image_label.grid(row=0, column=0, padx=20, pady=20)

# Bold calligraphy text
text_label = ttk.Label(start_tab, text="Unlock Financial Freedom: Budgeting Made Simple.", font=('Bernard MT Condensed', 24, 'bold'))
text_label.grid(row=1, column=0, pady=10)

# Start Button
def start_application():
    salary_window.deiconify()
    start_tab.destroy()

start_button = ttk.Button(start_tab, text="Start", command=start_application)
start_button.grid(row=2, column=0, pady=(10, 20))

# Ask for salary window
salary_window = tk.Toplevel(root)
salary_window.title("Enter Initial Salary")

# Frame for input and buttons
input_frame_salary = ttk.Frame(salary_window, padding="10")
input_frame_salary.grid(row=0, column=0, sticky=(tk.W, tk.E))

initial_balance_label = ttk.Label(input_frame_salary, text="Enter Initial Salary (₹):")
initial_balance_label.grid(row=0, column=0, sticky=tk.W)
initial_balance_entry = ttk.Entry(input_frame_salary, width=15)
initial_balance_entry.grid(row=0, column=1, padx=(0, 10))

set_balance_button = ttk.Button(input_frame_salary, text="Set Initial Salary", command=set_initial_balance)
set_balance_button.grid(row=0, column=2)

# Frame for adding expenses window
expense_window = tk.Toplevel(root)
expense_window.title("Add Expenses")

# Frame for input and buttons
input_frame_expense = ttk.Frame(expense_window, padding="10")
input_frame_expense.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Description Entry
description_label = ttk.Label(input_frame_expense, text="Description:")
description_label.grid(row=0, column=0, sticky=tk.W)
description_entry = ttk.Entry(input_frame_expense, width=30)
description_entry.grid(row=0, column=1, padx=(0, 10))

# Amount Entry
amount_label = ttk.Label(input_frame_expense, text="Amount (₹):")
amount_label.grid(row=1, column=0, sticky=tk.W)
amount_entry = ttk.Entry(input_frame_expense, width=15)
amount_entry.grid(row=1, column=1)

# Add Transaction Button
add_button = ttk.Button(input_frame_expense, text="Add Expense", command=add_transaction)
add_button.grid(row=1, column=2, padx=(10, 0))

# Treeview for displaying transactions
tree = ttk.Treeview(expense_window, columns=("Description", "Amount"), show="headings")
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount")
tree.column("Description", anchor=tk.CENTER)
tree.column("Amount", anchor=tk.CENTER)
tree.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Delete Transaction Button
delete_button = ttk.Button(expense_window, text="Delete Expense", command=delete_transaction)
delete_button.grid(row=2, column=0, pady=(10, 0))

# Frame for total money and balance
total_money = tk.StringVar()
total_money.set("Total Money: ₹ 0.00")
total_money_label = ttk.Label(input_frame_expense, textvariable=total_money, font=('Arial', 12, 'bold'))
total_money_label.grid(row=3, column=0, pady=(10, 0))

balance_label = ttk.Label(input_frame_expense, text="Balance: ₹ 0.00", font=('Arial', 12, 'bold'))
balance_label.grid(row=4, column=0, pady=(5, 0))

# Analysis Button
analysis_button = ttk.Button(input_frame_expense, text="Analysis", command=show_analysis)
analysis_button.grid(row=5, column=0, pady=(10, 20))

# Hide expense window initially
expense_window.withdraw()


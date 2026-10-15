"""
=============================================================================
Project Title   : Expense Tracker Application
Technology      : Python 3, Tkinter GUI, CSV File Storage, Datetime
Purpose         : College Mini Project (Problem-Based Learning / Practical Exam)
Key Concepts    : Variables, Data Types, Conditionals, Loops, Functions,
                  Lists & Dictionaries, File & CSV Handling, Exception Handling,
                  and Date/Time Validation.
=============================================================================
"""

import csv
import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
# CSV file path where expense data is permanently stored
DATA_FILE = "expenses.csv"

# Predefined expense categories for user selection
CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Other",
]

# Currency symbol used throughout the application
CURRENCY = "₹"

# Color Palette for a modern desktop look
COLOR_BG = "#f1f5f9"           # Slate 100 - window background
COLOR_CARD_BG = "#ffffff"      # White card surface
COLOR_HEADER_BG = "#1e293b"    # Slate 800 - dark header
COLOR_HEADER_TEXT = "#ffffff"
COLOR_PRIMARY = "#2563eb"      # Blue 600 - primary buttons
COLOR_PRIMARY_HOVER = "#1d4ed8"
COLOR_DANGER = "#dc2626"       # Red 600 - delete button
COLOR_SUCCESS = "#16a34a"      # Green 600 - add button
COLOR_TEXT_DARK = "#0f172a"    # Slate 900 - main labels
COLOR_TEXT_MUTED = "#64748b"   # Slate 500 - sub labels
COLOR_BORDER = "#cbd5e1"       # Slate 300 - borders


# =============================================================================
# SECTION 1: DATA LAYER (FILE HANDLING & CSV OPERATIONS)
# =============================================================================

def initialize_csv(filepath=DATA_FILE):
    """
    Ensure the CSV file exists with the proper header row.
    Demonstrates: File handling, Conditionals, CSV Writer.
    """
    if not os.path.exists(filepath):
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Write CSV header row
                writer.writerow(["Date", "Category", "Amount", "Description"])
        except IOError as error:
            messagebox.showerror("File Error", f"Unable to create data file: {error}")


def load_expenses_from_csv(filepath=DATA_FILE):
    """
    Reads all expense records from the CSV file into a Python list of dictionaries.
    Demonstrates: Exception handling (try/except), File reading, Loops, Lists, Dictionaries.
    
    Returns:
        list of dict: [{'Date': '...', 'Category': '...', 'Amount': float, 'Description': '...'}, ...]
    """
    initialize_csv(filepath)
    expenses_list = []

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Clean and type-cast the Amount from string to float
                    amount_value = float(row.get("Amount", 0.0))
                    cleaned_record = {
                        "Date": row.get("Date", "").strip(),
                        "Category": row.get("Category", "Other").strip(),
                        "Amount": round(amount_value, 2),
                        "Description": row.get("Description", "").strip(),
                    }
                    expenses_list.append(cleaned_record)
                except ValueError:
                    # Skip corrupted or malformed rows without crashing the application
                    continue
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"File '{filepath}' not found. A new one will be created.")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to load records: {exc}")

    return expenses_list


def save_expenses_to_csv(expenses_list, filepath=DATA_FILE):
    """
    Writes the list of expense dictionaries back into the CSV file.
    Demonstrates: File handling with write mode, CSV DictWriter, Loops.
    """
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Date", "Category", "Amount", "Description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses_list:
                writer.writerow({
                    "Date": expense["Date"],
                    "Category": expense["Category"],
                    "Amount": f"{expense['Amount']:.2f}",
                    "Description": expense["Description"],
                })
        return True
    except IOError as error:
        messagebox.showerror("Save Error", f"Failed to save data: {error}")
        return False


# =============================================================================
# SECTION 2: BUSINESS LOGIC & DATA ANALYSIS (LOOPS, CONDITIONS, MATH)
# =============================================================================

def calculate_summary(expenses_list):
    """
    Calculates summary metrics:
      - Total amount spent
      - Total number of transactions
      - Average spending per transaction
      - Category-wise spending breakdown
      - Highest spending category
    
    Demonstrates: Loops, Conditional Statements, Dictionaries, Arithmetic operations.
    """
    total_spent = 0.0
    category_totals = {category: 0.0 for category in CATEGORIES}

    # Iterate over list of expenses
    for item in expenses_list:
        amount = item["Amount"]
        cat = item["Category"]

        total_spent += amount

        # Track category sum, or classify as 'Other' if unknown
        if cat in category_totals:
            category_totals[cat] += amount
        else:
            category_totals["Other"] = category_totals.get("Other", 0.0) + amount

    total_transactions = len(expenses_list)

    # Calculate average
    if total_transactions > 0:
        average_spent = total_spent / total_transactions
    else:
        average_spent = 0.0

    # Determine highest spending category
    top_category = "None"
    highest_amount = 0.0
    for category, amt in category_totals.items():
        if amt > highest_amount:
            highest_amount = amt
            top_category = category

    return {
        "total_spent": round(total_spent, 2),
        "total_transactions": total_transactions,
        "average_spent": round(average_spent, 2),
        "category_totals": {k: round(v, 2) for k, v in category_totals.items()},
        "top_category": top_category,
        "top_amount": round(highest_amount, 2),
    }


def filter_expenses_by_date(expenses_list, target_date_str):
    """
    Filters the list of expenses matching a specific YYYY-MM-DD date.
    Demonstrates: List comprehension / loops and string comparison.
    """
    filtered = []
    for item in expenses_list:
        if item["Date"] == target_date_str:
            filtered.append(item)
    return filtered


def validate_input(amount_str, category_str, date_str, desc_str):
    """
    Validates form input fields before adding an expense.
    Demonstrates:
      - Type casting (float)
      - Exception handling (try/except ValueError)
      - Date/Time parsing (datetime.strptime)
      - Conditional checks (if/elif/else)
    
    Returns:
        (is_valid: bool, error_message: str, parsed_amount: float)
    """
    # 1. Validate Amount
    if not amount_str.strip():
        return False, "Please enter an amount.", 0.0
    try:
        amount_val = float(amount_str.strip())
        if amount_val <= 0:
            return False, "Amount must be a positive number greater than zero.", 0.0
    except ValueError:
        return False, "Amount must be a valid numeric value (e.g., 250 or 99.50).", 0.0

    # 2. Validate Category
    if not category_str or category_str.strip() == "":
        return False, "Please select an expense category.", 0.0

    # 3. Validate Date format (YYYY-MM-DD)
    if not date_str.strip():
        return False, "Please enter a date.", 0.0
    try:
        datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return False, "Date must follow the format YYYY-MM-DD (e.g., 2026-10-15).", 0.0

    # 4. Validate Description
    if not desc_str.strip():
        return False, "Please enter a brief description for the expense.", 0.0

    return True, "", round(amount_val, 2)


# =============================================================================
# SECTION 3: USER INTERFACE (TKINTER GUI)
# =============================================================================

class ExpenseTrackerApp:
    """
    Main Application Class representing the Expense Tracker GUI.
    Handles user interaction, widget lifecycle, and updates.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("College Mini Project - Expense Tracker")
        self.root.geometry("1120x720")
        self.root.minsize(980, 640)
        self.root.configure(bg=COLOR_BG)

        # In-memory data store
        self.all_expenses = []
        self.currently_displayed = []
        self.is_filtered = False

        # Configure styles
        self.setup_styles()

        # Build GUI Components
        self.create_header()
        self.create_dashboard()
        self.create_main_content()
        self.create_status_bar()

        # Load existing data on startup
        self.refresh_data_from_file()

    def setup_styles(self):
        """Configure modern visual styles for Tkinter ttk widgets."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview styling (Table)
        self.style.configure(
            "Treeview",
            background="#ffffff",
            foreground=COLOR_TEXT_DARK,
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10),
            borderwidth=1,
        )
        self.style.configure(
            "Treeview.Heading",
            background="#e2e8f0",
            foreground=COLOR_TEXT_DARK,
            font=("Segoe UI", 10, "bold"),
            padding=(6, 6),
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#1e3a8a")],
        )

        # Combobox styling
        self.style.configure(
            "TCombobox",
            padding=4,
            font=("Segoe UI", 10),
        )

    # -------------------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------------------
    def create_header(self):
        """Top banner showing project title and student info."""
        header_frame = tk.Frame(self.root, bg=COLOR_HEADER_BG, height=65)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="💰 Student Expense Tracker",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_HEADER_BG,
            fg=COLOR_HEADER_TEXT,
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=12)

        subtitle_label = tk.Label(
            header_frame,
            text="Python Mini Project • CSV Data Storage",
            font=("Segoe UI", 10, "italic"),
            bg=COLOR_HEADER_BG,
            fg="#94a3b8",
        )
        subtitle_label.pack(side=tk.RIGHT, padx=20, pady=16)

    # -------------------------------------------------------------------------
    # DASHBOARD METRIC CARDS
    # -------------------------------------------------------------------------
    def create_dashboard(self):
        """Horizontal row of summary cards: Total Spent, Total Transactions, Top Category, Average."""
        dash_frame = tk.Frame(self.root, bg=COLOR_BG)
        dash_frame.pack(fill=tk.X, padx=20, pady=(15, 5))

        dash_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="dash_card")

        # Card 1: Total Spending
        self.card_total_var = tk.StringVar(value=f"{CURRENCY} 0.00")
        self.build_metric_card(
            dash_frame, 0, "Total Spending", self.card_total_var, "#2563eb", "💳"
        )

        # Card 2: Total Transactions
        self.card_tx_var = tk.StringVar(value="0")
        self.build_metric_card(
            dash_frame, 1, "Total Transactions", self.card_tx_var, "#059669", "📝"
        )

        # Card 3: Top Category
        self.card_top_var = tk.StringVar(value="None")
        self.build_metric_card(
            dash_frame, 2, "Highest Category", self.card_top_var, "#d97706", "🏷️"
        )

        # Card 4: Average Expense
        self.card_avg_var = tk.StringVar(value=f"{CURRENCY} 0.00")
        self.build_metric_card(
            dash_frame, 3, "Average / Expense", self.card_avg_var, "#7c3aed", "📊"
        )

    def build_metric_card(self, parent, col, title, value_var, accent_color, icon):
        """Helper to construct a polished card widget."""
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")

        # Accent color strip on left
        strip = tk.Frame(card, bg=accent_color, width=5)
        strip.pack(side=tk.LEFT, fill=tk.Y)

        inner = tk.Frame(card, bg=COLOR_CARD_BG)
        inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=10)

        header_row = tk.Frame(inner, bg=COLOR_CARD_BG)
        header_row.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_row,
            text=f"{icon} {title}",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD_BG,
        )
        title_lbl.pack(side=tk.LEFT)

        value_lbl = tk.Label(
            inner,
            textvariable=value_var,
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_DARK,
            bg=COLOR_CARD_BG,
        )
        value_lbl.pack(anchor="w", pady=(4, 0))

    # -------------------------------------------------------------------------
    # MAIN CONTENT (ENTRY FORM + TABLE + ACTION BAR)
    # -------------------------------------------------------------------------
    def create_main_content(self):
        """Creates the two-column layout: Form on Left, Table and Controls on Right."""
        content_frame = tk.Frame(self.root, bg=COLOR_BG)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left Column: Add Expense Form (width ~ 340px)
        left_panel = tk.Frame(
            content_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            width=340,
        )
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        self.build_form(left_panel)

        # Right Column: Filter Bar + Table + Delete Button
        right_panel = tk.Frame(content_frame, bg=COLOR_BG)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_filter_bar(right_panel)
        self.build_table(right_panel)
        self.build_table_actions(right_panel)

    def build_form(self, parent):
        """Constructs the expense input form."""
        header_lbl = tk.Label(
            parent,
            text="➕ Add New Expense",
            font=("Segoe UI", 13, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        header_lbl.pack(anchor="w", padx=16, pady=(16, 12))

        # Amount
        lbl_amt = tk.Label(
            parent,
            text=f"Amount ({CURRENCY}) *",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        lbl_amt.pack(anchor="w", padx=16, pady=(4, 2))
        self.entry_amount = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            relief="flat",
        )
        self.entry_amount.pack(fill=tk.X, padx=16, ipady=4)
        self.entry_amount.focus()

        # Category Combobox
        lbl_cat = tk.Label(
            parent,
            text="Category *",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        lbl_cat.pack(anchor="w", padx=16, pady=(10, 2))
        self.combo_category = ttk.Combobox(
            parent,
            values=CATEGORIES,
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.combo_category.pack(fill=tk.X, padx=16, ipady=3)
        self.combo_category.set(CATEGORIES[0])  # Default to Food

        # Date
        lbl_date = tk.Label(
            parent,
            text="Date (YYYY-MM-DD) *",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        lbl_date.pack(anchor="w", padx=16, pady=(10, 2))

        date_row = tk.Frame(parent, bg=COLOR_CARD_BG)
        date_row.pack(fill=tk.X, padx=16)

        self.entry_date = tk.Entry(
            date_row,
            font=("Segoe UI", 11),
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            relief="flat",
        )
        self.entry_date.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.set_date_to_today()

        btn_today = tk.Button(
            date_row,
            text="Today",
            font=("Segoe UI", 8, "bold"),
            bg="#e2e8f0",
            fg=COLOR_TEXT_DARK,
            relief="flat",
            cursor="hand2",
            padx=8,
            command=self.set_date_to_today,
        )
        btn_today.pack(side=tk.RIGHT, padx=(6, 0), ipady=2)

        # Description
        lbl_desc = tk.Label(
            parent,
            text="Description *",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(10, 2))
        self.entry_desc = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            relief="flat",
        )
        self.entry_desc.pack(fill=tk.X, padx=16, ipady=4)

        # Form Buttons
        btn_add = tk.Button(
            parent,
            text="✓ Save Expense",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.add_expense,
        )
        btn_add.pack(fill=tk.X, padx=16, pady=(20, 8), ipady=6)

        btn_clear = tk.Button(
            parent,
            text="Clear Form",
            font=("Segoe UI", 9),
            bg="#f8fafc",
            fg=COLOR_TEXT_MUTED,
            relief="flat",
            cursor="hand2",
            command=self.clear_form_inputs,
        )
        btn_clear.pack(fill=tk.X, padx=16, pady=(0, 10), ipady=4)

        # Category Summary Quick Button
        btn_summary = tk.Button(
            parent,
            text="📊 View Category Breakdown",
            font=("Segoe UI", 10, "bold"),
            bg="#0f766e",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.show_category_summary_dialog,
        )
        btn_summary.pack(fill=tk.X, side=tk.BOTTOM, padx=16, pady=16, ipady=6)

    def build_filter_bar(self, parent):
        """Search and filter toolbar above the records table."""
        filter_card = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        filter_card.pack(fill=tk.X, pady=(0, 8))

        lbl_filter = tk.Label(
            filter_card,
            text="📅 Filter by Date:",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_DARK,
        )
        lbl_filter.pack(side=tk.LEFT, padx=(12, 6), pady=8)

        self.entry_filter_date = tk.Entry(
            filter_card,
            font=("Segoe UI", 10),
            width=14,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            relief="flat",
        )
        self.entry_filter_date.pack(side=tk.LEFT, padx=4, ipady=2)
        self.entry_filter_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        btn_filter = tk.Button(
            filter_card,
            text="Apply Filter",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_PRIMARY,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.apply_date_filter,
        )
        btn_filter.pack(side=tk.LEFT, padx=6)

        btn_reset = tk.Button(
            filter_card,
            text="Show All Records",
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            fg=COLOR_TEXT_DARK,
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.reset_filter,
        )
        btn_reset.pack(side=tk.LEFT, padx=4)

        # Record count badge on right
        self.lbl_record_count = tk.Label(
            filter_card,
            text="Showing all records",
            font=("Segoe UI", 9, "italic"),
            bg=COLOR_CARD_BG,
            fg=COLOR_TEXT_MUTED,
        )
        self.lbl_record_count.pack(side=tk.RIGHT, padx=12)

    def build_table(self, parent):
        """Constructs the Treeview table with vertical and horizontal scrollbars."""
        table_frame = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("sno", "date", "category", "description", "amount")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        # Define headings and column widths
        self.tree.heading("sno", text="#", anchor=tk.CENTER)
        self.tree.heading("date", text="Date", anchor=tk.W)
        self.tree.heading("category", text="Category", anchor=tk.W)
        self.tree.heading("description", text="Description", anchor=tk.W)
        self.tree.heading("amount", text=f"Amount ({CURRENCY})", anchor=tk.E)

        self.tree.column("sno", width=45, minwidth=40, anchor=tk.CENTER)
        self.tree.column("date", width=105, minwidth=90, anchor=tk.W)
        self.tree.column("category", width=120, minwidth=100, anchor=tk.W)
        self.tree.column("description", width=300, minwidth=150, anchor=tk.W)
        self.tree.column("amount", width=120, minwidth=100, anchor=tk.E)

        # Alternating row colors
        self.tree.tag_configure("oddrow", background="#f8fafc")
        self.tree.tag_configure("evenrow", background="#ffffff")

        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Grid placement
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def build_table_actions(self, parent):
        """Action buttons beneath the table (Delete Selected, Refresh, Export Info)."""
        actions_frame = tk.Frame(parent, bg=COLOR_BG)
        actions_frame.pack(fill=tk.X, pady=(8, 0))

        btn_delete = tk.Button(
            actions_frame,
            text="🗑️ Delete Selected Expense",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_DANGER,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.delete_selected_expense,
        )
        btn_delete.pack(side=tk.LEFT)

        btn_refresh = tk.Button(
            actions_frame,
            text="🔄 Reload from File",
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            fg=COLOR_TEXT_DARK,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.refresh_data_from_file,
        )
        btn_refresh.pack(side=tk.LEFT, padx=8)

        lbl_hint = tk.Label(
            actions_frame,
            text="Tip: Click a row to select and delete it.",
            font=("Segoe UI", 9),
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
        )
        lbl_hint.pack(side=tk.RIGHT)

    def create_status_bar(self):
        """Bottom status bar indicating file path and program state."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg="#e2e8f0",
            fg=COLOR_TEXT_DARK,
            anchor="w",
            padx=12,
            pady=4,
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # -------------------------------------------------------------------------
    # CORE CONTROLLER ACTIONS & EVENT HANDLERS
    # -------------------------------------------------------------------------
    def set_date_to_today(self):
        """Helper to fill the date input with the current system date."""
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, today_str)

    def clear_form_inputs(self):
        """Clears all input fields on the left form."""
        self.entry_amount.delete(0, tk.END)
        self.combo_category.set(CATEGORIES[0])
        self.set_date_to_today()
        self.entry_desc.delete(0, tk.END)
        self.entry_amount.focus()

    def add_expense(self):
        """
        Handler to validate input, add expense to data list, and persist to CSV.
        Demonstrates: Input validation, Exception handling, List append, File save.
        """
        amount_raw = self.entry_amount.get()
        category_raw = self.combo_category.get()
        date_raw = self.entry_date.get()
        desc_raw = self.entry_desc.get()

        # Validate inputs
        is_valid, error_msg, validated_amount = validate_input(
            amount_raw, category_raw, date_raw, desc_raw
        )

        if not is_valid:
            messagebox.showwarning("Validation Error", error_msg)
            return

        new_record = {
            "Date": date_raw.strip(),
            "Category": category_raw.strip(),
            "Amount": validated_amount,
            "Description": desc_raw.strip(),
        }

        # Append to our in-memory data
        self.all_expenses.append(new_record)

        # Save to CSV file
        if save_expenses_to_csv(self.all_expenses, DATA_FILE):
            self.clear_form_inputs()
            self.update_ui_after_data_change()
            self.status_var.set(
                f"Expense of {CURRENCY} {validated_amount:.2f} ({new_record['Category']}) added successfully."
            )
            messagebox.showinfo("Success", "Expense recorded and saved to file!")

    def delete_selected_expense(self):
        """
        Deletes the currently selected row in the Treeview table.
        Demonstrates: Treeview selection handling, List element removal, CSV overwrite.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please click on a row in the table to select it for deletion.")
            return

        # Confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete the selected expense record?\nThis action cannot be undone.",
        )
        if not confirm:
            return

        # Retrieve row values
        row_values = self.tree.item(selected_item[0], "values")
        # row_values = (sno, date, category, description, amount)
        selected_date = str(row_values[1])
        selected_cat = str(row_values[2])
        selected_desc = str(row_values[3])
        # Clean amount string (remove currency symbol and commas)
        selected_amt_str = str(row_values[4]).replace(CURRENCY, "").replace(",", "").strip()

        try:
            target_amt = float(selected_amt_str)
        except ValueError:
            target_amt = -1.0

        # Find and delete matching entry from self.all_expenses
        deleted = False
        for idx, item in enumerate(self.all_expenses):
            if (
                item["Date"] == selected_date
                and item["Category"] == selected_cat
                and item["Description"] == selected_desc
                and abs(item["Amount"] - target_amt) < 0.01
            ):
                del self.all_expenses[idx]
                deleted = True
                break

        if deleted:
            save_expenses_to_csv(self.all_expenses, DATA_FILE)
            self.update_ui_after_data_change()
            self.status_var.set("Expense record deleted successfully.")
            messagebox.showinfo("Deleted", "Selected expense record has been removed.")
        else:
            messagebox.showerror("Error", "Could not locate matching record in file.")

    def apply_date_filter(self):
        """Filters the table to show records for the entered date only."""
        target_date = self.entry_filter_date.get().strip()
        if not target_date:
            messagebox.showwarning("Input Error", "Please enter a valid date in YYYY-MM-DD format to filter.")
            return

        try:
            datetime.datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Date Format Error", "Filter date must follow YYYY-MM-DD (e.g., 2026-10-15).")
            return

        filtered = filter_expenses_by_date(self.all_expenses, target_date)
        self.currently_displayed = filtered
        self.is_filtered = True

        self.populate_treeview(self.currently_displayed)
        self.update_dashboard_metrics(self.currently_displayed)

        self.lbl_record_count.config(
            text=f"Filtered: {len(filtered)} record(s) on {target_date}",
            fg="#b45309",
        )
        self.status_var.set(f"Showing {len(filtered)} expense(s) for {target_date}.")

    def reset_filter(self):
        """Clears any active date filter and displays the full dataset."""
        self.is_filtered = False
        self.currently_displayed = list(self.all_expenses)
        self.populate_treeview(self.currently_displayed)
        self.update_dashboard_metrics(self.all_expenses)
        self.lbl_record_count.config(
            text=f"Showing all {len(self.all_expenses)} record(s)",
            fg=COLOR_TEXT_MUTED,
        )
        self.status_var.set("Filter cleared. Displaying all expenses.")

    def refresh_data_from_file(self):
        """Loads data from CSV file and refreshes table and summary cards."""
        self.all_expenses = load_expenses_from_csv(DATA_FILE)
        self.reset_filter()
        self.status_var.set(f"Loaded {len(self.all_expenses)} records from '{DATA_FILE}'.")

    def update_ui_after_data_change(self):
        """Synchronizes table and dashboard after an addition or deletion."""
        if self.is_filtered:
            # Re-apply filter with updated dataset
            self.apply_date_filter()
        else:
            self.reset_filter()

    # -------------------------------------------------------------------------
    # RENDERING DATA TO TABLE & DASHBOARD
    # -------------------------------------------------------------------------
    def populate_treeview(self, records):
        """Populates the Treeview table with the given list of records."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new rows
        for index, exp in enumerate(records, start=1):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    exp["Date"],
                    exp["Category"],
                    exp["Description"],
                    f"{CURRENCY} {exp['Amount']:,.2f}",
                ),
                tags=(tag,),
            )

    def update_dashboard_metrics(self, data_subset):
        """Calculates and updates metric card values."""
        summary = calculate_summary(data_subset)

        self.card_total_var.set(f"{CURRENCY} {summary['total_spent']:,.2f}")
        self.card_tx_var.set(str(summary["total_transactions"]))
        
        if summary["top_category"] != "None":
            self.card_top_var.set(f"{summary['top_category']} ({CURRENCY}{summary['top_amount']:,.0f})")
        else:
            self.card_top_var.set("None")

        self.card_avg_var.set(f"{CURRENCY} {summary['average_spent']:,.2f}")

    # -------------------------------------------------------------------------
    # CATEGORY BREAKDOWN MODAL DIALOG
    # -------------------------------------------------------------------------
    def show_category_summary_dialog(self):
        """
        Opens a clean modal window showing total spending per category,
        with percentage breakdown and visual bar indicators.
        Demonstrates: Secondary windows (Toplevel), loops, formatting.
        """
        summary = calculate_summary(self.all_expenses)
        total_spent = summary["total_spent"]
        cat_totals = summary["category_totals"]

        # Create top-level modal
        dialog = tk.Toplevel(self.root)
        dialog.title("Category-wise Spending Summary")
        dialog.geometry("520x480")
        dialog.minsize(480, 420)
        dialog.configure(bg=COLOR_BG)
        dialog.transient(self.root)
        dialog.grab_set()

        # Dialog Header
        dlg_header = tk.Frame(dialog, bg=COLOR_HEADER_BG, height=50)
        dlg_header.pack(fill=tk.X)
        lbl_head = tk.Label(
            dlg_header,
            text="📊 Spending Breakdown by Category",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_HEADER_BG,
            fg="#ffffff",
        )
        lbl_head.pack(padx=16, pady=12, anchor="w")

        # Total spending badge
        info_frame = tk.Frame(dialog, bg=COLOR_BG)
        info_frame.pack(fill=tk.X, padx=16, pady=(12, 6))

        tk.Label(
            info_frame,
            text=f"Overall Expenditure: {CURRENCY} {total_spent:,.2f}",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_BG,
            fg=COLOR_TEXT_DARK,
        ).pack(side=tk.LEFT)

        # Card container for category rows
        card = tk.Frame(
            dialog,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        card.pack(fill=tk.BOTH, expand=True, padx=16, pady=10)

        # Table header
        th = tk.Frame(card, bg="#e2e8f0")
        th.pack(fill=tk.X)
        tk.Label(th, text="Category", font=("Segoe UI", 9, "bold"), width=15, anchor="w", bg="#e2e8f0").pack(side=tk.LEFT, padx=12, pady=6)
        tk.Label(th, text="Spent", font=("Segoe UI", 9, "bold"), width=14, anchor="e", bg="#e2e8f0").pack(side=tk.LEFT, padx=6)
        tk.Label(th, text="% Share", font=("Segoe UI", 9, "bold"), width=10, anchor="e", bg="#e2e8f0").pack(side=tk.LEFT, padx=6)
        tk.Label(th, text="Distribution", font=("Segoe UI", 9, "bold"), width=16, anchor="w", bg="#e2e8f0").pack(side=tk.LEFT, padx=6)

        # Scrollable container for category rows
        scroll_container = tk.Frame(card, bg=COLOR_CARD_BG)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Sort categories by spending descending
        sorted_cats = sorted(cat_totals.items(), key=lambda item: item[1], reverse=True)

        for cat_name, amt in sorted_cats:
            row_frame = tk.Frame(scroll_container, bg=COLOR_CARD_BG)
            row_frame.pack(fill=tk.X, pady=3)

            percentage = (amt / total_spent * 100) if total_spent > 0 else 0.0

            # Category name
            tk.Label(
                row_frame,
                text=cat_name,
                font=("Segoe UI", 9, "bold" if amt > 0 else "normal"),
                width=15,
                anchor="w",
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_DARK if amt > 0 else COLOR_TEXT_MUTED,
            ).pack(side=tk.LEFT, padx=12)

            # Amount
            tk.Label(
                row_frame,
                text=f"{CURRENCY} {amt:,.2f}",
                font=("Segoe UI", 9),
                width=14,
                anchor="e",
                bg=COLOR_CARD_BG,
                fg=COLOR_PRIMARY if amt > 0 else COLOR_TEXT_MUTED,
            ).pack(side=tk.LEFT, padx=6)

            # Percentage
            tk.Label(
                row_frame,
                text=f"{percentage:5.1f}%",
                font=("Segoe UI", 9),
                width=10,
                anchor="e",
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_DARK if amt > 0 else COLOR_TEXT_MUTED,
            ).pack(side=tk.LEFT, padx=6)

            # Visual progress bar
            bar_container = tk.Frame(row_frame, bg="#e2e8f0", width=110, height=12)
            bar_container.pack(side=tk.LEFT, padx=10)
            bar_container.pack_propagate(False)

            fill_width = int(percentage * 1.1)  # scale to 110px width
            if fill_width > 0:
                bar_fill = tk.Frame(bar_container, bg="#059669", width=fill_width)
                bar_fill.pack(side=tk.LEFT, fill=tk.Y)

        # Close button
        btn_close = tk.Button(
            dialog,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=dialog.destroy,
        )
        btn_close.pack(pady=(0, 14), ipadx=20, ipady=4)


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================
def main():
    """
    Program execution starts here.
    Initializes Tkinter root window and launches application loop.
    """
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

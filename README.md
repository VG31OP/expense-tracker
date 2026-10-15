# 💰 Python Mini Project: Expense Tracker

A clean, modern, beginner-friendly desktop **Expense Tracker Application** built in Python with **Tkinter** and **CSV file storage**. Developed for college Problem-Based Learning (PBL) and practical examinations.

---

## 🌟 Key Features

1. **Dashboard Overview**:
   - **Total Spending Card** with formatted currency (`₹` / `$`).
   - **Transaction Counter** showing total entries recorded.
   - **Top Category Badge** displaying where most money was spent.
   - **Average Expenditure** per transaction.

2. **Add Expense Form**:
   - Validates numeric input (rejects letters, negative amounts, and zero).
   - Dropdown selection for standard categories (*Food, Travel, Shopping, Education, Bills, Entertainment, Healthcare, Other*).
   - Date picker with automatic **Today** shortcut button and `YYYY-MM-DD` validation.
   - Expense description field.

3. **View & Manage Expenses Table**:
   - Built using `ttk.Treeview` with alternating row colors.
   - Vertical and horizontal scrollbars for smooth browsing.
   - Click-to-select and delete unwanted records with confirmation dialog.

4. **Category-wise Spending Breakdown**:
   - Dedicated modal showing total spent per category.
   - Percentage share calculation.
   - Visual progress bars representing spending distribution.

5. **Date Filter**:
   - Filter records by any specified date (`YYYY-MM-DD`).
   - Real-time filtered statistics.
   - "Show All Records" button to quickly restore full dataset.

6. **Persistent Storage (CSV)**:
   - Records are automatically saved to `expenses.csv`.
   - Data persists across application restarts without requiring external databases or paid APIs.

---

## 📂 Project Structure

```text
py pbl/
├── main.py              # Main Python script with GUI and business logic
├── expenses.csv         # CSV file storing expense records permanently
├── README.md            # Setup, execution, and user guide
└── PROJECT_REPORT.md    # College mini project documentation & viva guide
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.8 or higher installed on your computer.
- **No external third-party packages required** (uses standard libraries: `tkinter`, `csv`, `datetime`, `os`).

### Step-by-Step Instructions

1. **Open Terminal / Command Prompt** in the project folder:
   ```bash
   cd "e:\Project\py pbl"
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```
   *(Or double-click `main.py` in Windows File Explorer)*

3. **Demonstrating Features during Practical Exam**:
   - **Add an Expense**: Enter Amount (e.g. `250`), select Category (`Food`), click `Today`, type Description (`Lunch with friends`), and click **Save Expense**.
   - **View Table**: Notice the new record instantly appears at the bottom with updated dashboard counters.
   - **Category Summary**: Click **"📊 View Category Breakdown"** on the left to show the modal popup with percentage bars.
   - **Filter by Date**: Enter a date (e.g., `2026-10-15`) in the top bar and click **Apply Filter**. Click **Show All Records** to reset.
   - **Delete Record**: Click any row in the table, then click **"🗑️ Delete Selected Expense"** and confirm.
   - **Data Persistence**: Close the application and reopen it using `python main.py`; verify that all records remain intact in `expenses.csv`.

---

## 🐍 Python Concepts Demonstrated

| Concept | Implementation in Code |
| :--- | :--- |
| **Variables & Data Types** | `float` for amounts, `str` for descriptions/dates, `int` for counters |
| **Conditionals** | `if`, `elif`, `else` for input validation and filter matching |
| **Loops** | `for` loops in CSV parsing, metric summation, and table population |
| **Functions** | Modular architecture (`initialize_csv`, `calculate_summary`, `validate_input`) |
| **Lists & Dictionaries** | List of dictionaries `[{'Date': ..., 'Category': ..., 'Amount': ...}]` |
| **Exception Handling** | `try / except ValueError`, `FileNotFoundError`, `IOError` |
| **File Handling & CSV** | `csv.DictReader` and `csv.DictWriter` with file context manager (`with open(...)`) |
| **Date & Time** | `datetime.date.today()` and `datetime.datetime.strptime()` for validation |
| **GUI Programming** | Tkinter widgets (`Tk`, `Frame`, `Label`, `Entry`, `Button`, `ttk.Treeview`, `ttk.Combobox`) |

---

## 📄 College Project Submission
A complete, structured project report is provided in [PROJECT_REPORT.md](file:///e:/Project/py%20pbl/PROJECT_REPORT.md).

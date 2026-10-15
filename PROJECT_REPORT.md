# Mini Project Report

## Project Title: Desktop Expense Tracker Application in Python
**Course:** Problem-Based Learning (PBL) / Python Programming Laboratory  
**Technology:** Python 3, Tkinter GUI, CSV File Storage, Datetime Module  

---

## 1. Introduction

Managing daily expenditures is an essential skill for individuals, particularly students living on a budget. Traditional manual expense recording in notebooks or physical receipts is prone to loss, calculation errors, and lack of visual insight into spending patterns.

The **Desktop Expense Tracker Application** is an interactive, standalone software system developed in Python. It offers a graphical user interface (GUI) designed to facilitate recording, categorizing, viewing, filtering, and summarizing day-to-day personal expenses. By leveraging lightweight, comma-separated values (CSV) storage, the application ensures data persistence without requiring heavy database servers, external network connections, or subscription services.

---

## 2. Objectives

The primary objectives of this project are:
1. **Accurate Record Keeping:** Provide a simple interface to log expenditure with date, category, amount, and description.
2. **Data Persistence:** Store entries in a standard CSV format so that information is retained across sessions.
3. **Automated Analytics:** Compute aggregate metrics including total amount spent, transaction count, average spending, and top spending category in real time.
4. **Categorical Insights:** Present category-wise spending totals with percentage share and visual distribution bars.
5. **Search & Filter:** Allow users to filter expenditures by specific calendar dates.
6. **Input Integrity:** Enforce robust validation to eliminate negative figures, non-numeric values, missing fields, and incorrect date formats.
7. **Educational Demonstration:** Apply core Python concepts (data structures, loops, functions, file I/O, exception handling, and GUI development) in a unified project.

---

## 3. Methodology & System Architecture

### 3.1 Architectural Overview
The application follows a modular, three-tier desktop architecture:

```
+-------------------------------------------------------------+
|                 PRESENTATION TIER (Tkinter GUI)             |
|  - Dashboard Metric Cards    - Input Form                   |
|  - ttk.Treeview Table Records - Category Modal Dialog        |
|  - Date Filter Toolbar       - Status Bar                   |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               BUSINESS LOGIC & VALIDATION TIER               |
|  - Input Validation (validate_input)                        |
|  - Statistical Calculations (calculate_summary)              |
|  - Date Filtering (filter_expenses_by_date)                 |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  DATA STORAGE TIER (CSV I/O)                 |
|  - File Initializer (initialize_csv)                        |
|  - File Reader (load_expenses_from_csv using DictReader)     |
|  - File Writer (save_expenses_to_csv using DictWriter)       |
+-------------------------------------------------------------+
```

### 3.2 Data Flow
1. **Initialization:** On startup, the program calls `initialize_csv()` to ensure `expenses.csv` exists, followed by `load_expenses_from_csv()` which populates an in-memory list of dictionaries.
2. **Dashboard Update:** The in-memory data is passed to `calculate_summary()` which computes aggregates and updates Tkinter StringVars attached to the metric cards.
3. **Table Population:** Records are injected row-by-row into a `ttk.Treeview` with alternating row background colors.
4. **Expense Addition:** When a user submits the form, `validate_input()` checks each field. If valid, a new dictionary is appended to the data list and saved immediately to `expenses.csv`.
5. **Expense Deletion:** When a user selects a table row and confirms deletion, the matching record is removed from the memory list and the CSV file is rewritten.

---

## 4. Features & Module Description

| Module / Feature | Function in Code | Description |
| :--- | :--- | :--- |
| **Add Expense** | `add_expense()` | Captures amount, category, date, and description; validates them, appends to the dataset, and persists to disk. |
| **View Table** | `populate_treeview()` | Displays records in an organized table format with columns for S.No, Date, Category, Description, and Amount. |
| **Delete Record** | `delete_selected_expense()` | Deletes the selected row with an alert confirmation to prevent accidental loss. |
| **Summary Dashboard** | `update_dashboard_metrics()` | Displays 4 dynamic cards: Total Spending, Total Transactions, Top Spending Category, and Average Expense. |
| **Category Breakdown**| `show_category_summary_dialog()` | Displays a secondary dialog (`Toplevel`) with exact expenditure per category, percentage share, and visual progress bars. |
| **Date Filter** | `apply_date_filter()`, `reset_filter()` | Filters the table to only show expenses incurred on a user-specified date (`YYYY-MM-DD`). |
| **File Handling** | `load_expenses_from_csv()`, `save_expenses_to_csv()` | Reads and writes tabular data to `expenses.csv` using Python's standard `csv` module. |

---

## 5. Python Concepts Demonstrated

### 5.1 Variables & Data Types
- **Floats:** Used for monetary amounts (`amount = float(amount_str)`).
- **Strings:** Used for descriptions, dates, and category classifications.
- **Integers:** Used for transaction indexing and loop counters.
- **Booleans:** Used for validation flags (`is_valid, is_filtered`).

### 5.2 Conditional Statements (`if`, `elif`, `else`)
Conditional logic controls data validation, category mapping, and empty-dataset handling:
```python
if not amount_str.strip():
    return False, "Please enter an amount.", 0.0
elif float(amount_str) <= 0:
    return False, "Amount must be a positive number greater than zero.", 0.0
```

### 5.3 Loops (`for` loops)
Iterates through collections for summing expenses, populating tables, and filtering:
```python
for item in expenses_list:
    total_spent += item["Amount"]
    cat = item["Category"]
    category_totals[cat] = category_totals.get(cat, 0.0) + item["Amount"]
```

### 5.4 Functions & Modularity
Code is divided into cohesive, single-purpose functions:
- `validate_input(...)`
- `calculate_summary(...)`
- `load_expenses_from_csv(...)`
- `save_expenses_to_csv(...)`

### 5.5 Lists & Dictionaries
All records are managed as a list of dictionaries, a standard Python idiom for tabular data:
```python
cleaned_record = {
    "Date": "2026-10-15",
    "Category": "Food",
    "Amount": 250.00,
    "Description": "College Lunch",
}
expenses_list.append(cleaned_record)
```

### 5.6 Exception Handling (`try...except`)
Guards against application crashes due to unexpected user inputs or I/O errors:
```python
try:
    datetime.datetime.strptime(date_str, "%Y-%m-%d")
except ValueError:
    return False, "Date must follow YYYY-MM-DD.", 0.0
```

### 5.7 File I/O with Context Managers
Utilizes `with open(...)` to guarantee that file descriptors are automatically closed, preventing memory leaks:
```python
with open(filepath, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        ...
```

---

## 6. User Interface Design & Layout

The user interface is built using standard `tkinter` and `tkinter.ttk`:
1. **Header Banner:** Displays project title and metadata in Slate Navy (`#1e293b`).
2. **Dashboard Cards:** 4 high-contrast cards highlighting key metrics with distinct color accents (Blue, Green, Amber, Violet).
3. **Form Panel (Left):** Input fields with a "Today" shortcut button and a "Clear Form" reset button.
4. **Table View (Right):** A styled `Treeview` table with alternating row colors (`#f8fafc` and `#ffffff`) and integrated scrollbars.
5. **Filter Toolbar (Top-Right):** Quick date filter input box with "Apply Filter" and "Show All Records" buttons.
6. **Category Modal Dialog:** Pop-up window displaying category breakdown with custom progress bars.

---

## 7. Test Cases & Verification

| Test Case ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Valid expense addition | Amount: `450`, Cat: `Food`, Date: `2026-10-15`, Desc: `Snacks` | Expense added to table, saved to CSV, dashboard updated | Success dialog shown, table updated | **PASS** |
| **TC-02** | Non-numeric amount | Amount: `abc` | Error message dialog | Validation rejected with prompt | **PASS** |
| **TC-03** | Negative amount | Amount: `-100` | Error message dialog | Validation rejected ("Must be positive") | **PASS** |
| **TC-04** | Invalid date format | Date: `15/10/2026` | Error message dialog | Validation rejected ("Follow YYYY-MM-DD") | **PASS** |
| **TC-05** | Empty description | Desc: `""` | Error message dialog | Prompted to provide description | **PASS** |
| **TC-06** | Delete expense | Row selected in table | Row removed from table and CSV | Prompted for confirmation, then removed | **PASS** |
| **TC-07** | Filter by date | Date: `2026-10-15` | Shows only matching records | 1 record displayed, metrics reflect filtered subset | **PASS** |
| **TC-08** | Data persistence | Restart application | Records load from `expenses.csv` | All previous records present | **PASS** |

---

## 8. Conclusion & Future Enhancements

### 8.1 Conclusion
The **Expense Tracker Application** successfully fulfills all project requirements. It provides an intuitive, reliable desktop solution for recording, managing, and analyzing daily financial transactions. By relying exclusively on built-in Python libraries (`tkinter`, `csv`, `datetime`, `os`), the project runs seamlessly across Windows, macOS, and Linux without installation overhead.

### 8.2 Future Scope
Potential improvements for future iterations include:
- Generating visual spending graphs (pie charts, bar charts) using `matplotlib`.
- Monthly budget alert notifications when category spending exceeds a preset threshold.
- Exporting formatted summary reports to PDF or Excel formats.
- Password-protected multi-user profile support.

---

## 9. Viva Voce / Practical Examination Q&A

**Q1: Why was CSV chosen over SQLite or MySQL for this project?**  
*Answer:* CSV was chosen because it is lightweight, human-readable, requires no server or third-party database drivers, and directly demonstrates Python file handling (`open`, `csv.DictReader`, `csv.DictWriter`).

**Q2: How does the application handle invalid user inputs?**  
*Answer:* The `validate_input()` function implements input validation using conditional checks and exception handling (`try-except ValueError`). If an invalid number or date format is submitted, the system halts processing and displays an informative `messagebox.showwarning` dialog without crashing.

**Q3: How does the application ensure data is saved when restarted?**  
*Answer:* Every time an expense is added or deleted, the in-memory list of expenses is immediately synchronized to disk by rewriting `expenses.csv`. Upon startup, `load_expenses_from_csv()` reads the file into memory.

**Q4: Which Tkinter widget is used to render the table?**  
*Answer:* `ttk.Treeview` with defined column headings, cell alignments, and scrollbars.

**Q5: How is category-wise distribution calculated?**  
*Answer:* A Python dictionary `category_totals` initializes all categories with `0.0`. A `for` loop iterates through each expense dictionary, incrementing the corresponding category value. Percentages are derived by dividing each category total by the overall expenditure.

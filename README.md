# FinTrack Pro - Smart Personal Finance Dashboard

## Demo Account

For evaluation purposes, a demo account has been provided.

**Email:** `sasi@test.com`

**Password:** `123456`



## Project Overview

FinTrack Pro is a Smart Personal Finance Dashboard developed using Python, Streamlit, and SQLite. The application helps users manage their personal finances by tracking income and expenses, setting monthly budgets, viewing financial analytics, and generating detailed reports.

This project was developed as part of the Advanced Programming course for the Bachelor of Information Technology programme.

---

## Features

### User Authentication
- User Registration
- Secure Login
- Logout
- Password hashing
- Session management

### Dashboard
- Financial overview
- Total income
- Total expenses
- Current balance
- Monthly savings summary
- Financial health indicators

### Transaction Management
- Add income transactions
- Add expense transactions
- Edit existing transactions
- Delete transactions
- Search transactions
- Filter by:
  - Year
  - Month
  - Category
  - Transaction Type

### Budget Management
- Create monthly budgets
- Multiple expense categories
- Budget vs Actual spending
- Budget progress tracking

### Financial Analytics
- Income vs Expense analysis
- Monthly trends
- Category breakdown
- Yearly comparisons
- Interactive charts and graphs

### Reports
- Generate financial reports
- Export to:
  - PDF
  - Excel (.xlsx)
  - CSV

### Additional Features
- Dark Mode interface
- Responsive dashboard
- Five years of financial data (2022–2026)
- Import CSV transactions
- Modern user interface

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Main Programming Language |
| Streamlit | Web Application Framework |
| SQLite | Database |
| Pandas | Data Processing |
| Plotly | Interactive Charts |
| OpenPyXL | Excel Export |
| ReportLab | PDF Report Generation |
| hashlib | Password Encryption |

---

## Project Structure

```
FinTrack Pro
│
├── app.py
├── database/
│   ├── database.py
│   └── finance.db
│
├── pages/
│   ├── Login
│   ├── Register
│   ├── Dashboard
│   ├── Transactions
│   ├── Budget
│   ├── Analytics
│   └── Reports
│
├── utils/
│
├── assets/
│
├── screenshots/
│
├── reports/
│
└── requirements.txt
```

---

## Installation Guide

### 1. Clone or Download the Project

Download the project folder and extract it.

### 2. Install Python

Install Python 3.10 or newer.

Download:
https://www.python.org/downloads/

---

### 3. Install Required Packages

Open Command Prompt or Terminal.

Navigate to the project folder.

Run:

```
pip install -r requirements.txt
```

---

### 4. Start the Application

Run:

```
streamlit run app.py
```

The application will automatically open in your browser.

Usually at:

```
http://localhost:8501
```

---

## Database

The application uses SQLite.

Database file:

```
database/finance.db
```

The database stores:

- Users
- Transactions
- Budgets

---

## Default Workflow

1. Register a new account
2. Login
3. Add income transactions
4. Add expense transactions
5. Create monthly budgets
6. View dashboard
7. Explore analytics
8. Export reports

---

## Sample Data

This project includes financial records from:

- 2022
- 2023
- 2024
- 2025
- 2026

This allows the Analytics and Reports modules to demonstrate realistic multi-year financial trends.

---

## Reports Generated

The application can generate:

- Financial_Report.pdf
- transactions.csv
- transactions.xlsx

Reports are saved inside the reports folder.

---

## Screenshots

The project includes screenshots for:

- Home Page
- Login
- Register
- Dashboard
- Transactions
- Budget
- Analytics
- Reports

---

## Future Improvements

Possible future enhancements include:

- Email verification
- Bank API integration
- Mobile application
- Cloud database
- AI spending predictions
- Receipt image scanning
- Multi-user collaboration
- Automatic recurring transactions

---

## Author

Sasindran A/L R Paniksalvam

Bachelor of Information Technology

Advanced Programming Project

2026

---

## License

This project is developed for educational purposes only.
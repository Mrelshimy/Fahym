# Fahym - Financial Transactions Control App

## Introduction
Fahym is a financial transaction management app designed to provide users with insights into their financial performance. The app allows users to track, manage, and analyze financial data efficiently.

## Features
- **User Registration and Authentication**: Secure registration and login with form validation.
- **Financial Dashboard**: Overview of financial performance and transactions.
- **Sales Invoices**: Add and manage sales invoices.
- **Sales Invoices**: Add and manage purchase invoices.
- **Customers**: Add and manage customers.
- **Suppliers**: Add and manage suppliers.
- **Items**: Add and manage items.
- **Investments**: Add and manage investments.

## Installation

### Prerequisites
- Python 3.x
- Flask

### Clone the Repository
```bash
git clone https://github.com/mrelshimy/fahym.git
cd fahym
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run APP
```bash
python3 run.py
```

## Usage
1. Register a new account or log in with an existing account.
2. Navigate through the dashboard to manage your financial transactions.
3. Add and view invoices, business partners and investments.
4. Analyze financial performance with the provided insights.

## Project Structure
```plaintext
fahym/
│
├── app/                # Contains the main Flask application code
│   ├── __init__.py     # Application factory
|   ├── api/            # API Files
│   ├── routes.py       # Routes for the application
│   ├── models.py       # Database models
│   ├── forms.py        # Flask-WTF forms
|   ├── static/         # Static files (CSS, JavaScript, images)
│   └── templates/      # HTML templates
│
├── config.py           # Configuration settings
│
├── requirements.txt    # List of Python dependencies
│
└── README.md           # Project documentation (This file)
```

## Contact
If you have any questions or suggestions, feel free to reach out:

- **Email**: mraafat.elsayed@gmail.com
- **GitHub**: Mrelshimy

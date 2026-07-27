# Entity Relationship Diagram (ERD)

## Table 1 : Users

- user_id (Primary Key)
- full_name
- email
- password

↓

One user can have many transactions.

--------------------------------------------

## Table 2 : Transactions

- transaction_id (Primary Key)
- user_id (Foreign Key)
- transaction_date
- description
- category
- transaction_type
- amount

↓

Each transaction belongs to one category.

--------------------------------------------

## Table 3 : Categories

- category_id (Primary Key)
- category_name

↓

Categories are used by Transactions.

--------------------------------------------

## Table 4 : Budgets

- budget_id (Primary Key)
- category
- monthly_limit

↓

Each category can have one monthly budget.

--------------------------------------------

## Table 5 : Import Logs

- import_id (Primary Key)
- filename
- imported_date
- records

↓

Stores every imported CSV file.
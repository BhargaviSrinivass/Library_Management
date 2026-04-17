Library Management System
A Python-based CLI application to manage library operations, including book inventory, borrower records, and transaction tracking using MySQL.

🚀 Features
Book Management: Add, search (by title, ISBN, author, or genre), update status, and delete books.

Borrower Management: Register new members, view member lists, and remove members.

Transaction Handling: Issue books with automatic due-date calculation (14 days) and return books with stock updates.

Audit Logs: View all transaction histories including issue and return dates.

🛠️ Prerequisites
Python 3.x

MySQL Server

PyMySQL Library: Install via pip:

Bash
pip install pymysql
📂 Database Setup
Create a database named lib.

Run the following SQL commands to set up the required tables:

SQL
CREATE TABLE books (
    ISBN BIGINT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Genre VARCHAR(100),
    Copies INT,
    Status CHAR(1) DEFAULT 'N'
);

CREATE TABLE borrower (
    BID INT PRIMARY KEY,
    BName VARCHAR(255),
    BNo VARCHAR(15)
);

CREATE TABLE transacts (
    TID INT AUTO_INCREMENT PRIMARY KEY,
    BID INT,
    ISBN BIGINT,
    IssueDate DATE,
    DueDate DATE,
    ReturnDate DATE,
    Fine INT DEFAULT 0,
    FOREIGN KEY (BID) REFERENCES borrower(BID),
    FOREIGN KEY (ISBN) REFERENCES books(ISBN)
);
📊 Database Architecture
Table Relationships
The system follows a Relational Database Management System (RDBMS) structure where the transacts table acts as a bridge between books and borrowers.

One-to-Many (Borrower to Transactions): One borrower can have multiple transaction records (issuing different books over time).

One-to-Many (Books to Transactions): One specific ISBN can appear in multiple transaction records.

Data Integrity & Constraints
To ensure data accuracy, the following constraints are applied:

Table	Column	Constraint	Purpose
Books	ISBN	PRIMARY KEY	Ensures every book entry is uniquely identifiable.
Borrower	BID	PRIMARY KEY	Ensures unique identification for each library member.
Transacts	BID	FOREIGN KEY	Ensures a book cannot be issued to a non-existent borrower.
Transacts	ISBN	FOREIGN KEY	Ensures a transaction cannot exist for a book not in the inventory.
Books	Status	DEFAULT 'N'	Standardizes the availability flag ('N' for available, 'Y' for unavailable/restricted).
Potential Improvements for Integrity
Stock Validation: Your code currently checks if Copies > 0 before issuing. To prevent data corruption, you could add a SQL CHECK constraint: ALTER TABLE books ADD CONSTRAINT check_copies CHECK (Copies >= 0);.

Cascading Deletes: Currently, if you delete a borrower who has a transaction history, the database will throw an error. Using ON DELETE CASCADE in the foreign key definition would automatically clean up logs when a user is removed.

SQL Injection: Your search by ISBN and Author uses f-strings (e.g., f"select...where ISBN = {isbno}"). This is a security risk. You should switch these to parameterized queries (using %s) as you did in the "Add Book" section.

🖥️ How to Run
Update the db.connect credentials in the script with your MySQL password.

Run the script:

Bash
python library_management.py

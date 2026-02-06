# Library Management System

A comprehensive Python-based Library Management System with a command-line interface. This system allows librarians to manage books, members, borrowing records, and fines efficiently.

## Features

### 📚 Book Management
- Add new books with details (title, author, ISBN, publication year, category)
- View all books in the library
- Search books by title, author, or ISBN
- Update book information
- Delete books from the library
- Track available quantity of each book

### 👥 Member Management
- Register new library members
- View all members and their details
- Search members by name or email
- Update member information
- Delete members
- Track outstanding fines per member
- View member borrowing history

### 📤 Borrowing Management
- Record book borrowings with customizable duration
- Automatic due date calculation
- Return books with automatic fine calculation
- View all active borrowings
- Identify and manage overdue books
- Prevent borrowing if member has outstanding fines

### 💰 Fine Management
- Automatic fine calculation for overdue books
- View member fines and payment history
- Record fine payments
- Track outstanding library fines
- Prevent new borrowings if outstanding fines exist

### 📊 Reports & Statistics
- Total books and availability statistics
- Member statistics
- Borrowing statistics
- Overdue books report
- Category distribution
- Outstanding fines summary

## Project Structure

```
Library Management System/
├── main.py                 # Main application with CLI interface
├── database.py             # Database initialization and connection
├── models.py               # Data models (Book, Member, BorrowingRecord, Fine)
├── db_operations.py        # Database operations (CRUD operations)
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Requirements

- Python 3.7 or higher
- SQLite3 (usually included with Python)
- No external dependencies required (uses Python standard library only)

## Installation

1. Clone or download the project
2. Navigate to the project directory
3. No additional installation needed - uses SQLite which is built-in

## Usage

### Running the Application

```bash
python main.py
```

This will launch the interactive menu-driven interface.

### Main Menu Options

1. **Book Management** - Add, view, search, update, or delete books
2. **Member Management** - Register, view, update, or delete members
3. **Borrowing Management** - Handle book borrowing and returns
4. **Fine Management** - Track and manage fines
5. **Reports & Statistics** - View library statistics and reports
6. **Exit** - Close the application

### Sample Workflows

#### Adding a Book
1. Select "Book Management" → "Add New Book"
2. Enter book details (title, author, ISBN, publication year, quantity, category)
3. Book is added to the database

#### Registering a Member
1. Select "Member Management" → "Register New Member"
2. Enter member details (name, email, phone, address)
3. Member receives a unique ID

#### Borrowing a Book
1. Select "Borrowing Management" → "Borrow a Book"
2. Enter member ID and book ID
3. Set borrow duration (default: 14 days)
4. Due date is automatically calculated

#### Returning a Book
1. Select "Borrowing Management" → "Return a Book"
2. Enter borrowing ID
3. If overdue, fine is automatically calculated and applied
4. Fine is added to member's outstanding amount

## Database Schema

### books table
- book_id (Primary Key)
- title
- author
- isbn (Unique)
- publication_year
- quantity
- available_quantity
- category
- created_at

### members table
- member_id (Primary Key)
- name
- email (Unique)
- phone
- address
- membership_date
- membership_status
- outstanding_fine

### borrowing table
- borrow_id (Primary Key)
- member_id (Foreign Key)
- book_id (Foreign Key)
- borrow_date
- due_date
- return_date
- status ('borrowed' or 'returned')
- fine_amount

### fines table
- fine_id (Primary Key)
- member_id (Foreign Key)
- borrow_id (Foreign Key)
- amount
- reason
- paid (Boolean)
- created_date

## Features Explained

### Fine System
- Default fine: $1.00 per day (configurable)
- Fine is calculated when a book is returned late
- Fine is automatically added to member's outstanding amount
- Members cannot borrow new books if they have outstanding fines
- Fines can be paid through the Fine Management menu

### Search Functionality
- Books can be searched by title, author, or ISBN
- Members can be searched by name or email
- Partial matching is supported

### Reports
The system provides:
- Total books and quantity statistics
- Member statistics and active member count
- Borrowing activity metrics
- Overdue books list
- Outstanding fines summary
- Book category distribution

## Constraints & Validations

- ISBNs and emails must be unique
- Members cannot borrow if they have outstanding fines
- Books cannot be borrowed if not available
- Dates are automatically managed (no manual date entry needed)
- Fine calculations are automatic

## Future Enhancements

- Email notifications for due dates
- Book reservations
- Renewal of borrowed books
- Member subscription plans
- Advanced reporting and analytics
- GUI interface with Tkinter or PyQt
- Export functionality (CSV, PDF)
- Barcode scanning integration
- Multi-user support with authentication

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, refer to the code comments and docstrings throughout the project.

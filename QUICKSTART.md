# 🏛️ LIBRARY MANAGEMENT SYSTEM - QUICK START GUIDE

## Overview
A full-featured Python library management system with a command-line interface. Manage books, members, borrowing, and fines all in one application.

## Quick Start (5 Minutes)

### 1. Verify Python Installation
```bash
python --version
# Should show Python 3.7 or higher
```

### 2. Initialize Database with Sample Data
```bash
python init_sample_data.py
```
This creates the database and loads 15 sample books and 8 sample members.

### 3. Run the Application
```bash
python main.py
```

### 4. Navigate the Menu
Use the number keys to navigate:
- `1` - Book Management
- `2` - Member Management  
- `3` - Borrowing Management
- `4` - Fine Management
- `5` - Reports & Statistics
- `0` - Exit

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | Main application with interactive CLI menu |
| `database.py` | SQLite database setup and connection |
| `models.py` | Data models (Book, Member, BorrowingRecord, Fine) |
| `db_operations.py` | CRUD operations for all entities |
| `init_sample_data.py` | Populate database with sample data |
| `test_system.py` | Automated tests for all functionality |
| `library.db` | SQLite database (auto-created) |

## Core Features

### 📚 Book Management
```
✓ Add books with ISBN, publication year, category
✓ Search by title, author, or ISBN
✓ Track available quantity
✓ Update book details
✓ Delete books
```

### 👥 Member Management
```
✓ Register members (name, email, phone, address)
✓ Search members
✓ View member details and history
✓ Track outstanding fines
✓ Update member info
```

### 📤 Borrowing System
```
✓ Issue books to members (14-day default)
✓ Automatic due date calculation
✓ Record book returns
✓ View active borrowings
✓ Track overdue books
```

### 💰 Fine Management
```
✓ Automatic fine calculation ($1/day default)
✓ Fine applied when returning overdue books
✓ Prevent borrowing if fines unpaid
✓ Track fine payment history
✓ View outstanding fines
```

## Common Tasks

### Task: Add a Book
1. Select `1` (Book Management)
2. Select `1` (Add New Book)
3. Enter book details
4. Press Enter to confirm

### Task: Register a Member
1. Select `2` (Member Management)
2. Select `1` (Register New Member)
3. Enter member details
4. Receive member ID

### Task: Borrow a Book
1. Select `3` (Borrowing Management)
2. Select `1` (Borrow a Book)
3. Enter Member ID and Book ID
4. Confirm borrow duration (default 14 days)
5. Receive due date

### Task: Return a Book
1. Select `3` (Borrowing Management)
2. Select `2` (Return a Book)
3. Enter Borrowing ID
4. If overdue, fine is calculated automatically
5. Fine added to member's account

## Sample Data Included

### Books (15 total)
- The Great Gatsby, Pride and Prejudice, 1984
- The Hobbit, Harry Potter, Dune, The Lord of the Rings
- Sapiens, Atomic Habits, Educated
- And more!

### Members (8 total)
- John Smith, Mary Johnson, Robert Williams
- Patricia Brown, Michael Davis, Linda Miller
- James Wilson, Barbara Moore

## Database Structure

### Tables
- **books** - Book inventory and availability
- **members** - Member registration and status
- **borrowing** - Lending records and history
- **fines** - Fine records and payment status

All tables include timestamps and maintain referential integrity.

## Testing & Validation

### Run Automated Tests
```bash
python test_system.py
```

Tests verify:
- ✓ Book management operations
- ✓ Member registration and search
- ✓ Borrowing and returns
- ✓ Overdue scenarios
- ✓ Fine calculations

## Troubleshooting

### Issue: "Database already exists"
The database already has data. Run again or delete `library.db` first.

### Issue: "Invalid choice"
Make sure to enter the number corresponding to your selection.

### Issue: Member has outstanding fine
Members cannot borrow books if they have unpaid fines. Use Fine Management to pay.

### Issue: Book not available
A book may be fully borrowed out. Check availability in the book list view.

## System Specifications

- **Language**: Python 3.7+
- **Database**: SQLite3 (built-in)
- **Dependencies**: None (uses Python standard library)
- **File Size**: ~20KB (excluding database)
- **Database Size**: ~50KB (with sample data)

## Features in Detail

### Search Functionality
- Books: Search by title, author, or ISBN (partial matching)
- Members: Search by name or email
- Results show all matching records

### Fine System
- Default: $1.00 per day overdue
- Calculated automatically on return
- Added to member's outstanding balance
- Prevents new borrowing until paid

### Default Settings
- Borrowing duration: 14 days
- Fine rate: $1.00/day
- All customizable during transactions

## Advanced Features

### Reports & Statistics
- Total books and availability
- Member statistics
- Borrowing activity
- Overdue books list
- Fine summary
- Category distribution

### Data Validation
- Unique ISBNs and emails
- No duplicate registrations
- Automatic quantity tracking
- Fine prevention checks

## Next Steps

1. **Explore the System**: Run `python main.py` and try each menu option
2. **Test Operations**: Use the sample data to practice borrowing/returning
3. **Review Code**: Check `db_operations.py` for implementation details
4. **Customize**: Modify settings in the code (fine rates, borrowing duration, etc.)

## Tips & Best Practices

- ✓ Always pay outstanding fines before borrowing new books
- ✓ Note the borrowing ID when a book is issued
- ✓ Check overdue books regularly from Reports menu
- ✓ Use search functionality for quick access instead of scrolling lists
- ✓ Back up your database before making major changes

## Support & Documentation

- See `README.md` for detailed documentation
- Check code comments in Python files for implementation details
- Run `test_system.py` to verify system functionality
- Each module has docstrings explaining functions

## Version Information

- **Version**: 1.0
- **Status**: Fully Functional
- **Last Updated**: February 2026
- **Python Required**: 3.7+

---

**Ready to use? Run: `python main.py`**

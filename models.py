"""
Data models for Library Management System
"""
from datetime import datetime, timedelta

class Book:
    """Represents a book in the library"""
    def __init__(self, title, author, isbn=None, publication_year=None, quantity=1, category=None):
        self.book_id = None
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.quantity = quantity
        self.available_quantity = quantity
        self.category = category
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"Book(ID:{self.book_id}, Title:'{self.title}', Author:'{self.author}', Available:{self.available_quantity}/{self.quantity})"

class Member:
    """Represents a library member"""
    def __init__(self, name, email=None, phone=None, address=None):
        self.member_id = None
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.membership_date = datetime.now()
        self.membership_status = 'active'
        self.outstanding_fine = 0.0
    
    def __repr__(self):
        return f"Member(ID:{self.member_id}, Name:'{self.name}', Status:'{self.membership_status}', Fine:${self.outstanding_fine:.2f})"

class BorrowingRecord:
    """Represents a borrowing transaction"""
    def __init__(self, member_id, book_id, borrow_duration_days=14):
        self.borrow_id = None
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=borrow_duration_days)
        self.return_date = None
        self.status = 'borrowed'
        self.fine_amount = 0.0
    
    def __repr__(self):
        return f"BorrowingRecord(ID:{self.borrow_id}, Member:{self.member_id}, Book:{self.book_id}, Status:'{self.status}')"
    
    def is_overdue(self):
        """Check if the book is overdue"""
        if self.status == 'returned':
            return False
        return datetime.now() > self.due_date
    
    def calculate_fine(self, fine_per_day=1.0):
        """Calculate overdue fine"""
        if self.status == 'returned':
            return 0.0
        
        if self.is_overdue():
            days_overdue = (datetime.now() - self.due_date).days
            return days_overdue * fine_per_day
        return 0.0

class Fine:
    """Represents a fine/penalty"""
    def __init__(self, member_id, amount, reason, borrow_id=None):
        self.fine_id = None
        self.member_id = member_id
        self.borrow_id = borrow_id
        self.amount = amount
        self.reason = reason
        self.paid = False
        self.created_date = datetime.now()
    
    def __repr__(self):
        return f"Fine(ID:{self.fine_id}, Member:{self.member_id}, Amount:${self.amount:.2f}, Paid:{self.paid})"

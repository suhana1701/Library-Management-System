"""
Database operations for Library Management System
"""
from database import get_connection
from models import Book, Member, BorrowingRecord, Fine
from datetime import datetime, timedelta

class BookManager:
    """Manage book operations"""
    
    @staticmethod
    def add_book(book):
        """Add a new book to the library"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, isbn, publication_year, quantity, available_quantity, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book.title, book.author, book.isbn, book.publication_year, book.quantity, book.available_quantity, book.category))
            conn.commit()
            book.book_id = cursor.lastrowid
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    @staticmethod
    def get_book_by_id(book_id):
        """Retrieve a book by ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                book = Book(row[1], row[2], row[3], row[4], row[5], row[7])
                book.book_id = row[0]
                book.available_quantity = row[6]
                return book
            return None
        except Exception as e:
            print(f"Error retrieving book: {e}")
            return None
    
    @staticmethod
    def search_books(search_term):
        """Search books by title, author, or ISBN"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM books 
                WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()
            conn.close()
            
            books = []
            for row in rows:
                book = Book(row[1], row[2], row[3], row[4], row[5], row[7])
                book.book_id = row[0]
                book.available_quantity = row[6]
                books.append(book)
            return books
        except Exception as e:
            print(f"Error searching books: {e}")
            return []
    
    @staticmethod
    def get_all_books():
        """Get all books from the library"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            conn.close()
            
            books = []
            for row in rows:
                book = Book(row[1], row[2], row[3], row[4], row[5], row[7])
                book.book_id = row[0]
                book.available_quantity = row[6]
                books.append(book)
            return books
        except Exception as e:
            print(f"Error retrieving books: {e}")
            return []
    
    @staticmethod
    def update_book(book):
        """Update book information"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books 
                SET title = ?, author = ?, isbn = ?, publication_year = ?, quantity = ?, category = ?
                WHERE book_id = ?
            """, (book.title, book.author, book.isbn, book.publication_year, book.quantity, book.category, book.book_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
    
    @staticmethod
    def delete_book(book_id):
        """Delete a book from the library"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False


class MemberManager:
    """Manage member operations"""
    
    @staticmethod
    def add_member(member):
        """Add a new member to the library"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO members (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            """, (member.name, member.email, member.phone, member.address))
            conn.commit()
            member.member_id = cursor.lastrowid
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding member: {e}")
            return False
    
    @staticmethod
    def get_member_by_id(member_id):
        """Retrieve a member by ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                member = Member(row[1], row[2], row[3], row[4])
                member.member_id = row[0]
                member.membership_status = row[6]
                member.outstanding_fine = row[7]
                return member
            return None
        except Exception as e:
            print(f"Error retrieving member: {e}")
            return None
    
    @staticmethod
    def search_members(search_term):
        """Search members by name or email"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM members 
                WHERE name LIKE ? OR email LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()
            conn.close()
            
            members = []
            for row in rows:
                member = Member(row[1], row[2], row[3], row[4])
                member.member_id = row[0]
                member.membership_status = row[6]
                member.outstanding_fine = row[7]
                members.append(member)
            return members
        except Exception as e:
            print(f"Error searching members: {e}")
            return []
    
    @staticmethod
    def get_all_members():
        """Get all members"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            rows = cursor.fetchall()
            conn.close()
            
            members = []
            for row in rows:
                member = Member(row[1], row[2], row[3], row[4])
                member.member_id = row[0]
                member.membership_status = row[6]
                member.outstanding_fine = row[7]
                members.append(member)
            return members
        except Exception as e:
            print(f"Error retrieving members: {e}")
            return []
    
    @staticmethod
    def update_member(member):
        """Update member information"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE members 
                SET name = ?, email = ?, phone = ?, address = ?, membership_status = ?, outstanding_fine = ?
                WHERE member_id = ?
            """, (member.name, member.email, member.phone, member.address, member.membership_status, member.outstanding_fine, member.member_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating member: {e}")
            return False
    
    @staticmethod
    def delete_member(member_id):
        """Delete a member"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE member_id = ?", (member_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting member: {e}")
            return False


class BorrowingManager:
    """Manage borrowing operations"""
    
    @staticmethod
    def borrow_book(member_id, book_id, borrow_duration_days=14):
        """Record a book borrowing"""
        try:
            # Check if book is available
            book = BookManager.get_book_by_id(book_id)
            if not book or book.available_quantity <= 0:
                return False, "Book not available"
            
            # Create borrowing record
            borrowing = BorrowingRecord(member_id, book_id, borrow_duration_days)
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO borrowing (member_id, book_id, borrow_date, due_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (borrowing.member_id, borrowing.book_id, borrowing.borrow_date, borrowing.due_date, borrowing.status))
            conn.commit()
            borrowing.borrow_id = cursor.lastrowid
            
            # Update available quantity
            cursor.execute("""
                UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = ?
            """, (book_id,))
            conn.commit()
            conn.close()
            
            return True, f"Book borrowed successfully. Due date: {borrowing.due_date.strftime('%Y-%m-%d')}"
        except Exception as e:
            return False, f"Error borrowing book: {e}"
    
    @staticmethod
    def return_book(borrow_id, fine_per_day=1.0):
        """Record a book return"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM borrowing WHERE borrow_id = ?", (borrow_id,))
            row = cursor.fetchone()
            
            if not row:
                return False, "Borrowing record not found"
            
            # Calculate fine if overdue
            due_date = datetime.fromisoformat(row[4])
            fine_amount = 0.0
            if datetime.now() > due_date:
                days_overdue = (datetime.now() - due_date).days
                fine_amount = days_overdue * fine_per_day
            
            # Update borrowing record
            cursor.execute("""
                UPDATE borrowing 
                SET return_date = ?, status = 'returned', fine_amount = ?
                WHERE borrow_id = ?
            """, (datetime.now(), fine_amount, borrow_id))
            
            # Update available quantity
            cursor.execute("""
                UPDATE books SET available_quantity = available_quantity + 1 
                WHERE book_id = ?
            """, (row[2],))
            
            # If there's a fine, add it to member's outstanding fine
            if fine_amount > 0:
                cursor.execute("""
                    UPDATE members SET outstanding_fine = outstanding_fine + ?
                    WHERE member_id = ?
                """, (fine_amount, row[1]))
                
                # Create fine record
                cursor.execute("""
                    INSERT INTO fines (member_id, borrow_id, amount, reason)
                    VALUES (?, ?, ?, ?)
                """, (row[1], borrow_id, fine_amount, f"Late return fine - {days_overdue} days overdue"))
            
            conn.commit()
            conn.close()
            
            message = f"Book returned successfully"
            if fine_amount > 0:
                message += f". Fine imposed: ${fine_amount:.2f}"
            return True, message
        except Exception as e:
            return False, f"Error returning book: {e}"
    
    @staticmethod
    def get_active_borrowings(member_id):
        """Get active borrowings for a member"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM borrowing 
                WHERE member_id = ? AND status = 'borrowed'
            """, (member_id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(f"Error retrieving borrowings: {e}")
            return []
    
    @staticmethod
    def get_all_borrowings():
        """Get all borrowing records"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM borrowing WHERE status = 'borrowed'")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(f"Error retrieving borrowings: {e}")
            return []
    
    @staticmethod
    def get_overdue_books():
        """Get all overdue books"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.*, m.name 
                FROM borrowing b
                JOIN members m ON b.member_id = m.member_id
                WHERE b.status = 'borrowed' AND b.due_date < ?
            """, (datetime.now(),))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(f"Error retrieving overdue books: {e}")
            return []


class FineManager:
    """Manage fine operations"""
    
    @staticmethod
    def pay_fine(fine_id):
        """Mark a fine as paid"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get fine details
            cursor.execute("SELECT * FROM fines WHERE fine_id = ?", (fine_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Fine not found"
            
            # Update fine as paid
            cursor.execute("""
                UPDATE fines SET paid = 1 WHERE fine_id = ?
            """, (fine_id,))
            
            # Update member's outstanding fine
            cursor.execute("""
                UPDATE members SET outstanding_fine = outstanding_fine - ?
                WHERE member_id = ?
            """, (row[3], row[1]))
            
            conn.commit()
            conn.close()
            return True, f"Fine paid successfully. Amount: ${row[3]:.2f}"
        except Exception as e:
            return False, f"Error paying fine: {e}"
    
    @staticmethod
    def get_member_fines(member_id):
        """Get all fines for a member"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM fines 
                WHERE member_id = ? ORDER BY created_date DESC
            """, (member_id,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(f"Error retrieving fines: {e}")
            return []

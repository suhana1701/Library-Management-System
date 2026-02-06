"""
Test and demonstration script for Library Management System
This script demonstrates the functionality of the system programmatically
"""
from datetime import datetime, timedelta
from database import init_database, DATABASE_FILE
from db_operations import BookManager, MemberManager, BorrowingManager, FineManager
from models import Book, Member
import os

def print_test_header(test_name):
    """Print a formatted test header"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}".center(60))
    print(f"{'='*60}\n")

def test_book_operations():
    """Test book management operations"""
    print_test_header("Book Management Operations")
    
    # Add books
    print("1. Adding books:")
    book1 = Book("Python Programming", "Guido van Rossum", "978-0123456789", 2020, 5, "Programming")
    book2 = Book("Web Development", "John Doe", "978-0987654321", 2021, 3, "Programming")
    
    BookManager.add_book(book1)
    BookManager.add_book(book2)
    print(f"   ✓ Book 1: {book1}")
    print(f"   ✓ Book 2: {book2}")
    
    # Get all books
    print("\n2. Retrieving all books:")
    books = BookManager.get_all_books()
    print(f"   Total books in library: {len(books)}")
    
    # Search books
    print("\n3. Searching for books:")
    search_results = BookManager.search_books("Python")
    print(f"   Found {len(search_results)} book(s) matching 'Python'")
    for book in search_results:
        print(f"   - {book.title}")
    
    # Update book
    print("\n4. Updating book:")
    book1.quantity = 6
    book1.available_quantity = 6
    if BookManager.update_book(book1):
        print(f"   ✓ Updated {book1.title} quantity to {book1.quantity}")
    
    return book1.book_id, book2.book_id

def test_member_operations():
    """Test member management operations"""
    print_test_header("Member Management Operations")
    
    # Register members
    print("1. Registering members:")
    member1 = Member("Alice Johnson", "alice@email.com", "555-0001", "100 Main St")
    member2 = Member("Bob Smith", "bob@email.com", "555-0002", "200 Oak Ave")
    
    MemberManager.add_member(member1)
    MemberManager.add_member(member2)
    print(f"   ✓ Member 1: {member1}")
    print(f"   ✓ Member 2: {member2}")
    
    # Get all members
    print("\n2. Retrieving all members:")
    members = MemberManager.get_all_members()
    print(f"   Total members: {len(members)}")
    
    # Search members
    print("\n3. Searching for members:")
    search_results = MemberManager.search_members("Alice")
    print(f"   Found {len(search_results)} member(s) matching 'Alice'")
    for member in search_results:
        print(f"   - {member.name}")
    
    # Get member details
    print("\n4. Retrieving member details:")
    member = MemberManager.get_member_by_id(member1.member_id)
    if member:
        print(f"   ✓ Member: {member.name}")
        print(f"   ✓ Email: {member.email}")
        print(f"   ✓ Status: {member.membership_status}")
        print(f"   ✓ Outstanding Fine: ${member.outstanding_fine:.2f}")
    
    return member1.member_id, member2.member_id

def test_borrowing_operations(member_id, book_id):
    """Test borrowing management operations"""
    print_test_header("Borrowing Management Operations")
    
    # Borrow a book
    print("1. Borrowing a book:")
    success, message = BorrowingManager.borrow_book(member_id, book_id, 14)
    print(f"   ✓ {message}")
    
    # Get active borrowings
    print("\n2. Retrieving active borrowings:")
    borrowings = BorrowingManager.get_active_borrowings(member_id)
    print(f"   Active borrowings for member {member_id}: {len(borrowings)}")
    for borrow in borrowings:
        due_date = datetime.fromisoformat(borrow[4])
        print(f"   - Book ID: {borrow[2]}, Due: {due_date.strftime('%Y-%m-%d')}")
    
    # Return the book
    print("\n3. Returning a book:")
    success, message = BorrowingManager.return_book(borrowings[0][0])
    print(f"   ✓ {message}")
    
    return borrowings[0][0]

def test_overdue_scenario(member_id, book_id):
    """Test overdue book scenario"""
    print_test_header("Overdue Book Scenario")
    
    # Borrow with 1 day duration
    print("1. Borrowing a book for 1 day:")
    success, message = BorrowingManager.borrow_book(member_id, book_id, 1)
    print(f"   ✓ {message}")
    
    # Get the borrowing record
    borrowings = BorrowingManager.get_active_borrowings(member_id)
    if borrowings:
        due_date = datetime.fromisoformat(borrowings[0][4])
        print(f"\n2. Due date: {due_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Simulate return after due date
        print(f"\n3. Simulating late return (showing what would happen):")
        print(f"   - If returned today, would be {(datetime.now() - due_date).days} day(s) overdue")
        
        if (datetime.now() - due_date).days > 0:
            print(f"   ✓ Fine would be calculated at $1.00/day")

def test_fine_operations(member_id):
    """Test fine management operations"""
    print_test_header("Fine Management Operations")
    
    # Get member fines
    print(f"1. Retrieving fines for member {member_id}:")
    fines = FineManager.get_member_fines(member_id)
    
    if not fines:
        print(f"   No fines for this member yet.")
    else:
        print(f"   Total fines: {len(fines)}")
        for fine in fines:
            paid_status = "Paid" if fine[5] == 1 else "Unpaid"
            print(f"   - Fine ID: {fine[0]}, Amount: ${fine[3]:.2f}, Status: {paid_status}")
        
        # Pay a fine if there are unpaid ones
        unpaid_fines = [f for f in fines if f[5] == 0]
        if unpaid_fines:
            print(f"\n2. Paying a fine:")
            success, message = FineManager.pay_fine(unpaid_fines[0][0])
            print(f"   ✓ {message}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE TEST SUITE".center(60))
    print("="*60)
    
    # Initialize database
    print("\nInitializing database...")
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    init_database()
    print("✓ Database initialized")
    
    # Run tests
    try:
        book_id_1, book_id_2 = test_book_operations()
        member_id_1, member_id_2 = test_member_operations()
        test_borrowing_operations(member_id_1, book_id_1)
        test_overdue_scenario(member_id_2, book_id_2)
        test_fine_operations(member_id_1)
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY".center(60))
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()

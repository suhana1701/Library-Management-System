"""
Main application for Library Management System
"""
import os
from datetime import datetime
from database import init_database, DATABASE_FILE
from db_operations import BookManager, MemberManager, BorrowingManager, FineManager
from models import Book, Member

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}".center(60))
    print("="*60 + "\n")

def print_menu(options):
    """Print a menu"""
    for key, value in options.items():
        print(f"{key}. {value}")
    print()

def manage_books():
    """Book management menu"""
    while True:
        clear_screen()
        print_header("📚 BOOK MANAGEMENT")
        options = {
            "1": "Add New Book",
            "2": "View All Books",
            "3": "Search Books",
            "4": "Update Book",
            "5": "Delete Book",
            "0": "Back to Main Menu"
        }
        print_menu(options)
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def add_book():
    """Add a new book"""
    clear_screen()
    print_header("➕ ADD NEW BOOK")
    
    title = input("Book Title: ").strip()
    if not title:
        print("Title cannot be empty!")
        input("Press Enter to continue...")
        return
    
    author = input("Author Name: ").strip()
    if not author:
        print("Author cannot be empty!")
        input("Press Enter to continue...")
        return
    
    isbn = input("ISBN (optional): ").strip()
    
    try:
        pub_year = input("Publication Year (optional): ").strip()
        pub_year = int(pub_year) if pub_year else None
    except ValueError:
        pub_year = None
    
    try:
        quantity = int(input("Quantity: ").strip() or "1")
    except ValueError:
        quantity = 1
    
    category = input("Category (optional): ").strip()
    
    book = Book(title, author, isbn, pub_year, quantity, category)
    
    if BookManager.add_book(book):
        print(f"\n✓ Book '{title}' added successfully with ID: {book.book_id}")
    else:
        print("\n✗ Error adding book. Please check if ISBN is unique.")
    
    input("Press Enter to continue...")

def view_all_books():
    """View all books in the library"""
    clear_screen()
    print_header("📖 ALL BOOKS IN LIBRARY")
    
    books = BookManager.get_all_books()
    
    if not books:
        print("No books in the library yet.")
    else:
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Available':<10} {'Category':<15}")
        print("-"*80)
        for book in books:
            print(f"{book.book_id:<5} {book.title[:29]:<30} {book.author[:19]:<20} {book.available_quantity}/{book.quantity:<8} {(book.category or 'N/A')[:14]:<15}")
        print(f"\nTotal Books: {len(books)}")
    
    input("\nPress Enter to continue...")

def search_books():
    """Search for books"""
    clear_screen()
    print_header("🔍 SEARCH BOOKS")
    
    search_term = input("Enter search term (Title/Author/ISBN): ").strip()
    if not search_term:
        print("Search term cannot be empty!")
        input("Press Enter to continue...")
        return
    
    books = BookManager.search_books(search_term)
    
    if not books:
        print(f"No books found matching '{search_term}'.")
    else:
        print(f"\nFound {len(books)} book(s):\n")
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Available':<10}")
        print("-"*65)
        for book in books:
            print(f"{book.book_id:<5} {book.title[:29]:<30} {book.author[:19]:<20} {book.available_quantity}/{book.quantity:<8}")
    
    input("\nPress Enter to continue...")

def update_book():
    """Update book information"""
    clear_screen()
    print_header("✏️ UPDATE BOOK")
    
    try:
        book_id = int(input("Enter Book ID: ").strip())
    except ValueError:
        print("Invalid Book ID!")
        input("Press Enter to continue...")
        return
    
    book = BookManager.get_book_by_id(book_id)
    if not book:
        print("Book not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nCurrent Info: {book}")
    print("\nEnter new values (press Enter to keep current):\n")
    
    title = input(f"Title [{book.title}]: ").strip() or book.title
    author = input(f"Author [{book.author}]: ").strip() or book.author
    isbn = input(f"ISBN [{book.isbn}]: ").strip() or book.isbn
    
    try:
        pub_year = input(f"Publication Year [{book.publication_year}]: ").strip()
        pub_year = int(pub_year) if pub_year else book.publication_year
    except ValueError:
        pub_year = book.publication_year
    
    try:
        quantity = int(input(f"Quantity [{book.quantity}]: ").strip() or book.quantity)
    except ValueError:
        quantity = book.quantity
    
    category = input(f"Category [{book.category}]: ").strip() or book.category
    
    book.title = title
    book.author = author
    book.isbn = isbn
    book.publication_year = pub_year
    book.quantity = quantity
    book.category = category
    
    if BookManager.update_book(book):
        print("\n✓ Book updated successfully!")
    else:
        print("\n✗ Error updating book!")
    
    input("Press Enter to continue...")

def delete_book():
    """Delete a book"""
    clear_screen()
    print_header("🗑️ DELETE BOOK")
    
    try:
        book_id = int(input("Enter Book ID to delete: ").strip())
    except ValueError:
        print("Invalid Book ID!")
        input("Press Enter to continue...")
        return
    
    book = BookManager.get_book_by_id(book_id)
    if not book:
        print("Book not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nBook to delete: {book}")
    confirm = input("\nAre you sure? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        if BookManager.delete_book(book_id):
            print("\n✓ Book deleted successfully!")
        else:
            print("\n✗ Error deleting book!")
    else:
        print("Deletion cancelled.")
    
    input("Press Enter to continue...")

def manage_members():
    """Member management menu"""
    while True:
        clear_screen()
        print_header("👥 MEMBER MANAGEMENT")
        options = {
            "1": "Register New Member",
            "2": "View All Members",
            "3": "Search Members",
            "4": "View Member Details",
            "5": "Update Member",
            "6": "Delete Member",
            "0": "Back to Main Menu"
        }
        print_menu(options)
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            register_member()
        elif choice == "2":
            view_all_members()
        elif choice == "3":
            search_members()
        elif choice == "4":
            view_member_details()
        elif choice == "5":
            update_member()
        elif choice == "6":
            delete_member()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def register_member():
    """Register a new member"""
    clear_screen()
    print_header("➕ REGISTER NEW MEMBER")
    
    name = input("Full Name: ").strip()
    if not name:
        print("Name cannot be empty!")
        input("Press Enter to continue...")
        return
    
    email = input("Email: ").strip()
    phone = input("Phone Number: ").strip()
    address = input("Address: ").strip()
    
    member = Member(name, email, phone, address)
    
    if MemberManager.add_member(member):
        print(f"\n✓ Member '{name}' registered successfully with ID: {member.member_id}")
    else:
        print("\n✗ Error registering member. Please check if email is unique.")
    
    input("Press Enter to continue...")

def view_all_members():
    """View all members"""
    clear_screen()
    print_header("👥 ALL MEMBERS")
    
    members = MemberManager.get_all_members()
    
    if not members:
        print("No members registered yet.")
    else:
        print(f"{'ID':<5} {'Name':<25} {'Email':<25} {'Status':<10} {'Fine':<10}")
        print("-"*75)
        for member in members:
            print(f"{member.member_id:<5} {member.name[:24]:<25} {(member.email or 'N/A')[:24]:<25} {member.membership_status:<10} ${member.outstanding_fine:<9.2f}")
        print(f"\nTotal Members: {len(members)}")
    
    input("\nPress Enter to continue...")

def search_members():
    """Search for members"""
    clear_screen()
    print_header("🔍 SEARCH MEMBERS")
    
    search_term = input("Enter search term (Name/Email): ").strip()
    if not search_term:
        print("Search term cannot be empty!")
        input("Press Enter to continue...")
        return
    
    members = MemberManager.search_members(search_term)
    
    if not members:
        print(f"No members found matching '{search_term}'.")
    else:
        print(f"\nFound {len(members)} member(s):\n")
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Status':<10}")
        print("-"*70)
        for member in members:
            print(f"{member.member_id:<5} {member.name[:24]:<25} {(member.email or 'N/A')[:29]:<30} {member.membership_status:<10}")
    
    input("\nPress Enter to continue...")

def view_member_details():
    """View detailed member information"""
    clear_screen()
    print_header("👤 MEMBER DETAILS")
    
    try:
        member_id = int(input("Enter Member ID: ").strip())
    except ValueError:
        print("Invalid Member ID!")
        input("Press Enter to continue...")
        return
    
    member = MemberManager.get_member_by_id(member_id)
    if not member:
        print("Member not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nName: {member.name}")
    print(f"Member ID: {member.member_id}")
    print(f"Email: {member.email or 'N/A'}")
    print(f"Phone: {member.phone or 'N/A'}")
    print(f"Address: {member.address or 'N/A'}")
    print(f"Membership Status: {member.membership_status}")
    print(f"Outstanding Fine: ${member.outstanding_fine:.2f}")
    
    # Show active borrowings
    borrowings = BorrowingManager.get_active_borrowings(member_id)
    print(f"\n📚 Active Borrowings: {len(borrowings)}")
    for borrow in borrowings:
        book = BookManager.get_book_by_id(borrow[2])
        due_date = datetime.fromisoformat(borrow[4])
        status_icon = "⚠️" if datetime.now() > due_date else "✓"
        print(f"  {status_icon} Book ID: {borrow[2]}, Due: {due_date.strftime('%Y-%m-%d')}")
    
    # Show unpaid fines
    fines = FineManager.get_member_fines(member_id)
    unpaid_fines = [f for f in fines if f[5] == 0]
    print(f"\n💰 Unpaid Fines: {len(unpaid_fines)}")
    for fine in unpaid_fines:
        print(f"  Fine ID: {fine[0]}, Amount: ${fine[3]:.2f}, Reason: {fine[4]}")
    
    input("\nPress Enter to continue...")

def update_member():
    """Update member information"""
    clear_screen()
    print_header("✏️ UPDATE MEMBER")
    
    try:
        member_id = int(input("Enter Member ID: ").strip())
    except ValueError:
        print("Invalid Member ID!")
        input("Press Enter to continue...")
        return
    
    member = MemberManager.get_member_by_id(member_id)
    if not member:
        print("Member not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nCurrent Info: {member}")
    print("\nEnter new values (press Enter to keep current):\n")
    
    name = input(f"Name [{member.name}]: ").strip() or member.name
    email = input(f"Email [{member.email}]: ").strip() or member.email
    phone = input(f"Phone [{member.phone}]: ").strip() or member.phone
    address = input(f"Address [{member.address}]: ").strip() or member.address
    
    member.name = name
    member.email = email
    member.phone = phone
    member.address = address
    
    if MemberManager.update_member(member):
        print("\n✓ Member updated successfully!")
    else:
        print("\n✗ Error updating member!")
    
    input("Press Enter to continue...")

def delete_member():
    """Delete a member"""
    clear_screen()
    print_header("🗑️ DELETE MEMBER")
    
    try:
        member_id = int(input("Enter Member ID to delete: ").strip())
    except ValueError:
        print("Invalid Member ID!")
        input("Press Enter to continue...")
        return
    
    member = MemberManager.get_member_by_id(member_id)
    if not member:
        print("Member not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nMember to delete: {member}")
    confirm = input("\nAre you sure? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        if MemberManager.delete_member(member_id):
            print("\n✓ Member deleted successfully!")
        else:
            print("\n✗ Error deleting member!")
    else:
        print("Deletion cancelled.")
    
    input("Press Enter to continue...")

def manage_borrowing():
    """Borrowing management menu"""
    while True:
        clear_screen()
        print_header("📚 BORROWING MANAGEMENT")
        options = {
            "1": "Borrow a Book",
            "2": "Return a Book",
            "3": "View Active Borrowings",
            "4": "View Overdue Books",
            "0": "Back to Main Menu"
        }
        print_menu(options)
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            borrow_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            view_active_borrowings()
        elif choice == "4":
            view_overdue_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def borrow_book():
    """Record a book borrowing"""
    clear_screen()
    print_header("📤 BORROW A BOOK")
    
    try:
        member_id = int(input("Enter Member ID: ").strip())
    except ValueError:
        print("Invalid Member ID!")
        input("Press Enter to continue...")
        return
    
    member = MemberManager.get_member_by_id(member_id)
    if not member:
        print("Member not found!")
        input("Press Enter to continue...")
        return
    
    if member.outstanding_fine > 0:
        print(f"\n⚠️ Warning! Member has outstanding fine: ${member.outstanding_fine:.2f}")
        proceed = input("Continue? (yes/no): ").strip().lower()
        if proceed != 'yes':
            input("Press Enter to continue...")
            return
    
    try:
        book_id = int(input("Enter Book ID: ").strip())
    except ValueError:
        print("Invalid Book ID!")
        input("Press Enter to continue...")
        return
    
    book = BookManager.get_book_by_id(book_id)
    if not book:
        print("Book not found!")
        input("Press Enter to continue...")
        return
    
    print(f"\nBook: {book.title} by {book.author}")
    print(f"Available: {book.available_quantity}")
    
    if book.available_quantity <= 0:
        print("This book is not available for borrowing!")
        input("Press Enter to continue...")
        return
    
    try:
        days = int(input("Borrow duration (days) [14]: ").strip() or "14")
    except ValueError:
        days = 14
    
    success, message = BorrowingManager.borrow_book(member_id, book_id, days)
    
    if success:
        print(f"\n✓ {message}")
    else:
        print(f"\n✗ {message}")
    
    input("Press Enter to continue...")

def return_book():
    """Record a book return"""
    clear_screen()
    print_header("📥 RETURN A BOOK")
    
    try:
        borrow_id = int(input("Enter Borrowing ID: ").strip())
    except ValueError:
        print("Invalid Borrowing ID!")
        input("Press Enter to continue...")
        return
    
    try:
        fine_per_day = float(input("Fine per day [1.0]: ").strip() or "1.0")
    except ValueError:
        fine_per_day = 1.0
    
    success, message = BorrowingManager.return_book(borrow_id, fine_per_day)
    
    if success:
        print(f"\n✓ {message}")
    else:
        print(f"\n✗ {message}")
    
    input("Press Enter to continue...")

def view_active_borrowings():
    """View all active borrowings"""
    clear_screen()
    print_header("📚 ACTIVE BORROWINGS")
    
    borrowings = BorrowingManager.get_all_borrowings()
    
    if not borrowings:
        print("No active borrowings.")
    else:
        print(f"{'Borrow ID':<12} {'Member ID':<12} {'Book ID':<10} {'Due Date':<15} {'Days Left':<12}")
        print("-"*60)
        for borrow in borrowings:
            due_date = datetime.fromisoformat(borrow[4])
            days_left = (due_date - datetime.now()).days
            status = "⚠️" if days_left < 0 else "✓"
            days_display = f"{status} {days_left}"
            print(f"{borrow[0]:<12} {borrow[1]:<12} {borrow[2]:<10} {due_date.strftime('%Y-%m-%d'):<15} {days_display:<12}")
        print(f"\nTotal Active Borrowings: {len(borrowings)}")
    
    input("\nPress Enter to continue...")

def view_overdue_books():
    """View all overdue books"""
    clear_screen()
    print_header("⚠️ OVERDUE BOOKS")
    
    overdue = BorrowingManager.get_overdue_books()
    
    if not overdue:
        print("No overdue books.")
    else:
        print(f"{'Borrow ID':<12} {'Member':<20} {'Book ID':<10} {'Due Date':<15} {'Days Overdue':<15}")
        print("-"*72)
        for borrow in overdue:
            due_date = datetime.fromisoformat(borrow[4])
            days_overdue = (datetime.now() - due_date).days
            print(f"{borrow[0]:<12} {borrow[9][:19]:<20} {borrow[2]:<10} {due_date.strftime('%Y-%m-%d'):<15} {days_overdue:<15}")
        print(f"\nTotal Overdue Books: {len(overdue)}")
    
    input("\nPress Enter to continue...")

def manage_fines():
    """Fine management menu"""
    while True:
        clear_screen()
        print_header("💰 FINE MANAGEMENT")
        options = {
            "1": "View Member Fines",
            "2": "Pay a Fine",
            "3": "View All Unpaid Fines",
            "0": "Back to Main Menu"
        }
        print_menu(options)
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_member_fines()
        elif choice == "2":
            pay_fine()
        elif choice == "3":
            view_all_unpaid_fines()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_member_fines():
    """View fines for a member"""
    clear_screen()
    print_header("💰 MEMBER FINES")
    
    try:
        member_id = int(input("Enter Member ID: ").strip())
    except ValueError:
        print("Invalid Member ID!")
        input("Press Enter to continue...")
        return
    
    member = MemberManager.get_member_by_id(member_id)
    if not member:
        print("Member not found!")
        input("Press Enter to continue...")
        return
    
    print(f"Member: {member.name}")
    print(f"Outstanding Fine: ${member.outstanding_fine:.2f}\n")
    
    fines = FineManager.get_member_fines(member_id)
    
    if not fines:
        print("No fines for this member.")
    else:
        print(f"{'Fine ID':<10} {'Amount':<12} {'Reason':<35} {'Paid':<6}")
        print("-"*63)
        for fine in fines:
            paid_status = "Yes" if fine[5] == 1 else "No"
            print(f"{fine[0]:<10} ${fine[3]:<11.2f} {(fine[4] or 'N/A')[:34]:<35} {paid_status:<6}")
    
    input("\nPress Enter to continue...")

def pay_fine():
    """Pay a fine"""
    clear_screen()
    print_header("💳 PAY A FINE")
    
    try:
        fine_id = int(input("Enter Fine ID: ").strip())
    except ValueError:
        print("Invalid Fine ID!")
        input("Press Enter to continue...")
        return
    
    success, message = FineManager.pay_fine(fine_id)
    
    if success:
        print(f"\n✓ {message}")
    else:
        print(f"\n✗ {message}")
    
    input("Press Enter to continue...")

def view_all_unpaid_fines():
    """View all unpaid fines in the library"""
    clear_screen()
    print_header("💰 ALL UNPAID FINES")
    
    # This would require a query that gets all unpaid fines
    # For now, we'll implement a simple version
    members = MemberManager.get_all_members()
    all_fines = []
    
    for member in members:
        fines = FineManager.get_member_fines(member.member_id)
        for fine in fines:
            if fine[5] == 0:  # Not paid
                all_fines.append((fine, member.name))
    
    if not all_fines:
        print("No unpaid fines.")
    else:
        total_amount = sum(fine[0][3] for fine in all_fines)
        print(f"{'Fine ID':<10} {'Member':<20} {'Amount':<12} {'Reason':<30}")
        print("-"*72)
        for fine, member_name in all_fines:
            print(f"{fine[0]:<10} {member_name[:19]:<20} ${fine[3]:<11.2f} {(fine[4] or 'N/A')[:29]:<30}")
        print(f"\n{'Total Unpaid Fines:':<40} ${total_amount:.2f}")
        print(f"Number of Unpaid Fines: {len(all_fines)}")
    
    input("\nPress Enter to continue...")

def main():
    """Main application"""
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE_FILE):
        print("Initializing database...")
        init_database()
    
    while True:
        clear_screen()
        print_header("🏛️ LIBRARY MANAGEMENT SYSTEM")
        print("Welcome to the Library Management System\n")
        
        options = {
            "1": "Book Management",
            "2": "Member Management",
            "3": "Borrowing Management",
            "4": "Fine Management",
            "5": "Reports & Statistics",
            "0": "Exit"
        }
        print_menu(options)
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            manage_books()
        elif choice == "2":
            manage_members()
        elif choice == "3":
            manage_borrowing()
        elif choice == "4":
            manage_fines()
        elif choice == "5":
            show_reports()
        elif choice == "0":
            print("\nThank you for using Library Management System!")
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def show_reports():
    """Show library reports and statistics"""
    clear_screen()
    print_header("📊 REPORTS & STATISTICS")
    
    # Get statistics
    books = BookManager.get_all_books()
    members = MemberManager.get_all_members()
    active_borrowings = BorrowingManager.get_all_borrowings()
    overdue = BorrowingManager.get_overdue_books()
    
    total_books = len(books)
    total_available = sum(b.available_quantity for b in books)
    total_borrowed = sum(b.quantity - b.available_quantity for b in books)
    
    total_members = len(members)
    active_members = len([m for m in members if m.membership_status == 'active'])
    total_fines = sum(m.outstanding_fine for m in members)
    
    print("📚 BOOK STATISTICS")
    print(f"  Total Books: {total_books}")
    print(f"  Available Books: {total_available}")
    print(f"  Borrowed Books: {total_borrowed}")
    
    print("\n👥 MEMBER STATISTICS")
    print(f"  Total Members: {total_members}")
    print(f"  Active Members: {active_members}")
    print(f"  Total Outstanding Fines: ${total_fines:.2f}")
    
    print("\n📤 BORROWING STATISTICS")
    print(f"  Active Borrowings: {len(active_borrowings)}")
    print(f"  Overdue Books: {len(overdue)}")
    
    # Top categories
    if books:
        categories = {}
        for book in books:
            cat = book.category or "Uncategorized"
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📖 TOP CATEGORIES")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {cat}: {count} books")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

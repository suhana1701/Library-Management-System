"""
Configuration and Customization Guide for Library Management System

This file documents the customizable parameters in the system and how to adjust them.
"""

# ============================================================================
# CUSTOMIZABLE PARAMETERS
# ============================================================================

"""
DEFAULT BORROWING DURATION
Location: db_operations.py, BorrowingManager.borrow_book() method
Default: 14 days

To change:
    Option 1 - Change default in code:
    - Open db_operations.py
    - Find: def borrow_book(self, member_id, book_id, borrow_duration_days=14)
    - Change 14 to desired number of days
    
    Option 2 - User input during borrowing (current implementation):
    - Users can enter custom duration when borrowing
    - Press Enter to use default 14 days
"""

BORROWING_DURATION_DAYS = 14

"""
FINE RATE (per day)
Location: db_operations.py, BorrowingManager.return_book() method
Default: $1.00 per day

To change:
    Option 1 - Change in return_book method:
    - Open db_operations.py
    - Find: success, message = BorrowingManager.return_book(borrow_id, fine_per_day=1.0)
    - Change 1.0 to desired amount
    
    Option 2 - Allow user input:
    - Modify return_book() function in main.py
    - Add input for fine_per_day before calling return_book
"""

FINE_RATE_PER_DAY = 1.0

"""
MEMBER SUSPENSION THRESHOLD
To implement automatic member suspension for unpaid fines:
    - Create a method in MemberManager to check and suspend members
    - Call when fine payment status changes
    - Example threshold: $50.00
    
Code to add in MemberManager:
    @staticmethod
    def check_and_suspend_member(member_id, fine_threshold=50.0):
        member = MemberManager.get_member_by_id(member_id)
        if member.outstanding_fine >= fine_threshold:
            member.membership_status = 'suspended'
            MemberManager.update_member(member)
"""

MEMBER_SUSPENSION_THRESHOLD = 50.0

"""
MAXIMUM BORROWED BOOKS PER MEMBER
To implement a limit on concurrent borrows:
    Add this check in BorrowingManager.borrow_book():
    
    active_borrows = BorrowingManager.get_active_borrowings(member_id)
    if len(active_borrows) >= MAX_BOOKS_PER_MEMBER:
        return False, "Maximum borrowed books limit reached"
"""

MAX_BOOKS_PER_MEMBER = 5

"""
MAXIMUM OVERDUE DAYS BEFORE SUSPENSION
Implementation: Check when returning or viewing member:
    def get_days_overdue(borrow_id):
        # Calculate and return days overdue
        # If > MAX_OVERDUE_DAYS, flag for admin review
"""

MAX_OVERDUE_DAYS_ALLOWED = 30

# ============================================================================
# DATABASE CUSTOMIZATIONS
# ============================================================================

"""
To add new fields to existing tables:

1. Books table - Additional fields:
   ALTER TABLE books ADD COLUMN publisher TEXT;
   ALTER TABLE books ADD COLUMN isbn_13 TEXT;
   ALTER TABLE books ADD COLUMN pages INTEGER;

2. Members table - Additional fields:
   ALTER TABLE members ADD COLUMN registration_number TEXT UNIQUE;
   ALTER TABLE members ADD COLUMN renewal_date DATE;

3. Borrowing table - Additional fields:
   ALTER TABLE borrowing ADD COLUMN renewal_count INTEGER DEFAULT 0;
   ALTER TABLE borrowing ADD COLUMN notes TEXT;

4. New table example - Book Reviews:
   CREATE TABLE reviews (
       review_id INTEGER PRIMARY KEY,
       book_id INTEGER NOT NULL,
       member_id INTEGER NOT NULL,
       rating INTEGER CHECK(rating >= 1 AND rating <= 5),
       review_text TEXT,
       created_date TIMESTAMP,
       FOREIGN KEY (book_id) REFERENCES books(book_id),
       FOREIGN KEY (member_id) REFERENCES members(member_id)
   );
"""

# ============================================================================
# FEATURE ENHANCEMENTS
# ============================================================================

"""
ENHANCEMENT 1: Book Renewal
In BorrowingManager, add:
    @staticmethod
    def renew_book(borrow_id, additional_days=14):
        # Extend due date by additional_days
        # Limit renewals (e.g., max 2 renewals per book)
        # Check for holds by other members

ENHANCEMENT 2: Book Reservations
Create new table:
    CREATE TABLE reservations (
        reservation_id INTEGER PRIMARY KEY,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        reservation_date TIMESTAMP,
        status TEXT DEFAULT 'pending'
    );

Add ReservationManager class with:
    - reserve_book()
    - cancel_reservation()
    - get_reservations_for_book()

ENHANCEMENT 3: Late Notice System
Add method to send notifications:
    @staticmethod
    def get_books_due_soon(days=3):
        # Find books due in next N days
        # Send email/SMS notification
        # Log notification sent

ENHANCEMENT 4: Automatic Fine Waiver
Add to FineManager:
    @staticmethod
    def apply_waiver(fine_id, reason, approved_by):
        # Allow admins to waive fines with reason
        # Create audit trail
        # Notify member

ENHANCEMENT 5: Multi-Copy Management
Track individual copy status:
    ALTER TABLE books ADD COLUMN copy_number INTEGER;
    ALTER TABLE borrowing ADD COLUMN copy_number INTEGER;

ENHANCEMENT 6: Member Tiers/Categories
    Community Tier - 5 books, 14 days
    Premium Tier - 10 books, 21 days
    VIP Tier - Unlimited with 30 days

Add to Member model:
    self.membership_tier = 'community'  # or 'premium', 'vip'
"""

# ============================================================================
# UI CUSTOMIZATIONS
# ============================================================================

"""
MENU CUSTOMIZATION:
To add new menu options in main():
    1. Add option to main menu dictionary
    2. Create handler function
    3. Add elif clause to call handler

Example:
    options = {
        ...
        "6": "Manage Book Reservations",  # New option
        ...
    }
    
    elif choice == "6":
        manage_reservations()

THEMING:
Add color support (requires colorama):
    from colorama import Fore, Back, Style
    print(f"{Fore.GREEN}✓ Success!{Style.RESET_ALL}")
    
    Install: pip install colorama

DISPLAY ENHANCEMENTS:
Add tabulate for better tables (requires tabulate):
    from tabulate import tabulate
    print(tabulate(books, headers=['ID', 'Title', 'Author']))
    
    Install: pip install tabulate

PAGINATION:
For large datasets, add pagination:
    def paginate_results(items, page_size=10):
        return [items[i:i+page_size] for i in range(0, len(items), page_size)]
"""

# ============================================================================
# PERFORMANCE OPTIMIZATIONS
# ============================================================================

"""
1. INDEXING:
Add indexes for frequently searched columns:
    CREATE INDEX idx_books_title ON books(title);
    CREATE INDEX idx_books_isbn ON books(isbn);
    CREATE INDEX idx_members_email ON members(email);
    CREATE INDEX idx_borrowing_member ON borrowing(member_id);
    CREATE INDEX idx_borrowing_status ON borrowing(status);

2. CACHING:
Implement simple caching for frequently accessed data:
    class Cache:
        def __init__(self):
            self.data = {}
            self.timestamps = {}
        
        def get(self, key, expiry_minutes=5):
            if key in self.data:
                age = (datetime.now() - self.timestamps[key]).seconds
                if age < expiry_minutes * 60:
                    return self.data[key]
            return None
        
        def set(self, key, value):
            self.data[key] = value
            self.timestamps[key] = datetime.now()

3. BATCH OPERATIONS:
For bulk imports:
    def bulk_add_books(book_list):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO books (title, author, isbn, ...) VALUES (?, ?, ?, ...)",
            book_data
        )
        conn.commit()
"""

# ============================================================================
# SECURITY ENHANCEMENTS
# ============================================================================

"""
1. INPUT VALIDATION:
Add stricter validation:
    import re
    
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_isbn(isbn):
        # Remove hyphens and check length
        isbn_clean = isbn.replace('-', '')
        return len(isbn_clean) in [10, 13]

2. USER AUTHENTICATION:
Add login system:
    CREATE TABLE librarians (
        librarian_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT  -- 'admin', 'librarian', 'viewer'
    );
    
    Use: pip install python-dotenv for credentials

3. AUDIT LOGGING:
Track all operations:
    CREATE TABLE audit_log (
        log_id INTEGER PRIMARY KEY,
        action TEXT,
        table_name TEXT,
        record_id INTEGER,
        timestamp TIMESTAMP,
        user_id INTEGER
    );

4. DATA VALIDATION:
Add constraints:
    - Email format validation
    - Phone number format
    - ISBN format (10 or 13 digits)
    - Quantity >= 0
    - Fine rate >= 0
"""

# ============================================================================
# INTEGRATION EXAMPLES
# ============================================================================

"""
EMAIL NOTIFICATIONS (requires smtplib):
    def send_due_date_reminder(member_email, book_title, due_date):
        import smtplib
        message = f"Reminder: '{book_title}' is due on {due_date}"
        # Send email to member_email
        
EXPORT TO CSV (requires csv module):
    import csv
    
    def export_books_to_csv():
        books = BookManager.get_all_books()
        with open('books_export.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Author', 'ISBN'])
            for book in books:
                writer.writerow([book.book_id, book.title, book.author, book.isbn])

GENERATE REPORTS (requires reportlab):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    def generate_library_report(filename="library_report.pdf"):
        # Create PDF with statistics and charts
"""

# ============================================================================
# TROUBLESHOOTING CUSTOMIZATIONS
# ============================================================================

"""
ENABLE DEBUG LOGGING:
Add to database.py:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
Then in operations:
    logger.debug(f"Adding book: {book.title}")

EXPAND ERROR MESSAGES:
Modify error handling:
    try:
        # operation
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("Error: ISBN or Email already exists")
        else:
            print(f"Database error: {e}")

CHECK DATABASE INTEGRITY:
    def check_database_integrity():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        return result[0] == "ok"
"""

# ============================================================================
# CONFIGURATION CONSTANTS (Change these to customize behavior)
# ============================================================================

# Borrowing defaults
DEFAULT_BORROW_DAYS = 14
DEFAULT_FINE_PER_DAY = 1.0

# Member settings
DEFAULT_MEMBER_STATUS = 'active'
SUSPENSION_FINE_THRESHOLD = 50.0
MAX_CONCURRENT_BORROWS = 5

# System settings
DATABASE_NAME = "library.db"
ENABLE_LOGGING = False
MAX_SEARCH_RESULTS = 50

# These constants can be modified by administrators
# Create a config.py file for easier management

print("""
CUSTOMIZATION GUIDE
==================
1. Modify DEFAULT_BORROW_DAYS to change default borrowing period
2. Modify DEFAULT_FINE_PER_DAY to change fine rate
3. Add database columns using ALTER TABLE statements
4. Implement new managers for new features
5. Add validation functions to ensure data quality
6. Enable logging for debugging

See specific sections above for implementation details.
""")

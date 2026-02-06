"""
Sample data initialization script for Library Management System
Run this to populate the database with sample data for testing
"""
from database import init_database, DATABASE_FILE
from db_operations import BookManager, MemberManager
from models import Book, Member
import os

def init_sample_data():
    """Initialize database with sample data"""
    
    # Initialize database
    if os.path.exists(DATABASE_FILE):
        print("Database already exists. Backing up and creating new one...")
        os.rename(DATABASE_FILE, f"{DATABASE_FILE}.backup")
    
    init_database()
    
    # Sample Books
    sample_books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 1925, 3, "Fiction"),
        Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 1960, 2, "Fiction"),
        Book("1984", "George Orwell", "978-0451524935", 1949, 4, "Science Fiction"),
        Book("Pride and Prejudice", "Jane Austen", "978-0141439518", 1813, 3, "Romance"),
        Book("The Catcher in the Rye", "J.D. Salinger", "978-0316769174", 1951, 2, "Fiction"),
        Book("Sapiens", "Yuval Noah Harari", "978-0062316097", 2011, 5, "Non-Fiction"),
        Book("Thinking, Fast and Slow", "Daniel Kahneman", "978-0374533557", 2011, 3, "Non-Fiction"),
        Book("Atomic Habits", "James Clear", "978-0735211292", 2018, 6, "Self-Help"),
        Book("The Silent Patient", "Alex Michaelides", "978-1250295255", 2019, 2, "Mystery"),
        Book("Educated", "Tara Westover", "978-0399590504", 2018, 4, "Biography"),
        Book("A Brief History of Time", "Stephen Hawking", "978-0553380163", 1988, 3, "Science"),
        Book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 1937, 5, "Fantasy"),
        Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "978-0747532699", 1997, 4, "Fantasy"),
        Book("Dune", "Frank Herbert", "978-0441172719", 1965, 2, "Science Fiction"),
        Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0544003415", 1954, 3, "Fantasy"),
    ]
    
    print("Adding sample books...")
    for book in sample_books:
        if BookManager.add_book(book):
            print(f"✓ Added: {book.title}")
        else:
            print(f"✗ Error adding: {book.title}")
    
    # Sample Members
    sample_members = [
        Member("John Smith", "john.smith@email.com", "555-0101", "123 Main St"),
        Member("Mary Johnson", "mary.johnson@email.com", "555-0102", "456 Oak Ave"),
        Member("Robert Williams", "robert.williams@email.com", "555-0103", "789 Pine Rd"),
        Member("Patricia Brown", "patricia.brown@email.com", "555-0104", "321 Elm St"),
        Member("Michael Davis", "michael.davis@email.com", "555-0105", "654 Maple Dr"),
        Member("Linda Miller", "linda.miller@email.com", "555-0106", "987 Cedar Ln"),
        Member("James Wilson", "james.wilson@email.com", "555-0107", "147 Birch Ct"),
        Member("Barbara Moore", "barbara.moore@email.com", "555-0108", "258 Spruce Way"),
    ]
    
    print("\nAdding sample members...")
    for member in sample_members:
        if MemberManager.add_member(member):
            print(f"✓ Added: {member.name} (ID: {member.member_id})")
        else:
            print(f"✗ Error adding: {member.name}")
    
    print("\n✓ Sample data initialized successfully!")
    print("\nYou can now run 'python main.py' to start the application.")

if __name__ == "__main__":
    init_sample_data()

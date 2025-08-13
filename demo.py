#!/usr/bin/env python3
"""
Demo script for the Library Management System.
Demonstrates all major features and OOP concepts.
"""

from datetime import datetime, date
from models import Book, BookCategory, Member, MembershipType, ContactInfo
from services import LibraryService
from utils import BookFormatter, MemberFormatter, StatisticsFormatter


def demo_library_system():
    """Comprehensive demonstration of the library system"""
    
    print("LIBRARY MANAGEMENT SYSTEM DEMO")
    print("=" * 60)
    print("Demonstrating advanced OOP concepts and design patterns")
    print("=" * 60)
    
    # Initialize library service
    library = LibraryService()
    
    # Demo 1: Adding Books (demonstrates validation, encapsulation)
    print("\nDEMO 1: Adding Books")
    print("-" * 40)
    
    books_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5", BookCategory.FICTION, 1925),
        ("Clean Code", "Robert C. Martin", "978-0-13-235088-4", BookCategory.TECHNOLOGY, 2008),
        ("Sapiens", "Yuval Noah Harari", "978-0-06-231609-7", BookCategory.HISTORY, 2011),
        ("Python Tricks", "Dan Bader", "978-1-77505-093-3", BookCategory.TECHNOLOGY, 2017)
    ]
    
    book_objects = []
    for title, author, isbn, category, year in books_data:
        try:
            book = library.add_book(title, author, isbn, category, year)
            book_objects.append(book)
            print(f"Added: {title} by {author}")
        except Exception as e:
            print(f"Error adding {title}: {e}")
    
    print(f"\nTotal books added: {len(book_objects)}")
    
    # Demo 2: Adding Members (demonstrates inheritance, composition)
    print("\nDEMO 2: Adding Members")
    print("-" * 40)
    
    members_data = [
        ("Alice", "Johnson", MembershipType.STUDENT, "alice@university.edu", "+1-555-0101"),
        ("Dr. Bob", "Smith", MembershipType.FACULTY, "bob.smith@university.edu", "+1-555-0102"),
        ("Carol", "Davis", MembershipType.STAFF, "carol.davis@university.edu", "+1-555-0103"),
        ("David", "Wilson", MembershipType.PUBLIC, "david.wilson@email.com", "+1-555-0104")
    ]
    
    member_objects = []
    for first, last, mtype, email, phone in members_data:
        try:
            contact = ContactInfo(email, phone, "123 University St")
            member = library.add_member(first, last, mtype, contact_info=contact)
            member_objects.append(member)
            print(f"Added: {first} {last} ({mtype.value})")
        except Exception as e:
            print(f"Error adding {first} {last}: {e}")
    
    print(f"\nTotal members added: {len(member_objects)}")
    
    # Demo 3: Book Borrowing (demonstrates business logic, state management)
    print("\nDEMO 3: Book Borrowing")
    print("-" * 40)
    
    if book_objects and member_objects:
        # Borrow first book to first member
        try:
            transaction = library.borrow_book(member_objects[0].id, book_objects[0].id)
            print(f"{member_objects[0].full_name} borrowed '{book_objects[0].title}'")
            print(f"Transaction ID: {transaction.id}")
            print(f"Due Date: {transaction.due_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Error borrowing book: {e}")
        
        # Try to borrow the same book again (should fail)
        try:
            library.borrow_book(member_objects[1].id, book_objects[0].id)
        except Exception as e:
            print(f"Correctly prevented double borrowing: {e}")
    
    # Demo 4: Search and Filtering (demonstrates polymorphism)
    print("\nDEMO 4: Search and Filtering")
    print("-" * 40)
    
    # Search books by different criteria
    print("Searching for 'Python':")
    python_books = library.search_books("Python")
    for book in python_books:
        print(f"  • {book.title} by {book.author}")
    
    print("\nFiction books:")
    fiction_books = library.search_books(category=BookCategory.FICTION)
    for book in fiction_books:
        print(f"  • {book.title} by {book.author}")
    
    print("\nAvailable books only:")
    available_books = library.search_books(available_only=True)
    print(f"  Found {len(available_books)} available books")
    
    # Demo 5: Data Validation (demonstrates validation patterns)
    print("\nDEMO 5: Data Validation")
    print("-" * 40)
    
    # Try to add invalid book
    try:
        library.add_book("", "Author", "invalid-isbn")
    except Exception as e:
        print(f"Correctly rejected invalid book: {e}")
    
    # Try to add member with invalid email
    try:
        invalid_contact = ContactInfo("invalid-email", "123", "Address")
        library.add_member("Test", "User", MembershipType.PUBLIC, contact_info=invalid_contact)
    except Exception as e:
        print(f"Correctly rejected invalid email: {e}")
    
    # Demo 6: Polymorphism and Formatting
    print("\nDEMO 6: Polymorphism and Formatting")
    print("-" * 40)
    
    # Display books in different formats
    if book_objects:
        print("Book summary format:")
        for book in book_objects[:2]:
            print(f"  {BookFormatter.format_book_summary(book)}")
        
        print("\nDetailed book format:")
        print(BookFormatter.format_book_detail(book_objects[0]))
    
    # Demo 7: Business Logic and Calculations
    print("\nDEMO 7: Business Logic and Calculations")
    print("-" * 40)
    
    if member_objects:
        member = member_objects[0]
        print(f"Member: {member.full_name}")
        print(f"Membership type: {member.membership_type.value}")
        print(f"Max books allowed: {member.max_books_allowed}")
        print(f"Currently borrowed: {member.borrowed_books_count}")
        print(f"Can borrow more: {member.can_borrow_books()}")
        print(f"Membership valid until: {member.membership_end_date}")
    
    # Demo 8: Statistics and Reporting
    print("\nDEMO 8: Statistics and Reporting")
    print("-" * 40)
    
    stats = library.get_library_statistics()
    print(StatisticsFormatter.format_statistics(stats))
    
    # Demo 9: Advanced Features
    print("\nDEMO 9: Advanced Features")
    print("-" * 40)
    
    # Demonstrate sorting
    from utils import BookSorter, SortOrder
    
    all_books = library.get_all_books()
    if all_books:
        print("Books sorted by title:")
        sorted_books = BookSorter.by_title(all_books)
        for book in sorted_books:
            print(f"  • {book.title}")
        
        print("\nBooks sorted by publication year (descending):")
        sorted_by_year = BookSorter.by_publication_year(all_books, SortOrder.DESC)
        for book in sorted_by_year:
            year = book.publication_year or "Unknown"
            print(f"  • {book.title} ({year})")
    
    # Demo 10: Error Handling and Edge Cases
    print("\nDEMO 10: Error Handling and Edge Cases")
    print("-" * 40)
    
    # Try various invalid operations
    test_cases = [
        ("Get non-existent book", lambda: library.get_book("invalid-id")),
        ("Get non-existent member", lambda: library.get_member("invalid-id")),
        ("Return book not borrowed", lambda: library.return_book(member_objects[0].id, book_objects[1].id) if member_objects and book_objects else None),
    ]
    
    for test_name, test_func in test_cases:
        try:
            if test_func:
                test_func()
            print(f"{test_name}: Should have failed")
        except Exception as e:
            print(f"{test_name}: Correctly handled - {type(e).__name__}")
    
    # Demo Summary
    print("\nDEMO SUMMARY")
    print("=" * 60)
    print("This demonstration showcased:")
    print("Object-Oriented Programming concepts")
    print("SOLID principles implementation")
    print("Design patterns (Strategy, Repository, etc.)")
    print("Data validation and error handling")
    print("Business logic implementation")
    print("Search and sorting capabilities")
    print("Professional code structure")
    print("Clean architecture principles")
    print("\nPerfect for demonstrating Python expertise in CV!")
    print("=" * 60)


def quick_demo():
    """Quick demonstration for testing"""
    print("QUICK DEMO")
    print("-" * 30)
    
    library = LibraryService()
    
    # Add a book
    book = library.add_book("Demo Book", "Demo Author", "978-1-234-56789-0")
    print(f"Added book: {book.title}")
    
    # Add a member
    member = library.add_member("John", "Doe", MembershipType.PUBLIC)
    print(f"Added member: {member.full_name}")
    
    # Borrow the book
    transaction = library.borrow_book(member.id, book.id)
    print(f"Borrowed book, due: {transaction.due_date.strftime('%Y-%m-%d')}")
    
    # Show statistics
    stats = library.get_library_statistics()
    print(f"Stats: {stats['books']['total']} books, {stats['members']['total']} members")
    
    print("Quick demo completed!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        demo_library_system()
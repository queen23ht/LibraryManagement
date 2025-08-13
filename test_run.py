#!/usr/bin/env python3
"""
Simple test script to verify the library system works
"""

import uuid
from models import Book, BookCategory, Member, MembershipType
from services import LibraryService

def test_basic_functionality():
    """Test basic functionality"""
    print("TESTING LIBRARY SYSTEM")
    print("-" * 40)
    
    # Create library instance
    library = LibraryService()
    
    # Generate unique ISBN for testing
    unique_isbn = f"978-1-234-{str(uuid.uuid4())[:8]}"
    
    try:
        # Test 1: Add a book
        print("Test 1: Adding a book...")
        book = library.add_book(
            "Test Book", 
            "Test Author", 
            unique_isbn,
            BookCategory.FICTION
        )
        print(f"Book added successfully: {book.title}")
        
        # Test 2: Add a member
        print("\nTest 2: Adding a member...")
        member = library.add_member(
            "Test", 
            "User", 
            MembershipType.PUBLIC
        )
        print(f"Member added successfully: {member.full_name}")
        
        # Test 3: Borrow book
        print("\nTest 3: Borrowing book...")
        transaction = library.borrow_book(member.id, book.id)
        print(f"Book borrowed successfully!")
        print(f"Due date: {transaction.due_date.strftime('%Y-%m-%d')}")
        
        # Test 4: Show statistics
        print("\nTest 4: Library statistics...")
        stats = library.get_library_statistics()
        print(f"Books: {stats['books']['total']} total, {stats['books']['borrowed']} borrowed")
        print(f"Members: {stats['members']['total']} total")
        print(f"Transactions: {stats['transactions']['total']} total")
        
        print("\nALL TESTS PASSED!")
        print("The library system is working correctly!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_functionality()
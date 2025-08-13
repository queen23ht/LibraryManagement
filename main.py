#!/usr/bin/env python3
"""
Main CLI application for the Library Management System.
Demonstrates: CLI design, Menu systems, Error handling, User interaction
"""

import sys
from datetime import datetime, date
from typing import Optional

from models import (
    Book, BookCategory, BookStatus,
    Member, MembershipType, MemberStatus, ContactInfo,
    Transaction, TransactionType
)
from services import LibraryService, LibraryServiceError
from utils import (
    BookFormatter, MemberFormatter, TransactionFormatter, 
    StatisticsFormatter, BookSorter, MemberSorter, SortOrder
)


class LibraryApp:
    """
    Main CLI application class.
    Demonstrates: Command pattern, Menu system, User interaction
    """
    
    def __init__(self):
        self.library = LibraryService()
        self.running = True
    
    def run(self) -> None:
        """Main application loop"""
        self.show_welcome()
        
        while self.running:
            try:
                self.show_main_menu()
                choice = input("\nEnter your choice: ").strip()
                self.handle_main_menu(choice)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def show_welcome(self) -> None:
        """Display welcome message"""
        print("=" * 60)
        print("📚 WELCOME TO LIBRARY MANAGEMENT SYSTEM 📚")
        print("=" * 60)
        print("A comprehensive OOP Python project for CV showcase")
        print("Demonstrates: OOP, Design Patterns, SOLID Principles")
        print("=" * 60)
    
    def show_main_menu(self) -> None:
        """Display main menu"""
        print("\n" + "=" * 40)
        print("📋 MAIN MENU")
        print("=" * 40)
        print("1. 📚 Book Management")
        print("2. 👥 Member Management")
        print("3. 📋 Transaction Management")
        print("4. 📊 Reports & Statistics")
        print("5. 🔍 Search & Browse")
        print("6. ⚙️  System Utilities")
        print("0. 🚪 Exit")
        print("=" * 40)
    
    def handle_main_menu(self, choice: str) -> None:
        """Handle main menu selection"""
        menu_handlers = {
            '1': self.book_menu,
            '2': self.member_menu,
            '3': self.transaction_menu,
            '4': self.reports_menu,
            '5': self.search_menu,
            '6': self.utilities_menu,
            '0': self.exit_app
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
        else:
            print("\n❌ Invalid choice. Please try again.")
    
    def book_menu(self) -> None:
        """Book management menu"""
        while True:
            print("\n" + "=" * 40)
            print("📚 BOOK MANAGEMENT")
            print("=" * 40)
            print("1. ➕ Add New Book")
            print("2. 👀 View Book Details")
            print("3. 📝 Update Book")
            print("4. 🗑️  Delete Book")
            print("5. 📋 List All Books")
            print("6. 🔍 Search Books")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.view_book()
            elif choice == '3':
                self.update_book()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                self.list_books()
            elif choice == '6':
                self.search_books()
            elif choice == '0':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def add_book(self) -> None:
        """Add a new book"""
        print("\n📚 ADD NEW BOOK")
        print("-" * 30)
        
        try:
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            
            # Category selection
            print("\nCategories:")
            categories = list(BookCategory)
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat.value.replace('_', ' ').title()}")
            
            cat_choice = input("\nSelect category (1-{}): ".format(len(categories))).strip()
            try:
                category = categories[int(cat_choice) - 1]
            except (ValueError, IndexError):
                category = BookCategory.OTHER
            
            # Optional fields
            pub_year_str = input("Publication Year (optional): ").strip()
            publication_year = int(pub_year_str) if pub_year_str else None
            
            publisher = input("Publisher (optional): ").strip()
            
            pages_str = input("Pages (optional): ").strip()
            pages = int(pages_str) if pages_str else 0
            
            description = input("Description (optional): ").strip()
            
            # Add book
            book = self.library.add_book(
                title, author, isbn, category, 
                publication_year, publisher, pages, description
            )
            
            print(f"\n✅ Book added successfully!")
            print(BookFormatter.format_book_detail(book))
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        except ValueError as e:
            print(f"\n❌ Invalid input: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_book(self) -> None:
        """View book details"""
        print("\n👀 VIEW BOOK DETAILS")
        print("-" * 30)
        
        book_id = input("Enter Book ID: ").strip()
        
        try:
            book = self.library.get_book(book_id)
            print(BookFormatter.format_book_detail(book))
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def update_book(self) -> None:
        """Update book information"""
        print("\n📝 UPDATE BOOK")
        print("-" * 30)
        
        book_id = input("Enter Book ID: ").strip()
        
        try:
            book = self.library.get_book(book_id)
            print(f"\nCurrent book details:")
            print(BookFormatter.format_book_detail(book))
            
            print(f"\nEnter new values (press Enter to keep current):")
            
            # Get updated values
            updates = {}
            
            new_title = input(f"Title [{book.title}]: ").strip()
            if new_title:
                updates['title'] = new_title
            
            new_author = input(f"Author [{book.author}]: ").strip()
            if new_author:
                updates['author'] = new_author
            
            # Update book
            if updates:
                updated_book = self.library.update_book(book_id, **updates)
                print(f"\n✅ Book updated successfully!")
                print(BookFormatter.format_book_detail(updated_book))
            else:
                print(f"\n📝 No changes made.")
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def delete_book(self) -> None:
        """Delete a book"""
        print("\n🗑️ DELETE BOOK")
        print("-" * 30)
        
        book_id = input("Enter Book ID: ").strip()
        
        try:
            book = self.library.get_book(book_id)
            print(f"\nBook to delete:")
            print(BookFormatter.format_book_summary(book))
            
            confirm = input("\nAre you sure? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                self.library.delete_book(book_id)
                print(f"\n✅ Book deleted successfully!")
            else:
                print(f"\n📝 Deletion cancelled.")
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def list_books(self) -> None:
        """List all books"""
        print("\n📋 ALL BOOKS")
        print("-" * 30)
        
        books = self.library.get_all_books()
        
        if not books:
            print("No books found.")
        else:
            # Sort options
            print("Sort by:")
            print("1. Title")
            print("2. Author")
            print("3. Category")
            print("4. Status")
            
            sort_choice = input("Choose sort option (1-4, default: 1): ").strip()
            
            if sort_choice == '2':
                books = BookSorter.by_author(books)
            elif sort_choice == '3':
                books = BookSorter.by_category(books)
            elif sort_choice == '4':
                books = BookSorter.by_status(books)
            else:
                books = BookSorter.by_title(books)
            
            print(BookFormatter.format_books_table(books))
        
        input("\nPress Enter to continue...")
    
    def search_books(self) -> None:
        """Search books"""
        print("\n🔍 SEARCH BOOKS")
        print("-" * 30)
        
        query = input("Enter search query: ").strip()
        
        # Filter options
        print("\nFilter by status:")
        print("1. All")
        print("2. Available only")
        print("3. Borrowed only")
        
        filter_choice = input("Choose filter (1-3, default: 1): ").strip()
        
        if filter_choice == '2':
            books = self.library.search_books(query, available_only=True)
        elif filter_choice == '3':
            books = self.library.search_books(query, status=BookStatus.BORROWED)
        else:
            books = self.library.search_books(query)
        
        if not books:
            print(f"\n📭 No books found for query: '{query}'")
        else:
            print(f"\n🔍 Found {len(books)} book(s):")
            print(BookFormatter.format_books_table(books))
        
        input("\nPress Enter to continue...")
    
    def member_menu(self) -> None:
        """Member management menu"""
        while True:
            print("\n" + "=" * 40)
            print("👥 MEMBER MANAGEMENT")
            print("=" * 40)
            print("1. ➕ Add New Member")
            print("2. 👀 View Member Details")
            print("3. 📝 Update Member")
            print("4. 🗑️  Delete Member")
            print("5. 📋 List All Members")
            print("6. 🔍 Search Members")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.view_member()
            elif choice == '3':
                self.update_member()
            elif choice == '4':
                self.delete_member()
            elif choice == '5':
                self.list_members()
            elif choice == '6':
                self.search_members()
            elif choice == '0':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def add_member(self) -> None:
        """Add a new member"""
        print("\n👥 ADD NEW MEMBER")
        print("-" * 30)
        
        try:
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            
            # Membership type selection
            print("\nMembership Types:")
            types = list(MembershipType)
            for i, mtype in enumerate(types, 1):
                print(f"{i}. {mtype.value.replace('_', ' ').title()}")
            
            type_choice = input(f"\nSelect type (1-{len(types)}): ").strip()
            try:
                membership_type = types[int(type_choice) - 1]
            except (ValueError, IndexError):
                membership_type = MembershipType.PUBLIC
            
            # Optional fields
            email = input("Email (optional): ").strip()
            phone = input("Phone (optional): ").strip()
            address = input("Address (optional): ").strip()
            student_id = input("Student ID (optional): ").strip()
            
            # Create contact info
            contact_info = ContactInfo(email, phone, address)
            
            # Add member
            member = self.library.add_member(
                first_name, last_name, membership_type,
                contact_info=contact_info, student_id=student_id
            )
            
            print(f"\n✅ Member added successfully!")
            print(MemberFormatter.format_member_detail(member))
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        except ValueError as e:
            print(f"\n❌ Invalid input: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_member(self) -> None:
        """View member details"""
        print("\n👀 VIEW MEMBER DETAILS")
        print("-" * 30)
        
        member_id = input("Enter Member ID: ").strip()
        
        try:
            member = self.library.get_member(member_id)
            print(MemberFormatter.format_member_detail(member))
            
            # Show borrowed books
            if member.borrowed_books:
                print(f"\n📚 Currently Borrowed Books:")
                for book_id in member.borrowed_books:
                    try:
                        book = self.library.get_book(book_id)
                        print(f"  • {BookFormatter.format_book_summary(book)}")
                    except:
                        print(f"  • Book ID: {book_id} (details not available)")
        
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def update_member(self) -> None:
        """Update member information"""
        print("\n📝 UPDATE MEMBER")
        print("-" * 30)
        
        member_id = input("Enter Member ID: ").strip()
        
        try:
            member = self.library.get_member(member_id)
            print(f"\nCurrent member details:")
            print(MemberFormatter.format_member_detail(member))
            
            print(f"\nEnter new values (press Enter to keep current):")
            
            updates = {}
            
            new_first = input(f"First Name [{member.first_name}]: ").strip()
            if new_first:
                updates['first_name'] = new_first
            
            new_last = input(f"Last Name [{member.last_name}]: ").strip()
            if new_last:
                updates['last_name'] = new_last
            
            if updates:
                updated_member = self.library.update_member(member_id, **updates)
                print(f"\n✅ Member updated successfully!")
                print(MemberFormatter.format_member_detail(updated_member))
            else:
                print(f"\n📝 No changes made.")
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def delete_member(self) -> None:
        """Delete a member"""
        print("\n🗑️ DELETE MEMBER")
        print("-" * 30)
        
        member_id = input("Enter Member ID: ").strip()
        
        try:
            member = self.library.get_member(member_id)
            print(f"\nMember to delete:")
            print(MemberFormatter.format_member_summary(member))
            
            confirm = input("\nAre you sure? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                self.library.delete_member(member_id)
                print(f"\n✅ Member deleted successfully!")
            else:
                print(f"\n📝 Deletion cancelled.")
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def list_members(self) -> None:
        """List all members"""
        print("\n📋 ALL MEMBERS")
        print("-" * 30)
        
        members = self.library.get_all_members()
        
        if not members:
            print("No members found.")
        else:
            print("Sort by:")
            print("1. Name")
            print("2. Membership Type")
            print("3. Join Date")
            
            sort_choice = input("Choose sort option (1-3, default: 1): ").strip()
            
            if sort_choice == '2':
                members = MemberSorter.by_membership_type(members)
            elif sort_choice == '3':
                members = MemberSorter.by_join_date(members)
            else:
                members = MemberSorter.by_name(members)
            
            print(MemberFormatter.format_members_table(members))
        
        input("\nPress Enter to continue...")
    
    def search_members(self) -> None:
        """Search members"""
        print("\n🔍 SEARCH MEMBERS")
        print("-" * 30)
        
        query = input("Enter search query: ").strip()
        
        members = self.library.search_members(query)
        
        if not members:
            print(f"\n📭 No members found for query: '{query}'")
        else:
            print(f"\n🔍 Found {len(members)} member(s):")
            print(MemberFormatter.format_members_table(members))
        
        input("\nPress Enter to continue...")
    
    def transaction_menu(self) -> None:
        """Transaction management menu"""
        while True:
            print("\n" + "=" * 40)
            print("📋 TRANSACTION MANAGEMENT")
            print("=" * 40)
            print("1. 📤 Borrow Book")
            print("2. 📥 Return Book")
            print("3. 🔄 Renew Book")
            print("4. 💰 Pay Fine")
            print("5. 📋 View Member Transactions")
            print("6. ⚠️  View Overdue Books")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.borrow_book()
            elif choice == '2':
                self.return_book()
            elif choice == '3':
                self.renew_book()
            elif choice == '4':
                self.pay_fine()
            elif choice == '5':
                self.view_member_transactions()
            elif choice == '6':
                self.view_overdue_books()
            elif choice == '0':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def borrow_book(self) -> None:
        """Borrow a book"""
        print("\n📤 BORROW BOOK")
        print("-" * 30)
        
        member_id = input("Member ID: ").strip()
        book_id = input("Book ID: ").strip()
        
        try:
            transaction = self.library.borrow_book(member_id, book_id)
            print(f"\n✅ Book borrowed successfully!")
            print(TransactionFormatter.format_transaction_detail(transaction))
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def return_book(self) -> None:
        """Return a book"""
        print("\n📥 RETURN BOOK")
        print("-" * 30)
        
        member_id = input("Member ID: ").strip()
        book_id = input("Book ID: ").strip()
        
        try:
            transaction, fine = self.library.return_book(member_id, book_id)
            print(f"\n✅ Book returned successfully!")
            print(TransactionFormatter.format_transaction_detail(transaction))
            
            if fine > 0:
                print(f"\n💰 Fine applied: ${fine:.2f}")
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def renew_book(self) -> None:
        """Renew a book"""
        print("\n🔄 RENEW BOOK")
        print("-" * 30)
        
        member_id = input("Member ID: ").strip()
        book_id = input("Book ID: ").strip()
        
        try:
            transaction = self.library.renew_book(member_id, book_id)
            print(f"\n✅ Book renewed successfully!")
            print(TransactionFormatter.format_transaction_detail(transaction))
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def pay_fine(self) -> None:
        """Pay member fine"""
        print("\n💰 PAY FINE")
        print("-" * 30)
        
        member_id = input("Member ID: ").strip()
        
        try:
            member = self.library.get_member(member_id)
            print(f"\nMember: {member.full_name}")
            print(f"Current fine: ${member.fine_amount:.2f}")
            
            if member.fine_amount == 0:
                print("\n✅ No outstanding fines!")
                input("\nPress Enter to continue...")
                return
            
            amount_str = input(f"\nEnter payment amount: $").strip()
            amount = float(amount_str)
            
            transaction = self.library.pay_fine(member_id, amount)
            print(f"\n✅ Payment processed successfully!")
            print(TransactionFormatter.format_transaction_detail(transaction))
            
            # Show remaining fine
            updated_member = self.library.get_member(member_id)
            if updated_member.fine_amount > 0:
                print(f"\nRemaining fine: ${updated_member.fine_amount:.2f}")
            else:
                print(f"\n🎉 All fines paid!")
            
        except (LibraryServiceError, ValueError) as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_member_transactions(self) -> None:
        """View member transaction history"""
        print("\n📋 MEMBER TRANSACTIONS")
        print("-" * 30)
        
        member_id = input("Enter Member ID: ").strip()
        
        try:
            member = self.library.get_member(member_id)
            transactions = self.library.get_member_transactions(member_id)
            
            print(f"\nTransactions for: {member.full_name}")
            
            if not transactions:
                print("No transactions found.")
            else:
                print(TransactionFormatter.format_transactions_table(transactions))
            
        except LibraryServiceError as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_overdue_books(self) -> None:
        """View overdue books"""
        print("\n⚠️ OVERDUE BOOKS")
        print("-" * 30)
        
        overdue_items = self.library.get_overdue_books()
        
        if not overdue_items:
            print("📅 No overdue books!")
        else:
            print(StatisticsFormatter.format_overdue_report(overdue_items))
        
        input("\nPress Enter to continue...")
    
    def reports_menu(self) -> None:
        """Reports and statistics menu"""
        while True:
            print("\n" + "=" * 40)
            print("📊 REPORTS & STATISTICS")
            print("=" * 40)
            print("1. 📊 Library Statistics")
            print("2. ⚠️  Overdue Books Report")
            print("3. 👥 Member Activity Report")
            print("4. 📚 Popular Books Report")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.show_statistics()
            elif choice == '2':
                self.view_overdue_books()
            elif choice == '3':
                self.member_activity_report()
            elif choice == '4':
                self.popular_books_report()
            elif choice == '0':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def show_statistics(self) -> None:
        """Show library statistics"""
        print("\n📊 LIBRARY STATISTICS")
        print("-" * 30)
        
        stats = self.library.get_library_statistics()
        print(StatisticsFormatter.format_statistics(stats))
        
        input("\nPress Enter to continue...")
    
    def member_activity_report(self) -> None:
        """Show member activity report"""
        print("\n👥 MEMBER ACTIVITY REPORT")
        print("-" * 30)
        
        members = self.library.get_all_members()
        
        # Filter active members with borrowed books
        active_members = [m for m in members if m.borrowed_books_count > 0]
        
        if not active_members:
            print("No members with borrowed books.")
        else:
            # Sort by number of borrowed books
            active_members = MemberSorter.by_borrowed_books_count(active_members, SortOrder.DESC)
            print(MemberFormatter.format_members_table(active_members[:10]))  # Top 10
        
        input("\nPress Enter to continue...")
    
    def popular_books_report(self) -> None:
        """Show popular books report"""
        print("\n📚 POPULAR BOOKS REPORT")
        print("-" * 30)
        
        books = self.library.get_all_books()
        
        # Sort by popularity (borrow history length)
        popular_books = BookSorter.by_popularity(books, SortOrder.DESC)
        
        # Show top 10
        top_books = popular_books[:10]
        
        if not top_books:
            print("No books found.")
        else:
            print("Top 10 Most Borrowed Books:")
            print(BookFormatter.format_books_table(top_books))
        
        input("\nPress Enter to continue...")
    
    def search_menu(self) -> None:
        """Search and browse menu"""
        print("\n🔍 SEARCH & BROWSE")
        print("-" * 30)
        print("This functionality is integrated into the main menus.")
        print("Use the search options in Book and Member management.")
        
        input("\nPress Enter to continue...")
    
    def utilities_menu(self) -> None:
        """System utilities menu"""
        while True:
            print("\n" + "=" * 40)
            print("⚙️ SYSTEM UTILITIES")
            print("=" * 40)
            print("1. 🧪 Create Sample Data")
            print("2. 📁 Data Management")
            print("3. ℹ️  System Information")
            print("0. ⬅️  Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.create_sample_data()
            elif choice == '2':
                self.data_management()
            elif choice == '3':
                self.system_info()
            elif choice == '0':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def create_sample_data(self) -> None:
        """Create sample data for testing"""
        print("\n🧪 CREATE SAMPLE DATA")
        print("-" * 30)
        
        try:
            # Sample books
            books_data = [
                ("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5", BookCategory.FICTION),
                ("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4", BookCategory.FICTION),
                ("Python Programming", "John Smith", "978-1-234-56789-0", BookCategory.TECHNOLOGY),
                ("Data Science Handbook", "Jane Doe", "978-9-876-54321-0", BookCategory.SCIENCE),
                ("World History", "Robert Johnson", "978-5-555-55555-5", BookCategory.HISTORY)
            ]
            
            print("Creating sample books...")
            for title, author, isbn, category in books_data:
                try:
                    self.library.add_book(title, author, isbn, category)
                    print(f"  ✅ Added: {title}")
                except LibraryServiceError:
                    print(f"  ⚠️  Skipped: {title} (already exists)")
            
            # Sample members
            members_data = [
                ("John", "Doe", MembershipType.STUDENT),
                ("Jane", "Smith", MembershipType.FACULTY),
                ("Bob", "Wilson", MembershipType.STAFF),
                ("Alice", "Brown", MembershipType.PUBLIC)
            ]
            
            print("\nCreating sample members...")
            for first, last, mtype in members_data:
                try:
                    member = self.library.add_member(first, last, mtype)
                    print(f"  ✅ Added: {first} {last}")
                except LibraryServiceError:
                    print(f"  ⚠️  Error adding: {first} {last}")
            
            print(f"\n✅ Sample data created successfully!")
            
        except Exception as e:
            print(f"\n❌ Error creating sample data: {e}")
        
        input("\nPress Enter to continue...")
    
    def data_management(self) -> None:
        """Data management utilities"""
        print("\n📁 DATA MANAGEMENT")
        print("-" * 30)
        print("Data is automatically saved to JSON files in the 'data' directory.")
        print("Files: books.json, members.json, transactions.json")
        
        input("\nPress Enter to continue...")
    
    def system_info(self) -> None:
        """Show system information"""
        print("\nℹSYSTEM INFORMATION")
        print("-" * 30)
        print("Library Management System v1.0")
        print("Python OOP Demonstration Project")
        print("\nFeatures:")
        print("• Object-Oriented Programming")
        print("• SOLID Principles")
        print("• Design Patterns")
        print("• Data Validation")
        print("• Search & Sorting")
        print("• Transaction Management")
        print("• Report Generation")
        
        stats = self.library.get_library_statistics()
        print(f"\nCurrent Data:")
        print(f"• Books: {stats['books']['total']}")
        print(f"• Members: {stats['members']['total']}")
        print(f"• Transactions: {stats['transactions']['total']}")
        
        input("\nPress Enter to continue...")
    
    def exit_app(self) -> None:
        print("\n👋 Thank you for using Library Management System!")
        self.running = False


def main():
    """Main function"""
    try:
        app = LibraryApp()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("Please check your Python environment and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
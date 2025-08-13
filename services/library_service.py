"""
Library Service - Main business logic layer.
Demonstrates: Service Pattern, CRUD operations, Business rules, Exception handling
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional, Tuple
import json
import os
from pathlib import Path

from models import (
    Book, BookStatus, BookCategory,
    Member, MembershipType, MemberStatus,
    Transaction, TransactionType, TransactionStatus
)


class LibraryServiceError(Exception):
    """Base exception for library service errors"""
    pass


class BookNotFoundError(LibraryServiceError):
    """Raised when a book is not found"""
    pass


class MemberNotFoundError(LibraryServiceError):
    """Raised when a member is not found"""
    pass


class TransactionError(LibraryServiceError):
    """Raised when transaction operation fails"""
    pass


class LibraryService:
    """
    Main service class for library operations.
    Demonstrates: Repository pattern, Business logic separation, Data persistence
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # In-memory storage (in production, this would be a database)
        self._books: Dict[str, Book] = {}
        self._members: Dict[str, Member] = {}
        self._transactions: Dict[str, Transaction] = {}
        
        # Configuration
        self.default_borrow_days = 14
        self.max_renewals = 2
        self.daily_fine_rate = 1.0
        self.max_fine_amount = 50.0
        
        # Load existing data
        self._load_data()
    
    def _get_file_path(self, filename: str) -> Path:
        """Get full file path for data file"""
        return self.data_dir / filename
    
    def _save_data(self) -> None:
        """Save all data to JSON files"""
        try:
            # Save books
            books_data = {book_id: book.to_dict() for book_id, book in self._books.items()}
            with open(self._get_file_path("books.json"), 'w', encoding='utf-8') as f:
                json.dump(books_data, f, indent=2, ensure_ascii=False)
            
            # Save members
            members_data = {member_id: member.to_dict() for member_id, member in self._members.items()}
            with open(self._get_file_path("members.json"), 'w', encoding='utf-8') as f:
                json.dump(members_data, f, indent=2, ensure_ascii=False)
            
            # Save transactions
            transactions_data = {trans_id: trans.to_dict() for trans_id, trans in self._transactions.items()}
            with open(self._get_file_path("transactions.json"), 'w', encoding='utf-8') as f:
                json.dump(transactions_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            raise LibraryServiceError(f"Failed to save data: {str(e)}")
    
    def _load_data(self) -> None:
        """Load data from JSON files"""
        try:
            # Load books
            books_file = self._get_file_path("books.json")
            if books_file.exists():
                with open(books_file, 'r', encoding='utf-8') as f:
                    books_data = json.load(f)
                    for book_id, book_dict in books_data.items():
                        book = Book("", "", "").from_dict(book_dict)
                        self._books[book_id] = book
            
            # Load members
            members_file = self._get_file_path("members.json")
            if members_file.exists():
                with open(members_file, 'r', encoding='utf-8') as f:
                    members_data = json.load(f)
                    for member_id, member_dict in members_data.items():
                        member = Member("", "").from_dict(member_dict)
                        self._members[member_id] = member
            
            # Load transactions
            transactions_file = self._get_file_path("transactions.json")
            if transactions_file.exists():
                with open(transactions_file, 'r', encoding='utf-8') as f:
                    transactions_data = json.load(f)
                    for trans_id, trans_dict in transactions_data.items():
                        transaction = Transaction("", TransactionType.BORROW).from_dict(trans_dict)
                        self._transactions[trans_id] = transaction
        
        except Exception as e:
            raise LibraryServiceError(f"Failed to load data: {str(e)}")
    
    # Book Management
    def add_book(self, title: str, author: str, isbn: str, 
                 category: BookCategory = BookCategory.OTHER,
                 publication_year: int = None, publisher: str = "",
                 pages: int = 0, description: str = "") -> Book:
        """Add a new book to the library"""
        # Check if ISBN already exists
        for book in self._books.values():
            if book.isbn == isbn:
                raise LibraryServiceError(f"Book with ISBN {isbn} already exists")
        
        book = Book(title, author, isbn, category, publication_year, 
                   publisher, pages, description)
        
        if not book.validate():
            errors = book.get_validation_errors()
            raise LibraryServiceError(f"Book validation failed: {', '.join(errors)}")
        
        self._books[book.id] = book
        self._save_data()
        return book
    
    def get_book(self, book_id: str) -> Book:
        """Get a book by ID"""
        if book_id not in self._books:
            raise BookNotFoundError(f"Book with ID {book_id} not found")
        return self._books[book_id]
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN"""
        for book in self._books.values():
            if book.isbn == isbn:
                return book
        return None
    
    def update_book(self, book_id: str, **kwargs) -> Book:
        """Update book information"""
        book = self.get_book(book_id)
        
        # Update allowed fields
        updatable_fields = [
            'title', 'author', 'category', 'publication_year',
            'publisher', 'pages', 'description'
        ]
        
        for field, value in kwargs.items():
            if field in updatable_fields and hasattr(book, field):
                setattr(book, field, value)
        
        if not book.validate():
            errors = book.get_validation_errors()
            raise LibraryServiceError(f"Book validation failed: {', '.join(errors)}")
        
        self._save_data()
        return book
    
    def delete_book(self, book_id: str) -> bool:
        """Delete a book (only if not borrowed)"""
        book = self.get_book(book_id)
        
        if book.status == BookStatus.BORROWED:
            raise LibraryServiceError("Cannot delete a borrowed book")
        
        # Check for pending transactions
        pending_transactions = [
            t for t in self._transactions.values()
            if t.book_id == book_id and t.status == TransactionStatus.PENDING
        ]
        
        if pending_transactions:
            raise LibraryServiceError("Cannot delete book with pending transactions")
        
        del self._books[book_id]
        self._save_data()
        return True
    
    def search_books(self, query: str = "", category: BookCategory = None,
                    status: BookStatus = None, available_only: bool = False) -> List[Book]:
        """Search books with various filters"""
        results = list(self._books.values())
        
        if query:
            results = [book for book in results if book.matches_search(query)]
        
        if category:
            results = [book for book in results if book.category == category]
        
        if status:
            results = [book for book in results if book.status == status]
        
        if available_only:
            results = [book for book in results if book.is_available()]
        
        return sorted(results, key=lambda b: b.title)
    
    def get_all_books(self) -> List[Book]:
        """Get all books"""
        return sorted(self._books.values(), key=lambda b: b.title)
    
    # Member Management
    def add_member(self, first_name: str, last_name: str,
                  membership_type: MembershipType = MembershipType.PUBLIC,
                  **kwargs) -> Member:
        """Add a new member to the library"""
        member = Member(first_name, last_name, membership_type, **kwargs)
        
        if not member.validate():
            errors = member.get_validation_errors()
            raise LibraryServiceError(f"Member validation failed: {', '.join(errors)}")
        
        self._members[member.id] = member
        self._save_data()
        return member
    
    def get_member(self, member_id: str) -> Member:
        """Get a member by ID"""
        if member_id not in self._members:
            raise MemberNotFoundError(f"Member with ID {member_id} not found")
        return self._members[member_id]
    
    def update_member(self, member_id: str, **kwargs) -> Member:
        """Update member information"""
        member = self.get_member(member_id)
        
        # Update allowed fields
        updatable_fields = [
            'first_name', 'last_name', 'membership_type', 'date_of_birth',
            'student_id', 'contact_info'
        ]
        
        for field, value in kwargs.items():
            if field in updatable_fields and hasattr(member, field):
                setattr(member, field, value)
        
        if not member.validate():
            errors = member.get_validation_errors()
            raise LibraryServiceError(f"Member validation failed: {', '.join(errors)}")
        
        self._save_data()
        return member
    
    def delete_member(self, member_id: str) -> bool:
        """Delete a member (only if no borrowed books or fines)"""
        member = self.get_member(member_id)
        
        if member.borrowed_books_count > 0:
            raise LibraryServiceError("Cannot delete member with borrowed books")
        
        if member.fine_amount > 0:
            raise LibraryServiceError("Cannot delete member with outstanding fines")
        
        del self._members[member_id]
        self._save_data()
        return True
    
    def search_members(self, query: str = "", membership_type: MembershipType = None,
                      status: MemberStatus = None) -> List[Member]:
        """Search members with various filters"""
        results = list(self._members.values())
        
        if query:
            results = [member for member in results if member.matches_search(query)]
        
        if membership_type:
            results = [member for member in results if member.membership_type == membership_type]
        
        if status:
            results = [member for member in results if member.status == status]
        
        return sorted(results, key=lambda m: m.full_name)
    
    def get_all_members(self) -> List[Member]:
        """Get all members"""
        return sorted(self._members.values(), key=lambda m: m.full_name)
    
    # Transaction Management
    def borrow_book(self, member_id: str, book_id: str, 
                   processed_by: str = "system") -> Transaction:
        """Borrow a book"""
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        # Check if member can borrow books
        if not member.can_borrow_books():
            reasons = []
            if not member.is_active():
                reasons.append("member is not active")
            if not member.is_membership_valid():
                reasons.append("membership has expired")
            if member.borrowed_books_count >= member.max_books_allowed:
                reasons.append("maximum book limit reached")
            if member.fine_amount > 0:
                reasons.append("outstanding fines must be paid")
            
            raise TransactionError(f"Cannot borrow book: {', '.join(reasons)}")
        
        # Check if book is available
        if not book.is_available():
            raise TransactionError(f"Book is not available (status: {book.status.value})")
        
        # Create transaction
        due_date = datetime.now() + timedelta(days=self.default_borrow_days)
        transaction = Transaction(member_id, TransactionType.BORROW, book_id, due_date=due_date)
        
        # Process the transaction
        if not transaction.process_transaction(processed_by):
            raise TransactionError("Failed to process borrow transaction")
        
        # Update book and member
        if not book.borrow(member_id, due_date):
            raise TransactionError("Failed to update book status")
        
        if not member.borrow_book(book_id):
            # Rollback book status
            book.return_book()
            raise TransactionError("Failed to update member borrowed books")
        
        self._transactions[transaction.id] = transaction
        self._save_data()
        return transaction
    
    def return_book(self, member_id: str, book_id: str,
                   processed_by: str = "system") -> Tuple[Transaction, float]:
        """Return a book and calculate any fines"""
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        # Check if member has this book
        if book_id not in member.borrowed_books:
            raise TransactionError("Member does not have this book borrowed")
        
        # Check if book is borrowed by this member
        if book.borrowed_by != member_id:
            raise TransactionError("Book is not borrowed by this member")
        
        # Create return transaction
        transaction = Transaction(member_id, TransactionType.RETURN, book_id)
        
        # Process the transaction
        if not transaction.process_transaction(processed_by):
            raise TransactionError("Failed to process return transaction")
        
        # Calculate fine
        fine_amount = transaction.calculate_fine(self.daily_fine_rate)
        if fine_amount > 0:
            member.add_fine(fine_amount, f"Overdue return for book: {book.title}")
            transaction._fine_amount = fine_amount
        
        # Update book and member
        if not book.return_book():
            raise TransactionError("Failed to update book status")
        
        if not member.return_book(book_id):
            raise TransactionError("Failed to update member borrowed books")
        
        self._transactions[transaction.id] = transaction
        self._save_data()
        return transaction, fine_amount
    
    def renew_book(self, member_id: str, book_id: str,
                  processed_by: str = "system") -> Transaction:
        """Renew a borrowed book"""
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        # Check if member has this book
        if book_id not in member.borrowed_books:
            raise TransactionError("Member does not have this book borrowed")
        
        # Check if book is not overdue
        if book.due_date and datetime.now() > book.due_date:
            raise TransactionError("Cannot renew overdue book")
        
        # Check renewal limit
        renewal_count = len([
            t for t in self._transactions.values()
            if (t.member_id == member_id and t.book_id == book_id and 
                t.transaction_type == TransactionType.RENEW and 
                t.status == TransactionStatus.COMPLETED)
        ])
        
        if renewal_count >= self.max_renewals:
            raise TransactionError(f"Maximum renewals ({self.max_renewals}) reached")
        
        # Create renewal transaction
        new_due_date = book.due_date + timedelta(days=self.default_borrow_days)
        transaction = Transaction(member_id, TransactionType.RENEW, book_id, due_date=new_due_date)
        
        # Process the transaction
        if not transaction.process_transaction(processed_by):
            raise TransactionError("Failed to process renewal transaction")
        
        # Update book due date
        book._due_date = new_due_date
        book._update_timestamp()
        
        self._transactions[transaction.id] = transaction
        self._save_data()
        return transaction
    
    def pay_fine(self, member_id: str, amount: float,
                processed_by: str = "system") -> Transaction:
        """Pay member's fine"""
        member = self.get_member(member_id)
        
        if amount <= 0:
            raise TransactionError("Payment amount must be positive")
        
        if amount > member.fine_amount:
            raise TransactionError("Payment amount exceeds fine amount")
        
        # Create payment transaction
        transaction = Transaction(member_id, TransactionType.FINE_PAYMENT, amount=amount)
        
        # Process the transaction
        if not transaction.process_transaction(processed_by):
            raise TransactionError("Failed to process payment transaction")
        
        # Update member fine
        remaining_fine = member.pay_fine(amount)
        
        self._transactions[transaction.id] = transaction
        self._save_data()
        return transaction
    
    def get_member_transactions(self, member_id: str) -> List[Transaction]:
        """Get all transactions for a member"""
        return [
            t for t in self._transactions.values()
            if t.member_id == member_id
        ]
    
    def get_overdue_books(self) -> List[Tuple[Book, Member, Transaction]]:
        """Get all overdue books with member and transaction info"""
        overdue_items = []
        
        for book in self._books.values():
            if (book.status == BookStatus.BORROWED and 
                book.due_date and datetime.now() > book.due_date):
                
                member = self.get_member(book.borrowed_by)
                
                # Find the borrow transaction
                borrow_transaction = None
                for transaction in self._transactions.values():
                    if (transaction.member_id == member.id and
                        transaction.book_id == book.id and
                        transaction.transaction_type == TransactionType.BORROW and
                        transaction.status == TransactionStatus.COMPLETED):
                        borrow_transaction = transaction
                        break
                
                if borrow_transaction:
                    overdue_items.append((book, member, borrow_transaction))
        
        return overdue_items
    
    def get_library_statistics(self) -> Dict[str, Any]:
        """Get library statistics"""
        total_books = len(self._books)
        available_books = len([b for b in self._books.values() if b.is_available()])
        borrowed_books = len([b for b in self._books.values() if b.status == BookStatus.BORROWED])
        
        total_members = len(self._members)
        active_members = len([m for m in self._members.values() if m.is_active()])
        
        overdue_books = len(self.get_overdue_books())
        total_fines = sum(m.fine_amount for m in self._members.values())
        
        transactions_today = len([
            t for t in self._transactions.values()
            if t.created_at.date() == date.today()
        ])
        
        return {
            'books': {
                'total': total_books,
                'available': available_books,
                'borrowed': borrowed_books,
                'overdue': overdue_books
            },
            'members': {
                'total': total_members,
                'active': active_members
            },
            'finances': {
                'total_fines': total_fines
            },
            'transactions': {
                'today': transactions_today,
                'total': len(self._transactions)
            }
        }
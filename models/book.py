"""
Book model for the Library Management System.
Demonstrates: Inheritance, Encapsulation, Data Validation
"""

from datetime import datetime
from typing import Dict, Any, List
from enum import Enum
from .base import BaseEntity, Searchable, Validatable


class BookStatus(Enum):
    """Book availability status"""
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    LOST = "lost"


class BookCategory(Enum):
    """Book categories"""
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    SCIENCE = "science"
    HISTORY = "history"
    BIOGRAPHY = "biography"
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    CHILDREN = "children"
    OTHER = "other"


class Book(BaseEntity, Searchable, Validatable):
    """
    Book entity representing a book in the library.
    Demonstrates: Multiple inheritance, Property decorators, Validation
    """
    
    def __init__(self, title: str, author: str, isbn: str, 
                 category: BookCategory = BookCategory.OTHER,
                 publication_year: int = None, publisher: str = "",
                 pages: int = 0, description: str = ""):
        super().__init__()
        self._title = title.strip()
        self._author = author.strip()
        self._isbn = isbn.strip()
        self._category = category
        self._publication_year = publication_year
        self._publisher = publisher.strip()
        self._pages = pages
        self._description = description.strip()
        self._status = BookStatus.AVAILABLE
        self._borrowed_by = None
        self._borrowed_date = None
        self._due_date = None
        self._borrow_history: List[Dict] = []
    
    # Property decorators for encapsulation
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
        self._update_timestamp()
    
    @property
    def author(self) -> str:
        return self._author
    
    @author.setter
    def author(self, value: str):
        if not value or not value.strip():
            raise ValueError("Author cannot be empty")
        self._author = value.strip()
        self._update_timestamp()
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @isbn.setter
    def isbn(self, value: str):
        if not value or not value.strip():
            raise ValueError("ISBN cannot be empty")
        self._isbn = value.strip()
        self._update_timestamp()
    
    @property
    def category(self) -> BookCategory:
        return self._category
    
    @category.setter
    def category(self, value: BookCategory):
        if not isinstance(value, BookCategory):
            raise TypeError("Category must be a BookCategory enum")
        self._category = value
        self._update_timestamp()
    
    @property
    def publication_year(self) -> int:
        return self._publication_year
    
    @publication_year.setter
    def publication_year(self, value: int):
        current_year = datetime.now().year
        if value and (value < 0 or value > current_year):
            raise ValueError(f"Publication year must be between 0 and {current_year}")
        self._publication_year = value
        self._update_timestamp()
    
    @property
    def publisher(self) -> str:
        return self._publisher
    
    @publisher.setter
    def publisher(self, value: str):
        self._publisher = value.strip() if value else ""
        self._update_timestamp()
    
    @property
    def pages(self) -> int:
        return self._pages
    
    @pages.setter
    def pages(self, value: int):
        if value < 0:
            raise ValueError("Pages cannot be negative")
        self._pages = value
        self._update_timestamp()
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else ""
        self._update_timestamp()
    
    @property
    def status(self) -> BookStatus:
        return self._status
    
    @property
    def borrowed_by(self) -> str:
        return self._borrowed_by
    
    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date
    
    @property
    def due_date(self) -> datetime:
        return self._due_date
    
    @property
    def borrow_history(self) -> List[Dict]:
        return self._borrow_history.copy()  # Return copy to prevent external modification
    
    def is_available(self) -> bool:
        """Check if book is available for borrowing"""
        return self._status == BookStatus.AVAILABLE
    
    def borrow(self, member_id: str, due_date: datetime) -> bool:
        """
        Borrow the book to a member.
        Returns True if successful, False otherwise.
        """
        if not self.is_available():
            return False
        
        self._status = BookStatus.BORROWED
        self._borrowed_by = member_id
        self._borrowed_date = datetime.now()
        self._due_date = due_date
        self._update_timestamp()
        return True
    
    def return_book(self) -> bool:
        """
        Return the book.
        Returns True if successful, False otherwise.
        """
        if self._status != BookStatus.BORROWED:
            return False
        
        # Add to history
        self._borrow_history.append({
            'member_id': self._borrowed_by,
            'borrowed_date': self._borrowed_date,
            'returned_date': datetime.now(),
            'due_date': self._due_date,
            'was_overdue': datetime.now() > self._due_date if self._due_date else False
        })
        
        self._status = BookStatus.AVAILABLE
        self._borrowed_by = None
        self._borrowed_date = None
        self._due_date = None
        self._update_timestamp()
        return True
    
    def set_status(self, status: BookStatus) -> bool:
        """Set book status (for maintenance, lost, etc.)"""
        if self._status == BookStatus.BORROWED and status != BookStatus.AVAILABLE:
            return False  # Cannot change status while borrowed
        
        self._status = status
        if status == BookStatus.AVAILABLE:
            self._borrowed_by = None
            self._borrowed_date = None
            self._due_date = None
        self._update_timestamp()
        return True
    
    def matches_search(self, query: str) -> bool:
        """Check if book matches search query"""
        query = query.lower().strip()
        if not query:
            return True
        
        searchable_fields = [
            self._title.lower(),
            self._author.lower(),
            self._isbn.lower(),
            self._publisher.lower(),
            self._description.lower(),
            self._category.value.lower()
        ]
        
        return any(query in field for field in searchable_fields)
    
    def validate(self) -> bool:
        """Validate book data"""
        return len(self.get_validation_errors()) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors"""
        errors = []
        
        if not self._title or not self._title.strip():
            errors.append("Title is required")
        
        if not self._author or not self._author.strip():
            errors.append("Author is required")
        
        if not self._isbn or not self._isbn.strip():
            errors.append("ISBN is required")
        
        if self._publication_year:
            current_year = datetime.now().year
            if self._publication_year < 0 or self._publication_year > current_year:
                errors.append(f"Publication year must be between 0 and {current_year}")
        
        if self._pages < 0:
            errors.append("Pages cannot be negative")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert book to dictionary representation"""
        return {
            'id': self.id,
            'title': self._title,
            'author': self._author,
            'isbn': self._isbn,
            'category': self._category.value,
            'publication_year': self._publication_year,
            'publisher': self._publisher,
            'pages': self._pages,
            'description': self._description,
            'status': self._status.value,
            'borrowed_by': self._borrowed_by,
            'borrowed_date': self._borrowed_date.isoformat() if self._borrowed_date else None,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'borrow_history': self._borrow_history,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'Book':
        """Create book from dictionary data"""
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            category=BookCategory(data.get('category', BookCategory.OTHER.value)),
            publication_year=data.get('publication_year'),
            publisher=data.get('publisher', ''),
            pages=data.get('pages', 0),
            description=data.get('description', '')
        )
        
        book._id = data['id']
        book._status = BookStatus(data.get('status', BookStatus.AVAILABLE.value))
        book._borrowed_by = data.get('borrowed_by')
        
        if data.get('borrowed_date'):
            book._borrowed_date = datetime.fromisoformat(data['borrowed_date'])
        if data.get('due_date'):
            book._due_date = datetime.fromisoformat(data['due_date'])
        
        book._borrow_history = data.get('borrow_history', [])
        
        if data.get('created_at'):
            book._created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            book._updated_at = datetime.fromisoformat(data['updated_at'])
        
        return book
    
    def __str__(self) -> str:
        """String representation of book"""
        return f"Book(title='{self._title}', author='{self._author}', isbn='{self._isbn}', status='{self._status.value}')"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Book(id='{self.id}', title='{self._title}', author='{self._author}', "
                f"isbn='{self._isbn}', category='{self._category.value}', status='{self._status.value}')")
"""
Member model for the Library Management System.
Demonstrates: Inheritance, Encapsulation, Data Validation, Composition
"""

from datetime import datetime, date
from typing import Dict, Any, List, Optional
from enum import Enum
import re
from .base import BaseEntity, Searchable, Validatable


class MembershipType(Enum):
    """Membership types with different privileges"""
    STUDENT = "student"
    FACULTY = "faculty"
    STAFF = "staff"
    PUBLIC = "public"
    PREMIUM = "premium"


class MemberStatus(Enum):
    """Member account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    BLOCKED = "blocked"


class ContactInfo:
    """
    Contact information class.
    Demonstrates: Composition pattern, Data encapsulation
    """
    
    def __init__(self, email: str = "", phone: str = "", address: str = ""):
        self._email = email.strip()
        self._phone = phone.strip()
        self._address = address.strip()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if value and not self._is_valid_email(value):
            raise ValueError("Invalid email format")
        self._email = value.strip() if value else ""
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        if value and not self._is_valid_phone(value):
            raise ValueError("Invalid phone format")
        self._phone = value.strip() if value else ""
    
    @property
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, value: str):
        self._address = value.strip() if value else ""
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone format (basic validation)"""
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it contains only digits and has reasonable length
        return cleaned.isdigit() and 10 <= len(cleaned) <= 15
    
    def to_dict(self) -> Dict[str, str]:
        """Convert contact info to dictionary"""
        return {
            'email': self._email,
            'phone': self._phone,
            'address': self._address
        }
    
    def from_dict(self, data: Dict[str, str]) -> 'ContactInfo':
        """Create contact info from dictionary"""
        return ContactInfo(
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )


class Member(BaseEntity, Searchable, Validatable):
    """
    Member entity representing a library member.
    Demonstrates: Composition, Property validation, Business logic
    """
    
    def __init__(self, first_name: str, last_name: str, 
                 membership_type: MembershipType = MembershipType.PUBLIC,
                 date_of_birth: date = None, student_id: str = "",
                 contact_info: ContactInfo = None):
        super().__init__()
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._membership_type = membership_type
        self._date_of_birth = date_of_birth
        self._student_id = student_id.strip()
        self._contact_info = contact_info or ContactInfo()
        self._status = MemberStatus.ACTIVE
        self._membership_start_date = datetime.now().date()
        self._membership_end_date = self._calculate_membership_end_date()
        self._borrowed_books: List[str] = []  # List of book IDs
        self._reservation_history: List[Dict] = []
        self._fine_amount = 0.0
        self._max_books_allowed = self._get_max_books_for_type()
    
    def _calculate_membership_end_date(self) -> date:
        """Calculate membership end date based on type"""
        start_date = self._membership_start_date
        if self._membership_type == MembershipType.STUDENT:
            return date(start_date.year + 1, start_date.month, start_date.day)
        elif self._membership_type == MembershipType.FACULTY:
            return date(start_date.year + 3, start_date.month, start_date.day)
        elif self._membership_type == MembershipType.STAFF:
            return date(start_date.year + 2, start_date.month, start_date.day)
        elif self._membership_type == MembershipType.PREMIUM:
            return date(start_date.year + 1, start_date.month, start_date.day)
        else:  # PUBLIC
            return date(start_date.year + 1, start_date.month, start_date.day)
    
    def _get_max_books_for_type(self) -> int:
        """Get maximum books allowed based on membership type"""
        limits = {
            MembershipType.STUDENT: 5,
            MembershipType.FACULTY: 15,
            MembershipType.STAFF: 10,
            MembershipType.PREMIUM: 20,
            MembershipType.PUBLIC: 3
        }
        return limits.get(self._membership_type, 3)
    
    # Property decorators for encapsulation
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("First name cannot be empty")
        self._first_name = value.strip()
        self._update_timestamp()
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Last name cannot be empty")
        self._last_name = value.strip()
        self._update_timestamp()
    
    @property
    def full_name(self) -> str:
        """Get full name (computed property)"""
        return f"{self._first_name} {self._last_name}"
    
    @property
    def membership_type(self) -> MembershipType:
        return self._membership_type
    
    @membership_type.setter
    def membership_type(self, value: MembershipType):
        if not isinstance(value, MembershipType):
            raise TypeError("Membership type must be a MembershipType enum")
        self._membership_type = value
        self._membership_end_date = self._calculate_membership_end_date()
        self._max_books_allowed = self._get_max_books_for_type()
        self._update_timestamp()
    
    @property
    def date_of_birth(self) -> Optional[date]:
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value: Optional[date]):
        if value and value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        self._date_of_birth = value
        self._update_timestamp()
    
    @property
    def age(self) -> Optional[int]:
        """Calculate age from date of birth"""
        if not self._date_of_birth:
            return None
        today = date.today()
        return today.year - self._date_of_birth.year - (
            (today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day)
        )
    
    @property
    def student_id(self) -> str:
        return self._student_id
    
    @student_id.setter
    def student_id(self, value: str):
        self._student_id = value.strip() if value else ""
        self._update_timestamp()
    
    @property
    def contact_info(self) -> ContactInfo:
        return self._contact_info
    
    @contact_info.setter
    def contact_info(self, value: ContactInfo):
        if not isinstance(value, ContactInfo):
            raise TypeError("Contact info must be a ContactInfo instance")
        self._contact_info = value
        self._update_timestamp()
    
    @property
    def status(self) -> MemberStatus:
        return self._status
    
    @property
    def membership_start_date(self) -> date:
        return self._membership_start_date
    
    @property
    def membership_end_date(self) -> date:
        return self._membership_end_date
    
    @property
    def borrowed_books(self) -> List[str]:
        return self._borrowed_books.copy()
    
    @property
    def borrowed_books_count(self) -> int:
        return len(self._borrowed_books)
    
    @property
    def fine_amount(self) -> float:
        return self._fine_amount
    
    @property
    def max_books_allowed(self) -> int:
        return self._max_books_allowed
    
    @property
    def reservation_history(self) -> List[Dict]:
        return self._reservation_history.copy()
    
    def is_active(self) -> bool:
        """Check if member is active"""
        return self._status == MemberStatus.ACTIVE
    
    def is_membership_valid(self) -> bool:
        """Check if membership is still valid"""
        return date.today() <= self._membership_end_date
    
    def can_borrow_books(self) -> bool:
        """Check if member can borrow books"""
        return (self.is_active() and 
                self.is_membership_valid() and 
                self.borrowed_books_count < self._max_books_allowed and
                self._fine_amount == 0)
    
    def borrow_book(self, book_id: str) -> bool:
        """
        Add a book to member's borrowed books.
        Returns True if successful, False otherwise.
        """
        if not self.can_borrow_books():
            return False
        
        if book_id in self._borrowed_books:
            return False  # Already borrowed
        
        self._borrowed_books.append(book_id)
        self._update_timestamp()
        return True
    
    def return_book(self, book_id: str) -> bool:
        """
        Remove a book from member's borrowed books.
        Returns True if successful, False otherwise.
        """
        if book_id not in self._borrowed_books:
            return False
        
        self._borrowed_books.remove(book_id)
        self._update_timestamp()
        return True
    
    def add_fine(self, amount: float, reason: str = "") -> None:
        """Add fine to member's account"""
        if amount < 0:
            raise ValueError("Fine amount cannot be negative")
        self._fine_amount += amount
        self._update_timestamp()
    
    def pay_fine(self, amount: float) -> float:
        """
        Pay fine amount.
        Returns remaining fine amount.
        """
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        
        self._fine_amount = max(0, self._fine_amount - amount)
        self._update_timestamp()
        return self._fine_amount
    
    def suspend_membership(self, reason: str = "") -> None:
        """Suspend member's membership"""
        self._status = MemberStatus.SUSPENDED
        self._update_timestamp()
    
    def reactivate_membership(self) -> bool:
        """Reactivate suspended membership"""
        if self._status == MemberStatus.SUSPENDED and self.is_membership_valid():
            self._status = MemberStatus.ACTIVE
            self._update_timestamp()
            return True
        return False
    
    def renew_membership(self, duration_years: int = 1) -> None:
        """Renew membership for specified duration"""
        if duration_years <= 0:
            raise ValueError("Duration must be positive")
        
        end_date = self._membership_end_date
        new_end_date = date(end_date.year + duration_years, end_date.month, end_date.day)
        self._membership_end_date = new_end_date
        
        if self._status == MemberStatus.EXPIRED:
            self._status = MemberStatus.ACTIVE
        
        self._update_timestamp()
    
    def matches_search(self, query: str) -> bool:
        """Check if member matches search query"""
        query = query.lower().strip()
        if not query:
            return True
        
        searchable_fields = [
            self._first_name.lower(),
            self._last_name.lower(),
            self.full_name.lower(),
            self._student_id.lower(),
            self._contact_info.email.lower(),
            self._contact_info.phone.lower(),
            self._membership_type.value.lower()
        ]
        
        return any(query in field for field in searchable_fields)
    
    def validate(self) -> bool:
        """Validate member data"""
        return len(self.get_validation_errors()) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors"""
        errors = []
        
        if not self._first_name or not self._first_name.strip():
            errors.append("First name is required")
        
        if not self._last_name or not self._last_name.strip():
            errors.append("Last name is required")
        
        if self._date_of_birth and self._date_of_birth > date.today():
            errors.append("Date of birth cannot be in the future")
        
        if self._fine_amount < 0:
            errors.append("Fine amount cannot be negative")
        
        # Validate contact info
        try:
            if self._contact_info.email:
                self._contact_info.email = self._contact_info.email  # Trigger validation
            if self._contact_info.phone:
                self._contact_info.phone = self._contact_info.phone  # Trigger validation
        except ValueError as e:
            errors.append(str(e))
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert member to dictionary representation"""
        return {
            'id': self.id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'membership_type': self._membership_type.value,
            'date_of_birth': self._date_of_birth.isoformat() if self._date_of_birth else None,
            'student_id': self._student_id,
            'contact_info': self._contact_info.to_dict(),
            'status': self._status.value,
            'membership_start_date': self._membership_start_date.isoformat(),
            'membership_end_date': self._membership_end_date.isoformat(),
            'borrowed_books': self._borrowed_books,
            'reservation_history': self._reservation_history,
            'fine_amount': self._fine_amount,
            'max_books_allowed': self._max_books_allowed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'Member':
        """Create member from dictionary data"""
        contact_info = ContactInfo().from_dict(data.get('contact_info', {}))
        
        member = Member(
            first_name=data['first_name'],
            last_name=data['last_name'],
            membership_type=MembershipType(data.get('membership_type', MembershipType.PUBLIC.value)),
            date_of_birth=date.fromisoformat(data['date_of_birth']) if data.get('date_of_birth') else None,
            student_id=data.get('student_id', ''),
            contact_info=contact_info
        )
        
        member._id = data['id']
        member._status = MemberStatus(data.get('status', MemberStatus.ACTIVE.value))
        
        if data.get('membership_start_date'):
            member._membership_start_date = date.fromisoformat(data['membership_start_date'])
        if data.get('membership_end_date'):
            member._membership_end_date = date.fromisoformat(data['membership_end_date'])
        
        member._borrowed_books = data.get('borrowed_books', [])
        member._reservation_history = data.get('reservation_history', [])
        member._fine_amount = data.get('fine_amount', 0.0)
        member._max_books_allowed = data.get('max_books_allowed', member._get_max_books_for_type())
        
        if data.get('created_at'):
            member._created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            member._updated_at = datetime.fromisoformat(data['updated_at'])
        
        return member
    
    def __str__(self) -> str:
        """String representation of member"""
        return f"Member(name='{self.full_name}', type='{self._membership_type.value}', status='{self._status.value}')"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Member(id='{self.id}', name='{self.full_name}', "
                f"type='{self._membership_type.value}', status='{self._status.value}')")
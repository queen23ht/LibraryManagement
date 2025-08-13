"""
Transaction model for the Library Management System.
Demonstrates: Inheritance, State Pattern, Business Logic, Data Integrity
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum
from .base import BaseEntity, Searchable, Validatable


class TransactionType(Enum):
    """Types of library transactions"""
    BORROW = "borrow"
    RETURN = "return"
    RENEW = "renew"
    RESERVE = "reserve"
    CANCEL_RESERVATION = "cancel_reservation"
    FINE_PAYMENT = "fine_payment"
    LOST_BOOK = "lost_book"


class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    OVERDUE = "overdue"


class Transaction(BaseEntity, Searchable, Validatable):
    """
    Transaction entity representing a library transaction.
    Demonstrates: State management, Business rules, Data validation
    """
    
    def __init__(self, member_id: str, transaction_type: TransactionType,
                 book_id: str = None, amount: float = 0.0, 
                 due_date: datetime = None, notes: str = ""):
        super().__init__()
        self._member_id = member_id.strip()
        self._transaction_type = transaction_type
        self._book_id = book_id.strip() if book_id else None
        self._amount = amount
        self._due_date = due_date
        self._notes = notes.strip()
        self._status = TransactionStatus.PENDING
        self._processed_by = None  # Staff member who processed the transaction
        self._processed_at = None
        self._parent_transaction_id = None  # For linked transactions (e.g., renew links to original borrow)
        self._fine_amount = 0.0
        self._return_date = None
        
        # Set default due date for borrow transactions
        if transaction_type == TransactionType.BORROW and not due_date:
            self._due_date = datetime.now() + timedelta(days=14)  # Default 2 weeks
    
    # Property decorators for encapsulation
    @property
    def member_id(self) -> str:
        return self._member_id
    
    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type
    
    @property
    def book_id(self) -> Optional[str]:
        return self._book_id
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, value: float):
        if value < 0:
            raise ValueError("Amount cannot be negative")
        self._amount = value
        self._update_timestamp()
    
    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: Optional[datetime]):
        if value and value < datetime.now():
            raise ValueError("Due date cannot be in the past")
        self._due_date = value
        self._update_timestamp()
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, value: str):
        self._notes = value.strip() if value else ""
        self._update_timestamp()
    
    @property
    def status(self) -> TransactionStatus:
        return self._status
    
    @property
    def processed_by(self) -> Optional[str]:
        return self._processed_by
    
    @property
    def processed_at(self) -> Optional[datetime]:
        return self._processed_at
    
    @property
    def parent_transaction_id(self) -> Optional[str]:
        return self._parent_transaction_id
    
    @parent_transaction_id.setter
    def parent_transaction_id(self, value: Optional[str]):
        self._parent_transaction_id = value.strip() if value else None
        self._update_timestamp()
    
    @property
    def fine_amount(self) -> float:
        return self._fine_amount
    
    @property
    def return_date(self) -> Optional[datetime]:
        return self._return_date
    
    @property
    def is_overdue(self) -> bool:
        """Check if transaction is overdue"""
        if not self._due_date or self._status != TransactionStatus.COMPLETED:
            return False
        
        if self._transaction_type == TransactionType.BORROW:
            # Check if return date is after due date
            return (self._return_date and self._return_date > self._due_date) or \
                   (not self._return_date and datetime.now() > self._due_date)
        
        return False
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue"""
        if not self.is_overdue or not self._due_date:
            return 0
        
        end_date = self._return_date or datetime.now()
        return (end_date - self._due_date).days
    
    def calculate_fine(self, daily_fine_rate: float = 1.0) -> float:
        """
        Calculate fine amount for overdue transaction.
        Returns the calculated fine amount.
        """
        if not self.is_overdue:
            return 0.0
        
        days_overdue = self.days_overdue
        if days_overdue <= 0:
            return 0.0
        
        # Progressive fine calculation
        fine = 0.0
        if days_overdue <= 7:
            fine = days_overdue * daily_fine_rate
        elif days_overdue <= 30:
            fine = 7 * daily_fine_rate + (days_overdue - 7) * (daily_fine_rate * 1.5)
        else:
            fine = 7 * daily_fine_rate + 23 * (daily_fine_rate * 1.5) + \
                   (days_overdue - 30) * (daily_fine_rate * 2.0)
        
        return round(fine, 2)
    
    def process_transaction(self, processed_by: str) -> bool:
        """
        Process the transaction.
        Returns True if successful, False otherwise.
        """
        if self._status != TransactionStatus.PENDING:
            return False
        
        self._status = TransactionStatus.COMPLETED
        self._processed_by = processed_by.strip()
        self._processed_at = datetime.now()
        
        # Set return date for return transactions
        if self._transaction_type == TransactionType.RETURN:
            self._return_date = datetime.now()
            # Calculate fine if overdue
            self._fine_amount = self.calculate_fine()
        
        self._update_timestamp()
        return True
    
    def cancel_transaction(self, reason: str = "") -> bool:
        """
        Cancel the transaction.
        Returns True if successful, False otherwise.
        """
        if self._status not in [TransactionStatus.PENDING, TransactionStatus.FAILED]:
            return False
        
        self._status = TransactionStatus.CANCELLED
        if reason:
            self._notes = f"{self._notes}\nCancelled: {reason}".strip()
        self._update_timestamp()
        return True
    
    def fail_transaction(self, reason: str = "") -> bool:
        """
        Mark transaction as failed.
        Returns True if successful, False otherwise.
        """
        if self._status != TransactionStatus.PENDING:
            return False
        
        self._status = TransactionStatus.FAILED
        if reason:
            self._notes = f"{self._notes}\nFailed: {reason}".strip()
        self._update_timestamp()
        return True
    
    def extend_due_date(self, days: int) -> bool:
        """
        Extend due date by specified number of days.
        Returns True if successful, False otherwise.
        """
        if not self._due_date or self._status != TransactionStatus.COMPLETED:
            return False
        
        if self._transaction_type != TransactionType.BORROW:
            return False
        
        self._due_date += timedelta(days=days)
        self._update_timestamp()
        return True
    
    def renew_transaction(self, renewal_days: int = 14) -> bool:
        """
        Renew the transaction (extend due date).
        Returns True if successful, False otherwise.
        """
        if self._transaction_type != TransactionType.BORROW:
            return False
        
        if self._status != TransactionStatus.COMPLETED:
            return False
        
        # Check if already overdue
        if self.is_overdue:
            return False
        
        return self.extend_due_date(renewal_days)
    
    def matches_search(self, query: str) -> bool:
        """Check if transaction matches search query"""
        query = query.lower().strip()
        if not query:
            return True
        
        searchable_fields = [
            self._member_id.lower(),
            self._book_id.lower() if self._book_id else "",
            self._transaction_type.value.lower(),
            self._status.value.lower(),
            self._notes.lower(),
            self._processed_by.lower() if self._processed_by else ""
        ]
        
        return any(query in field for field in searchable_fields)
    
    def validate(self) -> bool:
        """Validate transaction data"""
        return len(self.get_validation_errors()) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors"""
        errors = []
        
        if not self._member_id or not self._member_id.strip():
            errors.append("Member ID is required")
        
        # Book ID required for certain transaction types
        book_required_types = [
            TransactionType.BORROW, 
            TransactionType.RETURN, 
            TransactionType.RENEW, 
            TransactionType.RESERVE,
            TransactionType.LOST_BOOK
        ]
        
        if self._transaction_type in book_required_types and not self._book_id:
            errors.append(f"Book ID is required for {self._transaction_type.value} transactions")
        
        if self._amount < 0:
            errors.append("Amount cannot be negative")
        
        if self._fine_amount < 0:
            errors.append("Fine amount cannot be negative")
        
        # Due date validation for borrow transactions
        if (self._transaction_type == TransactionType.BORROW and 
            self._due_date and self._due_date < self.created_at):
            errors.append("Due date cannot be before transaction creation date")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary representation"""
        return {
            'id': self.id,
            'member_id': self._member_id,
            'transaction_type': self._transaction_type.value,
            'book_id': self._book_id,
            'amount': self._amount,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'notes': self._notes,
            'status': self._status.value,
            'processed_by': self._processed_by,
            'processed_at': self._processed_at.isoformat() if self._processed_at else None,
            'parent_transaction_id': self._parent_transaction_id,
            'fine_amount': self._fine_amount,
            'return_date': self._return_date.isoformat() if self._return_date else None,
            'is_overdue': self.is_overdue,
            'days_overdue': self.days_overdue,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary data"""
        transaction = Transaction(
            member_id=data['member_id'],
            transaction_type=TransactionType(data['transaction_type']),
            book_id=data.get('book_id'),
            amount=data.get('amount', 0.0),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            notes=data.get('notes', '')
        )
        
        transaction._id = data['id']
        transaction._status = TransactionStatus(data.get('status', TransactionStatus.PENDING.value))
        transaction._processed_by = data.get('processed_by')
        transaction._parent_transaction_id = data.get('parent_transaction_id')
        transaction._fine_amount = data.get('fine_amount', 0.0)
        
        if data.get('processed_at'):
            transaction._processed_at = datetime.fromisoformat(data['processed_at'])
        if data.get('return_date'):
            transaction._return_date = datetime.fromisoformat(data['return_date'])
        if data.get('created_at'):
            transaction._created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            transaction._updated_at = datetime.fromisoformat(data['updated_at'])
        
        return transaction
    
    def __str__(self) -> str:
        """String representation of transaction"""
        return (f"Transaction(type='{self._transaction_type.value}', "
                f"member='{self._member_id}', book='{self._book_id}', "
                f"status='{self._status.value}')")
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Transaction(id='{self.id}', type='{self._transaction_type.value}', "
                f"member='{self._member_id}', book='{self._book_id}', "
                f"status='{self._status.value}', amount={self._amount})")
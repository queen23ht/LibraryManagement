"""
Validation utilities for the Library Management System.
Demonstrates: Validation patterns, Decorator pattern, Error handling
"""

import re
from typing import Any, Callable, List, Optional
from functools import wraps
from datetime import datetime, date


class ValidationError(Exception):
    """Exception raised for validation errors"""
    pass


class Validator:
    """
    Base validator class.
    Demonstrates: Strategy pattern, Method chaining
    """
    
    def __init__(self, value: Any, field_name: str = "field"):
        self.value = value
        self.field_name = field_name
        self.errors: List[str] = []
    
    def required(self, message: str = None) -> 'Validator':
        """Check if value is not None or empty"""
        if message is None:
            message = f"{self.field_name} is required"
        
        if self.value is None or (isinstance(self.value, str) and not self.value.strip()):
            self.errors.append(message)
        
        return self
    
    def min_length(self, length: int, message: str = None) -> 'Validator':
        """Check minimum length for strings"""
        if message is None:
            message = f"{self.field_name} must be at least {length} characters long"
        
        if isinstance(self.value, str) and len(self.value) < length:
            self.errors.append(message)
        
        return self
    
    def max_length(self, length: int, message: str = None) -> 'Validator':
        """Check maximum length for strings"""
        if message is None:
            message = f"{self.field_name} must be at most {length} characters long"
        
        if isinstance(self.value, str) and len(self.value) > length:
            self.errors.append(message)
        
        return self
    
    def min_value(self, min_val: float, message: str = None) -> 'Validator':
        """Check minimum value for numbers"""
        if message is None:
            message = f"{self.field_name} must be at least {min_val}"
        
        if isinstance(self.value, (int, float)) and self.value < min_val:
            self.errors.append(message)
        
        return self
    
    def max_value(self, max_val: float, message: str = None) -> 'Validator':
        """Check maximum value for numbers"""
        if message is None:
            message = f"{self.field_name} must be at most {max_val}"
        
        if isinstance(self.value, (int, float)) and self.value > max_val:
            self.errors.append(message)
        
        return self
    
    def regex(self, pattern: str, message: str = None) -> 'Validator':
        """Check if value matches regex pattern"""
        if message is None:
            message = f"{self.field_name} format is invalid"
        
        if isinstance(self.value, str) and not re.match(pattern, self.value):
            self.errors.append(message)
        
        return self
    
    def email(self, message: str = None) -> 'Validator':
        """Validate email format"""
        if message is None:
            message = f"{self.field_name} must be a valid email address"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return self.regex(email_pattern, message)
    
    def phone(self, message: str = None) -> 'Validator':
        """Validate phone number format"""
        if message is None:
            message = f"{self.field_name} must be a valid phone number"
        
        if isinstance(self.value, str):
            # Remove common phone number separators
            cleaned = re.sub(r'[\s\-\(\)\+]', '', self.value)
            if not (cleaned.isdigit() and 10 <= len(cleaned) <= 15):
                self.errors.append(message)
        
        return self
    
    def isbn(self, message: str = None) -> 'Validator':
        """Validate ISBN format (ISBN-10 or ISBN-13)"""
        if message is None:
            message = f"{self.field_name} must be a valid ISBN"
        
        if isinstance(self.value, str):
            # Remove dashes and spaces
            cleaned = re.sub(r'[\s\-]', '', self.value)
            
            # Check if it's a valid ISBN-10 or ISBN-13
            if not (self._is_valid_isbn10(cleaned) or self._is_valid_isbn13(cleaned)):
                self.errors.append(message)
        
        return self
    
    def _is_valid_isbn10(self, isbn: str) -> bool:
        """Validate ISBN-10 format"""
        if len(isbn) != 10:
            return False
        
        if not (isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9].upper() == 'X')):
            return False
        
        # Calculate checksum
        total = sum(int(digit) * (10 - i) for i, digit in enumerate(isbn[:9]))
        checksum = total % 11
        check_digit = 'X' if checksum == 1 else str(11 - checksum) if checksum != 0 else '0'
        
        return isbn[9].upper() == check_digit
    
    def _is_valid_isbn13(self, isbn: str) -> bool:
        """Validate ISBN-13 format"""
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        
        # Calculate checksum
        total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:12]))
        checksum = (10 - (total % 10)) % 10
        
        return int(isbn[12]) == checksum
    
    def date_not_future(self, message: str = None) -> 'Validator':
        """Check that date is not in the future"""
        if message is None:
            message = f"{self.field_name} cannot be in the future"
        
        if isinstance(self.value, (date, datetime)):
            today = date.today()
            check_date = self.value.date() if isinstance(self.value, datetime) else self.value
            
            if check_date > today:
                self.errors.append(message)
        
        return self
    
    def date_not_past(self, message: str = None) -> 'Validator':
        """Check that date is not in the past"""
        if message is None:
            message = f"{self.field_name} cannot be in the past"
        
        if isinstance(self.value, (date, datetime)):
            today = date.today()
            check_date = self.value.date() if isinstance(self.value, datetime) else self.value
            
            if check_date < today:
                self.errors.append(message)
        
        return self
    
    def custom(self, validator_func: Callable[[Any], bool], message: str) -> 'Validator':
        """Apply custom validation function"""
        if not validator_func(self.value):
            self.errors.append(message)
        
        return self
    
    def is_valid(self) -> bool:
        """Check if all validations passed"""
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.errors.copy()
    
    def raise_if_invalid(self) -> None:
        """Raise ValidationError if validation failed"""
        if not self.is_valid():
            raise ValidationError(f"Validation failed: {', '.join(self.errors)}")


def validate(value: Any, field_name: str = "field") -> Validator:
    """Create a new validator instance"""
    return Validator(value, field_name)


def validation_decorator(validation_func: Callable) -> Callable:
    """
    Decorator for adding validation to methods.
    Demonstrates: Decorator pattern
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs):
            # Apply validation
            validation_func(*args, **kwargs)
            # Call original method
            return method(*args, **kwargs)
        return wrapper
    return decorator


class BookValidator:
    """Specialized validator for Book entities"""
    
    @staticmethod
    def validate_book_data(title: str, author: str, isbn: str, 
                          publication_year: int = None, pages: int = 0) -> List[str]:
        """Validate book data and return list of errors"""
        errors = []
        
        # Title validation
        title_validator = validate(title, "Title").required().min_length(1).max_length(500)
        errors.extend(title_validator.get_errors())
        
        # Author validation
        author_validator = validate(author, "Author").required().min_length(1).max_length(200)
        errors.extend(author_validator.get_errors())
        
        # ISBN validation
        isbn_validator = validate(isbn, "ISBN").required().isbn()
        errors.extend(isbn_validator.get_errors())
        
        # Publication year validation
        if publication_year is not None:
            current_year = datetime.now().year
            year_validator = validate(publication_year, "Publication year").min_value(0).max_value(current_year)
            errors.extend(year_validator.get_errors())
        
        # Pages validation
        pages_validator = validate(pages, "Pages").min_value(0)
        errors.extend(pages_validator.get_errors())
        
        return errors


class MemberValidator:
    """Specialized validator for Member entities"""
    
    @staticmethod
    def validate_member_data(first_name: str, last_name: str, 
                           email: str = "", phone: str = "",
                           date_of_birth: date = None) -> List[str]:
        """Validate member data and return list of errors"""
        errors = []
        
        # Name validation
        first_name_validator = validate(first_name, "First name").required().min_length(1).max_length(50)
        errors.extend(first_name_validator.get_errors())
        
        last_name_validator = validate(last_name, "Last name").required().min_length(1).max_length(50)
        errors.extend(last_name_validator.get_errors())
        
        # Email validation (optional)
        if email:
            email_validator = validate(email, "Email").email()
            errors.extend(email_validator.get_errors())
        
        # Phone validation (optional)
        if phone:
            phone_validator = validate(phone, "Phone").phone()
            errors.extend(phone_validator.get_errors())
        
        # Date of birth validation (optional)
        if date_of_birth:
            dob_validator = validate(date_of_birth, "Date of birth").date_not_future()
            errors.extend(dob_validator.get_errors())
        
        return errors


class TransactionValidator:
    """Specialized validator for Transaction entities"""
    
    @staticmethod
    def validate_transaction_data(member_id: str, amount: float = 0.0,
                                due_date: datetime = None) -> List[str]:
        """Validate transaction data and return list of errors"""
        errors = []
        
        # Member ID validation
        member_id_validator = validate(member_id, "Member ID").required()
        errors.extend(member_id_validator.get_errors())
        
        # Amount validation
        amount_validator = validate(amount, "Amount").min_value(0)
        errors.extend(amount_validator.get_errors())
        
        # Due date validation (optional)
        if due_date:
            due_date_validator = validate(due_date, "Due date").date_not_past()
            errors.extend(due_date_validator.get_errors())
        
        return errors


# Example usage and testing functions
def test_validators():
    """Test function to demonstrate validator usage"""
    print("Testing validators...")
    
    # Test email validation
    email_validator = validate("test@example.com", "Email").email()
    print(f"Email validation passed: {email_validator.is_valid()}")
    
    # Test ISBN validation
    isbn_validator = validate("978-3-16-148410-0", "ISBN").isbn()
    print(f"ISBN validation passed: {isbn_validator.is_valid()}")
    
    # Test phone validation
    phone_validator = validate("+1 (555) 123-4567", "Phone").phone()
    print(f"Phone validation passed: {phone_validator.is_valid()}")
    
    # Test chained validation
    name_validator = validate("John", "Name").required().min_length(2).max_length(50)
    print(f"Name validation passed: {name_validator.is_valid()}")
    print(f"Errors: {name_validator.get_errors()}")


if __name__ == "__main__":
    test_validators()
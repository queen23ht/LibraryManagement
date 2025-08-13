"""
Sorting utilities for the Library Management System.
Demonstrates: Sorting algorithms, Comparators, Functional programming
"""

from typing import List, Callable, Any, Optional
from enum import Enum
from functools import cmp_to_key
from datetime import datetime

from models import Book, Member, Transaction


class SortOrder(Enum):
    """Sort order enumeration"""
    ASC = "ascending"
    DESC = "descending"


class BookSorter:
    """
    Utility class for sorting books.
    Demonstrates: Strategy pattern, Comparator functions
    """
    
    @staticmethod
    def by_title(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by title"""
        reverse = order == SortOrder.DESC
        return sorted(books, key=lambda b: b.title.lower(), reverse=reverse)
    
    @staticmethod
    def by_author(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by author"""
        reverse = order == SortOrder.DESC
        return sorted(books, key=lambda b: b.author.lower(), reverse=reverse)
    
    @staticmethod
    def by_publication_year(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by publication year (None values last)"""
        reverse = order == SortOrder.DESC
        
        def sort_key(book):
            # Put None values at the end
            if book.publication_year is None:
                return (1, 0) if not reverse else (0, 0)
            return (0, book.publication_year)
        
        return sorted(books, key=sort_key, reverse=reverse)
    
    @staticmethod
    def by_category(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by category"""
        reverse = order == SortOrder.DESC
        return sorted(books, key=lambda b: b.category.value, reverse=reverse)
    
    @staticmethod
    def by_status(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by status"""
        reverse = order == SortOrder.DESC
        status_priority = {
            'available': 1,
            'borrowed': 2,
            'reserved': 3,
            'maintenance': 4,
            'lost': 5
        }
        return sorted(books, key=lambda b: status_priority.get(b.status.value, 999), reverse=reverse)
    
    @staticmethod
    def by_created_date(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by creation date"""
        reverse = order == SortOrder.DESC
        return sorted(books, key=lambda b: b.created_at, reverse=reverse)
    
    @staticmethod
    def by_due_date(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by due date (borrowed books only, None values last)"""
        reverse = order == SortOrder.DESC
        
        def sort_key(book):
            if book.due_date is None:
                return (1, datetime.min) if not reverse else (0, datetime.max)
            return (0, book.due_date)
        
        return sorted(books, key=sort_key, reverse=reverse)
    
    @staticmethod
    def by_popularity(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        """Sort books by popularity (number of times borrowed)"""
        reverse = order == SortOrder.DESC
        return sorted(books, key=lambda b: len(b.borrow_history), reverse=reverse)
    
    @staticmethod
    def multi_sort(books: List[Book], criteria: List[tuple]) -> List[Book]:
        """
        Sort books by multiple criteria.
        criteria: List of (sort_function, order) tuples
        """
        result = books.copy()
        
        # Apply sorting criteria in reverse order (last criteria has highest priority)
        for sort_func, order in reversed(criteria):
            result = sort_func(result, order)
        
        return result


class MemberSorter:
    """Utility class for sorting members"""
    
    @staticmethod
    def by_name(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by full name"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.full_name.lower(), reverse=reverse)
    
    @staticmethod
    def by_first_name(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by first name"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.first_name.lower(), reverse=reverse)
    
    @staticmethod
    def by_last_name(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by last name"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.last_name.lower(), reverse=reverse)
    
    @staticmethod
    def by_membership_type(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by membership type"""
        reverse = order == SortOrder.DESC
        type_priority = {
            'student': 1,
            'faculty': 2,
            'staff': 3,
            'premium': 4,
            'public': 5
        }
        return sorted(members, key=lambda m: type_priority.get(m.membership_type.value, 999), reverse=reverse)
    
    @staticmethod
    def by_status(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by status"""
        reverse = order == SortOrder.DESC
        status_priority = {
            'active': 1,
            'suspended': 2,
            'expired': 3,
            'blocked': 4
        }
        return sorted(members, key=lambda m: status_priority.get(m.status.value, 999), reverse=reverse)
    
    @staticmethod
    def by_join_date(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by membership start date"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.membership_start_date, reverse=reverse)
    
    @staticmethod
    def by_age(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by age (None values last)"""
        reverse = order == SortOrder.DESC
        
        def sort_key(member):
            if member.age is None:
                return (1, 0) if not reverse else (0, 999)
            return (0, member.age)
        
        return sorted(members, key=sort_key, reverse=reverse)
    
    @staticmethod
    def by_borrowed_books_count(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by number of borrowed books"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.borrowed_books_count, reverse=reverse)
    
    @staticmethod
    def by_fine_amount(members: List[Member], order: SortOrder = SortOrder.ASC) -> List[Member]:
        """Sort members by fine amount"""
        reverse = order == SortOrder.DESC
        return sorted(members, key=lambda m: m.fine_amount, reverse=reverse)


class TransactionSorter:
    """Utility class for sorting transactions"""
    
    @staticmethod
    def by_date(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by creation date"""
        reverse = order == SortOrder.DESC
        return sorted(transactions, key=lambda t: t.created_at, reverse=reverse)
    
    @staticmethod
    def by_type(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by type"""
        reverse = order == SortOrder.DESC
        type_priority = {
            'borrow': 1,
            'return': 2,
            'renew': 3,
            'reserve': 4,
            'cancel_reservation': 5,
            'fine_payment': 6,
            'lost_book': 7
        }
        return sorted(transactions, key=lambda t: type_priority.get(t.transaction_type.value, 999), reverse=reverse)
    
    @staticmethod
    def by_status(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by status"""
        reverse = order == SortOrder.DESC
        status_priority = {
            'pending': 1,
            'completed': 2,
            'cancelled': 3,
            'failed': 4,
            'overdue': 5
        }
        return sorted(transactions, key=lambda t: status_priority.get(t.status.value, 999), reverse=reverse)
    
    @staticmethod
    def by_amount(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by amount"""
        reverse = order == SortOrder.DESC
        return sorted(transactions, key=lambda t: t.amount, reverse=reverse)
    
    @staticmethod
    def by_due_date(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by due date (None values last)"""
        reverse = order == SortOrder.DESC
        
        def sort_key(transaction):
            if transaction.due_date is None:
                return (1, datetime.min) if not reverse else (0, datetime.max)
            return (0, transaction.due_date)
        
        return sorted(transactions, key=sort_key, reverse=reverse)
    
    @staticmethod
    def by_overdue_status(transactions: List[Transaction], order: SortOrder = SortOrder.ASC) -> List[Transaction]:
        """Sort transactions by overdue status"""
        reverse = order == SortOrder.DESC
        return sorted(transactions, key=lambda t: (t.is_overdue, t.days_overdue), reverse=reverse)


class CustomSorter:
    """
    Generic sorter with custom comparison functions.
    Demonstrates: Higher-order functions, Functional programming
    """
    
    @staticmethod
    def sort_by_function(items: List[Any], key_func: Callable[[Any], Any], 
                        order: SortOrder = SortOrder.ASC) -> List[Any]:
        """Sort items using a custom key function"""
        reverse = order == SortOrder.DESC
        return sorted(items, key=key_func, reverse=reverse)
    
    @staticmethod
    def sort_by_comparator(items: List[Any], compare_func: Callable[[Any, Any], int], 
                          order: SortOrder = SortOrder.ASC) -> List[Any]:
        """Sort items using a custom comparator function"""
        reverse = order == SortOrder.DESC
        
        # Adjust comparator for reverse order
        if reverse:
            def reversed_compare(a, b):
                return -compare_func(a, b)
            compare_func = reversed_compare
        
        return sorted(items, key=cmp_to_key(compare_func))
    
    @staticmethod
    def stable_sort(items: List[Any], key_func: Callable[[Any], Any], 
                   order: SortOrder = SortOrder.ASC) -> List[Any]:
        """Stable sort that preserves order of equal elements"""
        reverse = order == SortOrder.DESC
        
        # Add index to maintain stability
        indexed_items = [(item, i) for i, item in enumerate(items)]
        
        def stable_key(indexed_item):
            item, index = indexed_item
            return (key_func(item), index)
        
        sorted_indexed = sorted(indexed_items, key=stable_key, reverse=reverse)
        return [item for item, _ in sorted_indexed]


class SearchAndSort:
    """
    Combined search and sort utilities.
    Demonstrates: Composition pattern, Fluent interface
    """
    
    def __init__(self, items: List[Any]):
        self.items = items.copy()
    
    def filter_by(self, predicate: Callable[[Any], bool]) -> 'SearchAndSort':
        """Filter items by predicate function"""
        self.items = [item for item in self.items if predicate(item)]
        return self
    
    def sort_by(self, key_func: Callable[[Any], Any], 
               order: SortOrder = SortOrder.ASC) -> 'SearchAndSort':
        """Sort items by key function"""
        self.items = CustomSorter.sort_by_function(self.items, key_func, order)
        return self
    
    def limit(self, count: int) -> 'SearchAndSort':
        """Limit number of results"""
        self.items = self.items[:count]
        return self
    
    def skip(self, count: int) -> 'SearchAndSort':
        """Skip first N items"""
        self.items = self.items[count:]
        return self
    
    def get_results(self) -> List[Any]:
        """Get final results"""
        return self.items.copy()


# Advanced sorting algorithms
class AdvancedSorter:
    """Advanced sorting algorithms and utilities"""
    
    @staticmethod
    def natural_sort(items: List[str], order: SortOrder = SortOrder.ASC) -> List[str]:
        """
        Natural sort for strings with numbers (e.g., "item2" comes before "item10")
        """
        import re
        
        def natural_key(text):
            return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]
        
        reverse = order == SortOrder.DESC
        return sorted(items, key=natural_key, reverse=reverse)
    
    @staticmethod
    def fuzzy_sort(items: List[str], query: str, order: SortOrder = SortOrder.ASC) -> List[str]:
        """
        Sort strings by similarity to query string
        """
        def similarity_score(text):
            # Simple similarity based on common characters
            text_lower = text.lower()
            query_lower = query.lower()
            
            if query_lower in text_lower:
                return len(query_lower) / len(text_lower)
            
            # Count common characters
            common = sum(1 for c in query_lower if c in text_lower)
            return common / max(len(query_lower), len(text_lower))
        
        reverse = order == SortOrder.DESC
        return sorted(items, key=similarity_score, reverse=reverse)


# Example usage and testing
def demo_sorting():
    """Demonstrate sorting functionality"""
    print("Sorting Demo")
    print("=" * 40)
    
    # Demo natural sort
    items = ["item1", "item10", "item2", "item20", "item3"]
    print(f"Original: {items}")
    print(f"Natural sort: {AdvancedSorter.natural_sort(items)}")
    
    # Demo fuzzy sort
    words = ["apple", "application", "apply", "banana", "grape"]
    query = "app"
    print(f"\nWords: {words}")
    print(f"Fuzzy sort by '{query}': {AdvancedSorter.fuzzy_sort(words, query, SortOrder.DESC)}")
    
    # Demo search and sort chaining
    numbers = list(range(20))
    result = (SearchAndSort(numbers)
              .filter_by(lambda x: x % 2 == 0)  # Even numbers only
              .sort_by(lambda x: -x)             # Descending order
              .limit(5)                          # Top 5
              .get_results())
    
    print(f"\nChained operations result: {result}")


if __name__ == "__main__":
    demo_sorting()
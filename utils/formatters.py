"""
Formatting utilities for the Library Management System.
Demonstrates: Formatting patterns, String manipulation, Data presentation
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional
from enum import Enum

from models import Book, Member, Transaction


class TableFormatter:
    """
    Utility class for formatting data into tables.
    Demonstrates: Formatting patterns, String manipulation
    """
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]], 
                    title: str = "", max_width: int = 100) -> str:
        """Format data into a table"""
        if not headers or not rows:
            return "No data to display"
        
        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Adjust for max width
        total_width = sum(col_widths) + len(headers) * 3 - 1
        if total_width > max_width:
            # Reduce column widths proportionally
            reduction = (total_width - max_width) / len(col_widths)
            col_widths = [max(8, int(width - reduction)) for width in col_widths]
        
        # Create format string
        format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
        separator = "-+-".join("-" * width for width in col_widths)
        
        # Build table
        lines = []
        
        if title:
            lines.append(f"\n{title}")
            lines.append("=" * len(title))
        
        lines.append(format_str.format(*headers))
        lines.append(separator)
        
        for row in rows:
            # Truncate cells if necessary
            truncated_row = []
            for i, cell in enumerate(row):
                cell_str = str(cell)
                if i < len(col_widths) and len(cell_str) > col_widths[i]:
                    cell_str = cell_str[:col_widths[i] - 3] + "..."
                truncated_row.append(cell_str)
            
            lines.append(format_str.format(*truncated_row))
        
        return "\n".join(lines)


class BookFormatter:
    """Formatting utilities for Book entities"""
    
    @staticmethod
    def format_book_summary(book: Book) -> str:
        """Format a single book for summary display"""
        status_emoji = {
            'available': '✅',
            'borrowed': '📖',
            'reserved': '📝',
            'maintenance': '🔧',
            'lost': '❌'
        }
        
        emoji = status_emoji.get(book.status.value, '❓')
        return f"{emoji} {book.title} by {book.author} ({book.status.value})"
    
    @staticmethod
    def format_book_detail(book: Book) -> str:
        """Format detailed book information"""
        lines = [
            f"📚 Book Details",
            f"{'=' * 50}",
            f"Title: {book.title}",
            f"Author: {book.author}",
            f"ISBN: {book.isbn}",
            f"Category: {book.category.value.replace('_', ' ').title()}",
            f"Status: {book.status.value.title()}",
        ]
        
        if book.publication_year:
            lines.append(f"Publication Year: {book.publication_year}")
        
        if book.publisher:
            lines.append(f"Publisher: {book.publisher}")
        
        if book.pages > 0:
            lines.append(f"Pages: {book.pages}")
        
        if book.description:
            lines.append(f"Description: {book.description}")
        
        if book.borrowed_by:
            lines.append(f"Borrowed by: {book.borrowed_by}")
            if book.borrowed_date:
                lines.append(f"Borrowed on: {DateTimeFormatter.format_date(book.borrowed_date)}")
            if book.due_date:
                lines.append(f"Due date: {DateTimeFormatter.format_date(book.due_date)}")
        
        lines.extend([
            f"Created: {DateTimeFormatter.format_datetime(book.created_at)}",
            f"Updated: {DateTimeFormatter.format_datetime(book.updated_at)}"
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_books_table(books: List[Book]) -> str:
        """Format list of books as a table"""
        if not books:
            return "No books found."
        
        headers = ["Title", "Author", "ISBN", "Category", "Status"]
        rows = []
        
        for book in books:
            rows.append([
                book.title,
                book.author,
                book.isbn,
                book.category.value.replace('_', ' ').title(),
                book.status.value.title()
            ])
        
        return TableFormatter.format_table(headers, rows, "📚 Books List")


class MemberFormatter:
    """Formatting utilities for Member entities"""
    
    @staticmethod
    def format_member_summary(member: Member) -> str:
        """Format a single member for summary display"""
        status_emoji = {
            'active': '✅',
            'suspended': '⏸️',
            'expired': '⏰',
            'blocked': '🚫'
        }
        
        emoji = status_emoji.get(member.status.value, '❓')
        return f"{emoji} {member.full_name} ({member.membership_type.value})"
    
    @staticmethod
    def format_member_detail(member: Member) -> str:
        """Format detailed member information"""
        lines = [
            f"👤 Member Details",
            f"{'=' * 50}",
            f"Name: {member.full_name}",
            f"Membership Type: {member.membership_type.value.replace('_', ' ').title()}",
            f"Status: {member.status.value.title()}",
        ]
        
        if member.student_id:
            lines.append(f"Student ID: {member.student_id}")
        
        if member.date_of_birth:
            lines.append(f"Date of Birth: {DateTimeFormatter.format_date(member.date_of_birth)}")
            if member.age:
                lines.append(f"Age: {member.age}")
        
        # Contact information
        if member.contact_info.email:
            lines.append(f"Email: {member.contact_info.email}")
        if member.contact_info.phone:
            lines.append(f"Phone: {member.contact_info.phone}")
        if member.contact_info.address:
            lines.append(f"Address: {member.contact_info.address}")
        
        # Membership information
        lines.extend([
            f"Membership Start: {DateTimeFormatter.format_date(member.membership_start_date)}",
            f"Membership End: {DateTimeFormatter.format_date(member.membership_end_date)}",
            f"Books Borrowed: {member.borrowed_books_count}/{member.max_books_allowed}",
        ])
        
        if member.fine_amount > 0:
            lines.append(f"Outstanding Fines: ${member.fine_amount:.2f}")
        
        lines.extend([
            f"Created: {DateTimeFormatter.format_datetime(member.created_at)}",
            f"Updated: {DateTimeFormatter.format_datetime(member.updated_at)}"
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_members_table(members: List[Member]) -> str:
        """Format list of members as a table"""
        if not members:
            return "No members found."
        
        headers = ["Name", "Type", "Status", "Books", "Fines"]
        rows = []
        
        for member in members:
            rows.append([
                member.full_name,
                member.membership_type.value.replace('_', ' ').title(),
                member.status.value.title(),
                f"{member.borrowed_books_count}/{member.max_books_allowed}",
                f"${member.fine_amount:.2f}" if member.fine_amount > 0 else "-"
            ])
        
        return TableFormatter.format_table(headers, rows, "👥 Members List")


class TransactionFormatter:
    """Formatting utilities for Transaction entities"""
    
    @staticmethod
    def format_transaction_summary(transaction: Transaction) -> str:
        """Format a single transaction for summary display"""
        type_emoji = {
            'borrow': '📤',
            'return': '📥',
            'renew': '🔄',
            'reserve': '📝',
            'cancel_reservation': '❌',
            'fine_payment': '💰',
            'lost_book': '❗'
        }
        
        emoji = type_emoji.get(transaction.transaction_type.value, '❓')
        return f"{emoji} {transaction.transaction_type.value.replace('_', ' ').title()}"
    
    @staticmethod
    def format_transaction_detail(transaction: Transaction) -> str:
        """Format detailed transaction information"""
        lines = [
            f"📋 Transaction Details",
            f"{'=' * 50}",
            f"ID: {transaction.id}",
            f"Type: {transaction.transaction_type.value.replace('_', ' ').title()}",
            f"Status: {transaction.status.value.title()}",
            f"Member ID: {transaction.member_id}",
        ]
        
        if transaction.book_id:
            lines.append(f"Book ID: {transaction.book_id}")
        
        if transaction.amount > 0:
            lines.append(f"Amount: ${transaction.amount:.2f}")
        
        if transaction.due_date:
            lines.append(f"Due Date: {DateTimeFormatter.format_datetime(transaction.due_date)}")
        
        if transaction.return_date:
            lines.append(f"Return Date: {DateTimeFormatter.format_datetime(transaction.return_date)}")
        
        if transaction.fine_amount > 0:
            lines.append(f"Fine Amount: ${transaction.fine_amount:.2f}")
        
        if transaction.is_overdue:
            lines.append(f"Days Overdue: {transaction.days_overdue}")
        
        if transaction.notes:
            lines.append(f"Notes: {transaction.notes}")
        
        if transaction.processed_by:
            lines.append(f"Processed by: {transaction.processed_by}")
            if transaction.processed_at:
                lines.append(f"Processed at: {DateTimeFormatter.format_datetime(transaction.processed_at)}")
        
        lines.extend([
            f"Created: {DateTimeFormatter.format_datetime(transaction.created_at)}",
            f"Updated: {DateTimeFormatter.format_datetime(transaction.updated_at)}"
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_transactions_table(transactions: List[Transaction]) -> str:
        """Format list of transactions as a table"""
        if not transactions:
            return "No transactions found."
        
        headers = ["Type", "Member", "Book", "Status", "Date", "Amount"]
        rows = []
        
        for transaction in transactions:
            rows.append([
                transaction.transaction_type.value.replace('_', ' ').title(),
                transaction.member_id[:8] + "..." if len(transaction.member_id) > 8 else transaction.member_id,
                transaction.book_id[:8] + "..." if transaction.book_id and len(transaction.book_id) > 8 else transaction.book_id or "-",
                transaction.status.value.title(),
                DateTimeFormatter.format_date(transaction.created_at),
                f"${transaction.amount:.2f}" if transaction.amount > 0 else "-"
            ])
        
        return TableFormatter.format_table(headers, rows, "📋 Transactions List")


class DateTimeFormatter:
    """Utilities for formatting dates and times"""
    
    @staticmethod
    def format_date(dt: date) -> str:
        """Format date in readable format"""
        if isinstance(dt, datetime):
            dt = dt.date()
        return dt.strftime("%Y-%m-%d")
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime in readable format"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def format_time_ago(dt: datetime) -> str:
        """Format time as 'X time ago'"""
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    
    @staticmethod
    def format_duration(start: datetime, end: datetime) -> str:
        """Format duration between two datetimes"""
        diff = end - start
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            return f"{diff.seconds} second{'s' if diff.seconds != 1 else ''}"


class StatisticsFormatter:
    """Utilities for formatting statistics and reports"""
    
    @staticmethod
    def format_statistics(stats: Dict[str, Any]) -> str:
        """Format library statistics"""
        lines = [
            f"📊 Library Statistics",
            f"{'=' * 50}",
            "",
            f"📚 Books:",
            f"  Total: {stats['books']['total']}",
            f"  Available: {stats['books']['available']}",
            f"  Borrowed: {stats['books']['borrowed']}",
            f"  Overdue: {stats['books']['overdue']}",
            "",
            f"👥 Members:",
            f"  Total: {stats['members']['total']}",
            f"  Active: {stats['members']['active']}",
            "",
            f"💰 Finances:",
            f"  Total Fines: ${stats['finances']['total_fines']:.2f}",
            "",
            f"📋 Transactions:",
            f"  Today: {stats['transactions']['today']}",
            f"  Total: {stats['transactions']['total']}",
        ]
        
        return "\n".join(lines)
    
    @staticmethod
    def format_overdue_report(overdue_items: List[tuple]) -> str:
        """Format overdue books report"""
        if not overdue_items:
            return "📅 No overdue books!"
        
        lines = [
            f"⚠️  Overdue Books Report",
            f"{'=' * 50}",
        ]
        
        for book, member, transaction in overdue_items:
            days_overdue = transaction.days_overdue
            fine = transaction.calculate_fine()
            
            lines.extend([
                f"",
                f"📖 {book.title}",
                f"   Member: {member.full_name}",
                f"   Due Date: {DateTimeFormatter.format_date(book.due_date)}",
                f"   Days Overdue: {days_overdue}",
                f"   Fine: ${fine:.2f}",
            ])
        
        return "\n".join(lines)


# Example usage
def demo_formatters():
    """Demonstrate formatter usage"""
    from datetime import datetime, date
    
    # Demo table formatting
    headers = ["Name", "Age", "City"]
    rows = [
        ["Alice", "25", "New York"],
        ["Bob", "30", "Los Angeles"],
        ["Charlie", "35", "Chicago"]
    ]
    
    print(TableFormatter.format_table(headers, rows, "Sample Table"))
    print("\n" + "=" * 50 + "\n")
    
    # Demo date formatting
    now = datetime.now()
    print(f"Current date: {DateTimeFormatter.format_date(now)}")
    print(f"Current datetime: {DateTimeFormatter.format_datetime(now)}")
    print(f"Time ago: {DateTimeFormatter.format_time_ago(datetime(2024, 1, 1))}")


if __name__ == "__main__":
    demo_formatters()
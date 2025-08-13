"""
Base classes for the Library Management System.
Demonstrates OOP principles: Inheritance, Encapsulation, Abstraction.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any
import uuid


class BaseEntity(ABC):
    """
    Abstract base class for all entities in the system.
    Demonstrates: Abstraction, Encapsulation
    """
    
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self) -> str:
        """Get entity ID (read-only)"""
        return self._id
    
    @property
    def created_at(self) -> datetime:
        """Get creation timestamp (read-only)"""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp"""
        return self._updated_at
    
    def _update_timestamp(self):
        """Update the timestamp when entity is modified"""
        self._updated_at = datetime.now()
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation"""
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> 'BaseEntity':
        """Create entity from dictionary data"""
        pass
    
    def __eq__(self, other) -> bool:
        """Compare entities by ID"""
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash function based on ID"""
        return hash(self._id)


class Searchable(ABC):
    """
    Interface for searchable entities.
    Demonstrates: Interface segregation principle
    """
    
    @abstractmethod
    def matches_search(self, query: str) -> bool:
        """Check if entity matches search query"""
        pass


class Validatable(ABC):
    """
    Interface for entities that can be validated.
    Demonstrates: Single Responsibility Principle
    """
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate entity data"""
        pass
    
    @abstractmethod
    def get_validation_errors(self) -> list:
        """Get list of validation errors"""
        pass
# unit_of_work.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Callable
from repository.income_repository import IncomeRepository
from repository.expense_repository import ExpenseRepository
from repository.bank_account_repository import BankAccountRepository
from repository.category_repository import CategoryRepository


# Abstract Unit of Work Base
class UnitOfWorkBase(ABC):
    incomes: IncomeRepository
    expenses: ExpenseRepository
    bank_accounts: BankAccountRepository
    categories: CategoryRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    def commit(self):
        """Commit the current transaction."""
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollback the current transaction."""
        raise NotImplementedError()


# Concrete Unit of Work Implementation

class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self._session = None
        self.incomes = None
        self.expenses = None
        self.bank_accounts = None
        self.categories = None

    def __enter__(self):
        self._session = self._session_factory()  # Start a new session
        self.incomes = IncomeRepository(self._session)
        self.expenses = ExpenseRepository(self._session)
        self.bank_accounts = BankAccountRepository(self._session)
        self.categories = CategoryRepository(self._session)
        return super().__enter__() # Returning self ensures that the repositories are accessible

    def commit(self):
        """Commit the current transaction."""
        self._session.commit()

    def rollback(self):
        """Rollback the current transaction."""
        self._session.rollback()

    def __del__(self):
        """Ensure the session is closed after usage."""
        self._session.close()

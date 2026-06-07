from app.modules.expenses.models import Expense, ExpenseShare


class ExpenseRepository:

    @staticmethod
    def create_expense(db, expense, shares):
        db.add(expense)
        db.add_all(shares)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_expense_by_id(db, expense_id):
        return (
            db.query(Expense)
            .filter(Expense.expense_id == expense_id)
            .first()
        )

    @staticmethod
    def get_group_expenses(db, group_id):
        return (
            db.query(Expense)
            .filter(Expense.group_id == group_id)
            .all()
        )

    @staticmethod
    def get_expense_shares(db, expense_id):
        return (
            db.query(ExpenseShare)
            .filter(ExpenseShare.expense_id == expense_id)
            .all()
        )

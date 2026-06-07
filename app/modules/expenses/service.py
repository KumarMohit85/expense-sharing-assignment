from uuid import uuid4

from fastapi import HTTPException

from app.modules.groups.repository import GroupRepository
from app.modules.users.repository import UserRepository

from .models import Expense, ExpenseShare
from .repository import ExpenseRepository


class ExpenseService:
    @staticmethod
    def create_expense(payload, db):
        group = GroupRepository.get_group_by_id(
            db,
            payload.group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        payer = UserRepository.get_user_by_id(
            db,
            payload.paid_by
        )

        if not payer:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        members = GroupRepository.get_members(
            db,
            payload.group_id
        )

        member_ids = [member.user_id for member in members]

        if payload.paid_by not in member_ids:
            raise HTTPException(
                status_code=400,
                detail="Payer is not a member of this group"
            )

        expense = Expense(
            expense_id=str(uuid4()),
            group_id=payload.group_id,
            paid_by=payload.paid_by,
            amount=payload.amount,
            description=payload.description
        )

        # split equally among all group members
        total_members = len(member_ids)
        equal_share = round(payload.amount / total_members, 2)

        shares = []
        for user_id in member_ids:
            shares.append(
                ExpenseShare(
                    expense_id=expense.expense_id,
                    user_id=user_id,
                    share_amount=equal_share
                )
            )

        # adjust the last share so the total matches the amount
        shares[-1].share_amount = round(
            payload.amount - equal_share * (total_members - 1),
            2
        )

        expense = ExpenseRepository.create_expense(db, expense, shares)
        
        return {
            "expense_id": expense.expense_id,
            "group_id": expense.group_id,
            "paid_by": {
                "user_id": payer.user_id,
                "name": payer.name
            },
            "amount": expense.amount,
            "description": expense.description,
            "created_at": expense.created_at
        }

    @staticmethod
    def get_expense_by_id(expense_id, db):
        expense = ExpenseRepository.get_expense_by_id(
            db,
            expense_id
        )

        if not expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        user = UserRepository.get_user_by_id(db, expense.paid_by)
        
        return {
            "expense_id": expense.expense_id,
            "group_id": expense.group_id,
            "paid_by": {
                "user_id": user.user_id,
                "name": user.name
            },
            "amount": expense.amount,
            "description": expense.description,
            "created_at": expense.created_at
        }

    @staticmethod
    def get_group_expenses(group_id, db):
        group = GroupRepository.get_group_by_id(
            db,
            group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        expenses = ExpenseRepository.get_group_expenses(db, group_id)
        
        result = []
        for expense in expenses:
            user = UserRepository.get_user_by_id(db, expense.paid_by)
            result.append({
                "expense_id": expense.expense_id,
                "group_id": expense.group_id,
                "paid_by": {
                    "user_id": user.user_id,
                    "name": user.name
                },
                "amount": expense.amount,
                "description": expense.description,
                "created_at": expense.created_at
            })
        
        return result

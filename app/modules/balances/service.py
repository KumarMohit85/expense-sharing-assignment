from fastapi import HTTPException

from app.modules.expenses.repository import ExpenseRepository
from app.modules.groups.repository import GroupRepository
from app.modules.users.repository import UserRepository


class BalanceService:
    @staticmethod
    def get_group_balances(group_id, db):
        group = GroupRepository.get_group_by_id(db, group_id)

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        members = GroupRepository.get_members(db, group_id)

        
        balances = {}
        for member in members:
            balances[member.user_id] = 0

        expenses = ExpenseRepository.get_group_expenses(db, group_id)

        for expense in expenses:
           
            balances[expense.paid_by] += expense.amount

            
            shares = ExpenseRepository.get_expense_shares(
                db,
                expense.expense_id
            )

            for share in shares:
                balances[share.user_id] -= share.share_amount

        result = []
        for member in members:
            user = UserRepository.get_user_by_id(db, member.user_id)

            result.append({
                "user_id": member.user_id,
                "name": user.name,
                "balance": round(balances[member.user_id], 2)
            })

        return result

    @staticmethod
    def get_pairwise_balances(group_id, db):
       
        group = GroupRepository.get_group_by_id(db, group_id)

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        members = GroupRepository.get_members(db, group_id)
        
        user_map = {}
        for member in members:
            user = UserRepository.get_user_by_id(db, member.user_id)
            user_map[member.user_id] = {
                "user_id": member.user_id,
                "name": user.name
            }

        pairwise_debts = {}
        
        expenses = ExpenseRepository.get_group_expenses(db, group_id)

        for expense in expenses:
            payer = user_map[expense.paid_by]
            payer_name = payer["name"]

            shares = ExpenseRepository.get_expense_shares(db, expense.expense_id)

            for share in shares:
               
                if share.user_id == expense.paid_by:
                    continue

                debtor_name = user_map[share.user_id]["name"]
                
                
                if debtor_name not in pairwise_debts:
                    pairwise_debts[debtor_name] = {"owes": {}}

                
                if payer_name not in pairwise_debts[debtor_name]["owes"]:
                    pairwise_debts[debtor_name]["owes"][payer_name] = 0

                pairwise_debts[debtor_name]["owes"][payer_name] = round(
                    pairwise_debts[debtor_name]["owes"][payer_name] + share.share_amount, 2
                )

       
        for debtor in list(pairwise_debts.keys()):
            for creditor in list(pairwise_debts[debtor]["owes"].keys()):
                if pairwise_debts[debtor]["owes"][creditor] == 0:
                    del pairwise_debts[debtor]["owes"][creditor]
            if not pairwise_debts[debtor]["owes"]:
                del pairwise_debts[debtor]

        return pairwise_debts

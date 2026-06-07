from app.modules.balances.service import BalanceService


class SettlementService:
    @staticmethod
    def get_settlement_suggestions(group_id, db):
        """
        Smart Settlement Suggestions using greedy algorithm.
        
        Algorithm:
        1. Calculate net balance for each user
        2. Separate into debtors (negative) and creditors (positive)
        3. Sort by absolute amount (largest first)
        4. Greedily match largest debtor with largest creditor
        5. Generate minimal settlement transactions
        
        This minimizes the number of transactions needed.
        """
        balances = BalanceService.get_group_balances(group_id, db)

        # Separate users by balance
        debtors = [b for b in balances if b["balance"] < 0]
        creditors = [b for b in balances if b["balance"] > 0]

        # Sort by absolute amount (largest first) for optimal greedy matching
        debtors.sort(key=lambda x: x["balance"])  # Most negative first
        creditors.sort(key=lambda x: x["balance"], reverse=True)  # Most positive first

        settlements = []
        i = 0  # debtor index
        j = 0  # creditor index

        while i < len(debtors) and j < len(creditors):
            # Amount debtor owes
            amount_owed = -debtors[i]["balance"]
            # Amount creditor should receive
            amount_to_receive = creditors[j]["balance"]

            # Settle the minimum of what's owed and what should be received
            settlement_amount = round(min(amount_owed, amount_to_receive), 2)

            if settlement_amount > 0:
                settlements.append({
                    "from_user": {
                        "user_id": debtors[i]["user_id"],
                        "name": debtors[i]["name"]
                    },
                    "to_user": {
                        "user_id": creditors[j]["user_id"],
                        "name": creditors[j]["name"]
                    },
                    "amount": settlement_amount
                })

            # Update remaining balances
            debtors[i]["balance"] += settlement_amount
            creditors[j]["balance"] -= settlement_amount

            # Move to next person if current one is settled
            if round(debtors[i]["balance"], 2) >= -0.01:
                i += 1

            if round(creditors[j]["balance"], 2) <= 0.01:
                j += 1

        return settlements

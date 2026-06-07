from fastapi import FastAPI

from app.modules.users.router import router as users_router
from app.modules.groups.router import router as groups_router
from app.modules.expenses.router import router as expenses_router
from app.modules.balances.router import router as balances_router
from app.modules.settlements.router import router as settlements_router

app = FastAPI()

app.include_router(users_router)
app.include_router(groups_router)
app.include_router(expenses_router)
app.include_router(balances_router)
app.include_router(settlements_router)
@app.get("/")
def home():
    return "Expense sharing service started"
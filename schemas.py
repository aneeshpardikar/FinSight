from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username :str
    password : str

class PortfolioAdd(BaseModel):
    symbol : str 
    quantity : int
    buy_price : float

class ChatMessage(BaseModel):
    content : str


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str


class BudgetUpdate(BaseModel):
    monthly_amount: float

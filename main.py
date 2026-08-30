from datetime import datetime, timedelta, timezone
import hmac
import os

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from groq import Groq
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing. Add a long random SECRET_KEY to your .env file.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expires_at}, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_hashed_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate your login session.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_error
    return user


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    username = user.username.strip()
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    new_user = models.User(username=username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully."}


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    matching_users = db.query(models.User).filter(models.User.username == user.username.strip()).all()
    matched_user = None
    matched_user_has_hash = False

    # This also supports duplicate legacy accounts created before username checks existed.
    for db_user in matching_users:
        try:
            is_hashed_password = db_user.password.startswith("$2")
            password_is_correct = (
                verify_hashed_password(user.password, db_user.password)
                if is_hashed_password
                else hmac.compare_digest(user.password, db_user.password)
            )
        except (ValueError, TypeError):
            password_is_correct = False

        if password_is_correct:
            matched_user = db_user
            matched_user_has_hash = is_hashed_password
            break

    if matched_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")

    if not matched_user_has_hash:
        matched_user.password = hash_password(user.password)
        db.commit()

    return {"access_token": create_access_token(matched_user.id), "token_type": "bearer"}


@app.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}


@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    import yfinance as yf

    info = yf.Ticker(symbol).info
    return {
        "current price": info["currentPrice"],
        "market_cap": info["marketCap"],
        "high_52week": info["fiftyTwoWeekHigh"],
        "low_52week": info["fiftyTwoWeekLow"],
    }


@app.post("/portfolio")
def add_portfolio(
    portfolio: schemas.PortfolioAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_portfolio = models.Portfolio(
        user_id=current_user.id,
        symbol=portfolio.symbol,
        quantity=portfolio.quantity,
        buy_price=portfolio.buy_price,
    )
    db.add(new_portfolio)
    db.commit()
    return {"message": "Portfolio item added."}


@app.get("/portfolio")
def get_portfolio(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).all()


@app.post("/expenses")
def add_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if expense.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expense amount must be greater than zero.")
    new_expense = models.Expense(
        user_id=current_user.id,
        description=expense.description.strip(),
        amount=expense.amount,
        category=expense.category.strip(),
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == current_user.id)
        .order_by(models.Expense.created_at.desc())
        .all()
    )


@app.delete("/expenses/{id}")
def delete_expense(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == id, models.Expense.user_id == current_user.id).first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted."}


@app.get("/budget")
def get_budget(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    budget = db.query(models.Budget).filter(models.Budget.user_id == current_user.id).first()
    return {"monthly_amount": budget.monthly_amount if budget else 0}


@app.put("/budget")
def update_budget(
    budget_data: schemas.BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if budget_data.monthly_amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget cannot be negative.")
    budget = db.query(models.Budget).filter(models.Budget.user_id == current_user.id).first()
    if budget is None:
        budget = models.Budget(user_id=current_user.id, monthly_amount=budget_data.monthly_amount)
        db.add(budget)
    else:
        budget.monthly_amount = budget_data.monthly_amount
    db.commit()
    return {"monthly_amount": budget_data.monthly_amount}


@app.delete("/portfolio/{id}")
def delete_portfolio(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id, models.Portfolio.user_id == current_user.id).first()
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio item not found.")
    db.delete(portfolio)
    db.commit()
    return {"message": "Portfolio item deleted."}


@app.post("/chat")
def chat(message: schemas.ChatMessage, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a stock market analyst. Give short, direct answers in 2-3 sentences only. No lengthy explanations."},
            {"role": "user", "content": message.content},
        ],
    )
    reply = response.choices[0].message.content
    db.add(models.Message(user_id=current_user.id, role="user", content=message.content))
    db.add(models.Message(user_id=current_user.id, role="assistant", content=reply))
    db.commit()
    return {"response": reply}


@app.get("/history")
def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Message).filter(models.Message.user_id == current_user.id).all()

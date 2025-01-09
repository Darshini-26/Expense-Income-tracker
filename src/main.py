from fastapi import FastAPI
#from router.upload import router as upload_router
from router.category import router as category_router
from router.user import router as user_router
from router.income import router as income_router
from router.expense import router as expense_router
from router.bank_account_routes import router as bank_account_router
from router.download import router as download_router
from router.upload import router as upload_router

app = FastAPI()

# Include the routers
app.include_router(user_router)
app.include_router(upload_router)
app.include_router(income_router)
app.include_router(expense_router)
app.include_router(bank_account_router)
app.include_router(category_router)
app.include_router(download_router)
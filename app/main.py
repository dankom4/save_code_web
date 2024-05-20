from fastapi import FastAPI

from app.crud.user import router as user_router
from app.crud.admin import router as admin_router
from app.crud.table import router as table_router


app = FastAPI()
app.include_router(router=user_router)
app.include_router(router=admin_router)
app.include_router(router=table_router)

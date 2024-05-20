from typing import Annotated

from fastapi import Depends

from app.utils.unitofwork import UnitOfWork, IUnitOfWork


UOWDp = Annotated[IUnitOfWork, Depends(UnitOfWork)]
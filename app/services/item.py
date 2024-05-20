from app.utils.unitofwork import UnitOfWork


class ItemServices:
    def __init__(self):
        self.uow = UnitOfWork()

    async def get_items(self):
        async with self.uow:
            res = await self.uow.item.find_all()
            return res

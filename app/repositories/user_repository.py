from prisma import Prisma
from prisma.models import User
from app.repositories.interfaces import IUserRepository
from app.domains.dtos.user_dto import UserCreateDTO


class UserRepository(IUserRepository):

    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def create(self, user: UserCreateDTO):
        async with self.prisma as db:
            data = await db.user.create(
                data=user.model_dump()
            )
        return data

    async def read_one(self, user_id: int):
        async with self.prisma as db:
            data = await db.user.find_first_or_raise(
                where={"id": user_id}
            )
        return data

    async def read_all(self):
        async with self.prisma as db:
            data = await db.user.find_many()
        return data

    async def update(self, _id: int, user_data: dict):
        async with self.prisma as db:
            data = await db.user.update(
                where={"id": _id},
                data=user_data
            )

        return data

    async def delete(self, user: User):
        async with self.prisma as db:
            data = await db.user.delete(
                where={"id": user.id}
            )
        return data

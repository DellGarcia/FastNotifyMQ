from abc import ABC, abstractmethod
from app.domain.dtos.user_dto import UserCreateDTO
from prisma.models import User


class IUserRepository(ABC):

    @abstractmethod
    async def create(self, user: UserCreateDTO):
        raise NotImplementedError

    @abstractmethod
    async def read_one(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def read_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update(self, _id: int, user_data: User):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User):
        raise NotImplementedError

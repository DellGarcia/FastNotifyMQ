import logging

from prisma.errors import UniqueViolationError, RecordNotFoundError

from fastapi import HTTPException
from pydantic import TypeAdapter

from app.repositories.user_repository import IUserRepository
from app.domains.dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO

logger = logging.getLogger("fastapi")


class IUserService:

    def create_user(self, user_data: UserCreateDTO):
        raise NotImplementedError

    def read_user(self, user_id: int):
        raise NotImplementedError

    def read_all(self):
        raise NotImplementedError

    def update_user(self, user_id: int, user_update: UserUpdateDTO):
        raise NotImplementedError

    def delete_user(self, user_id: int):
        raise NotImplementedError


class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        try:
            logger.info("Creating user: %s", user_data)
            created_user = await self.user_repository.create(user_data)
        except UniqueViolationError as e:
            logger.error("Error creating user: %s. Detail: %s", user_data, e)
            raise HTTPException(status_code=409, detail=f"User already exists. Error: {e.args[0]}")
        return TypeAdapter(UserDTO).validate_python(created_user)

    async def read_user(self, user_id: int) -> UserDTO:
        logger.info("Reading user with id %s", user_id)
        try:
            user = await self.user_repository.read_one(user_id)
        except RecordNotFoundError as e:
            logger.error("User with id %s not found. Detail: %s", user_id, e)
            raise HTTPException(status_code=404, detail="User not found")
        return TypeAdapter(UserDTO).validate_python(user)

    async def read_all(self) -> list[UserDTO]:
        logger.info("Finding all users")
        users = await self.user_repository.read_all()
        return [TypeAdapter(UserDTO).validate_python(user) for user in users]

    async def update_user(self, user_id: int, user_data: UserUpdateDTO) -> UserDTO:
        logger.info("Updating user with id %s", user_id)
        user = await self.user_repository.read_one(user_id)
        if user is None:
            logger.error("User with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        updated_user = await self.user_repository.update(user, user_data)
        return TypeAdapter(UserDTO).validate_python(updated_user)

    async def delete_user(self, user_id: int) -> int:
        logger.info("Deleting user with id %s", user_id)
        user = await self.user_repository.read_one(user_id)
        if user is None:
            logger.error("User with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        return await self.user_repository.delete(user)

from fastapi import APIRouter, Depends
from prisma import Prisma

from app.domain.dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


user_router = APIRouter(prefix="/users", tags=["Users"])


def get_user_repo() -> UserRepository:
    return UserRepository(Prisma())


@user_router.post("/", status_code=201, description="Cadastra um usuário", response_model=UserDTO)
async def create(request: UserCreateDTO, user_repo: UserRepository = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    return await user_service.create_user(request)


@user_router.get("/{user_id}", status_code=200, description="Busca um usuário pelo ID", response_model=UserDTO)
async def find_by_id(user_id: int, user_repo: UserRepository = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    return await user_service.read_user(user_id)


@user_router.get("/", status_code=200, description="Busca todos os usuários", response_model=list[UserDTO])
async def find_all(user_repo: UserRepository = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    return await user_service.read_all()


@user_router.put("/{user_id}", status_code=200, description="Atualiza um usuário", response_model=UserDTO)
async def update(user_id: int, request: UserUpdateDTO, user_repo: UserRepository = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    return await user_service.update_user(user_id, request)


@user_router.delete("/{user_id}", status_code=204, description="Deleta um usuário")
async def delete(user_id: int, user_repo: UserRepository = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    return await user_service.delete_user(user_id)

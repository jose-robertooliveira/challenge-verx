from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.crud import producer as crud
from app.database import get_session
from app.schemas.producer import ProducerCreate, ProducerList, ProducerResponse, ProducerUpdate

router = APIRouter(prefix="/producers", tags=["producers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_producer(
    producer: ProducerCreate,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProducerResponse:
    """
    Cria um novo produtor no sistema.
    - Dados obrigatórios do produtor (CPF/CNPJ, nome, áreas, etc.)
    - CPF/CNPJ deve ser único seguindo os padrões de validação,
    - também as areas hectares devem ser maiores que zero com virgula, e
    - adicionando o alias (ha) após os números.
    """

    logger.info(f"Creating producer: {producer.name}")
    created = await crud.create_producer(db=db, producer=producer)
    logger.info(f"Producer created with ID: {created.id}")
    return created


@router.get("/{producer_id}")
async def read_producer(
    producer_id: int,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProducerResponse:
    """Retorna os dados de um produtor pelo ID"""
    db_producer = await crud.get_producer(db, producer_id=producer_id)
    if db_producer is None:
        logger.warning(f"Producer ID {producer_id} not found.")
        raise HTTPException(status_code=404, detail="Producer not found")
    logger.info(f"Producer found: {db_producer.name}")
    return db_producer


@router.get("/")
async def read_producers(
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 10,
) -> ProducerList:
    """
    Retorna lista paginada de produtores cadastrados.
    """
    logger.info(f"Request to list producers: skip={skip}, limit={limit}")
    producers = await crud.get_producers(db, skip=skip, limit=limit)
    return ProducerList(producers=producers, total=len(producers), page=skip, size=limit)


@router.put("/{producer_id}")
async def update_producer(
    producer_id: int,
    updates: ProducerUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProducerResponse:
    """
    Atualiza os dados do produtor pelo ID.
    - producer_id: ID do produtor a ser atualizado
    """
    logger.info(f"Request to update producer ID: {producer_id}")
    return await crud.update_producer(db=db, producer_id=producer_id, updates=updates)


@router.delete("/{producer_id}")
async def delete_producer(
    producer_id: int,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProducerResponse:
    """Deleta um produtor existente passando o ID."""
    logger.info(f"Request to delete producer ID: {producer_id}")
    return await crud.delete_producer(db=db, producer_id=producer_id)

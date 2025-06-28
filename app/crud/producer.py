from typing import List

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.producer import Producer
from app.schemas.producer import ProducerCreate, ProducerUpdate


async def create_producer(db: AsyncSession, producer: ProducerCreate) -> Producer:
    db_producer = Producer(**producer.model_dump())
    try:
        logger.info(f"Attempting to create producer: {producer.name}")
        db.add(db_producer)
        await db.commit()
        await db.refresh(db_producer)
        logger.info(f"Producer created successfully with ID: {db_producer.id}")
    except IntegrityError:
        await db.rollback()
        logger.warning("IntegrityError: CPF/CNPJ already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Producer with given CPF/CNPJ already exists.",
        )
    return db_producer


async def get_producer(db: AsyncSession, producer_id: int) -> Producer:
    logger.info(f"Fetching producer with ID: {producer_id}")
    result = await db.execute(select(Producer).filter(Producer.id == producer_id))
    producer = result.scalar_one_or_none()
    if not producer:
        logger.warning(f"Producer ID {producer_id} not found in get_producer.")
    return producer


async def get_producers(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Producer]:
    logger.info(f"Fetching producers: skip={skip}, limit={limit}")
    result = await db.execute(select(Producer).offset(skip).limit(limit))
    return result.scalars().all()


async def update_producer(
    db: AsyncSession, producer_id: int, updates: ProducerUpdate
) -> Producer:
    logger.info(f"Updating producer ID: {producer_id}")
    db_producer = await get_producer(db, producer_id)
    if not db_producer:
        logger.warning(f"Producer ID {producer_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producer not found."
        )

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_producer, key, value)

    await db.commit()
    await db.refresh(db_producer)
    logger.info(f"Producer ID {producer_id} updated successfully.")
    return db_producer


async def delete_producer(db: AsyncSession, producer_id: int) -> JSONResponse:
    logger.info(f"Deleting producer ID: {producer_id}")
    db_producer = await get_producer(db, producer_id)
    if not db_producer:
        logger.warning(f"Producer ID {producer_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producer not found."
        )

    await db.delete(db_producer)
    await db.commit()
    logger.info(f"Producer ID {producer_id} deleted successfully.")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Producer with ID {producer_id} deleted successfully."},
    )

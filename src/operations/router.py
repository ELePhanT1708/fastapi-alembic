import random
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    res = []
    for row in result.all():
        res.append(list(row))

    return res
    # print(res)

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get('/fill')
async def fill_the_db_with_random_info(session: AsyncSession = Depends(get_async_session)):
    quantity = ['1.23', '2.54', '65.43', '345.38', '0.54']
    print(quantity)
    figis = ['AUD'
            'GBP',
            'EUR',
            'PY',
            'CHF',
            'USD',
            'AFN',
            'ALL',
            'DZD',
            'AOA',
            'ARS',
            'AMD'
            ]
    instrument_type = ['hammer', 'zipper', 'scissiors']

    types = ['usual', 'casual', 'sophisticated']
    for i in range(1000):
        dates = datetime.utcnow()
        stmt = insert(operation).values(
            {'quantity': random.choice(quantity),
             'figi': random.choice(figis),
             'instrument_type': random.choice(instrument_type),
             'date': dates,
             'type': random.choice(types)
             })
        await session.execute(stmt)
        await session.commit()
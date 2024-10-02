from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update
from db_models import Users
from os import getenv
from datetime import datetime

DATABASE_URL = f"mysql+aiomysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_SCHEME')}"
async_engine = create_async_engine(DATABASE_URL, pool_recycle=299, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

async def reg_user(tg_id, name):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            existing_user = result.scalar()
            if existing_user:
                return False
            else:
                user = Users(
                    tg_id=tg_id, 
                    name=name,
                    degreas_percent=-5,
                    increas_percent=5,
                    signal_interval=[1440],
                    signals_history="",
                    email="",
                    lang='en'
                )
                session.add(user)
                await session.commit()
                return True
        except SQLAlchemyError as err:
            print(err)
            return False

async def get_user_info(tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            return user if user else None
        except SQLAlchemyError as err:
            print(err)
            return False

async def get_lang(tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            return user.lang if user else None
        except SQLAlchemyError as err:
            print(err)
            return False

async def change_lang(tg_id, lang):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            if user:
                user.lang = lang
                await session.commit()
                return True
            return False
        except SQLAlchemyError as err:
            print(err)
            return False

async def set_degreas_percent(percent, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            if user and percent != user.degreas_percent:
                user.degreas_percent = percent
                await session.commit()
                return True
            return False
        except SQLAlchemyError as err:
            print(err)
            return False

async def set_increas_percent(percent, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            if user and percent != user.increas_percent:
                user.increas_percent = percent
                await session.commit()
                return True
            return False
        except SQLAlchemyError as err:
            print(err)
            return False

async def get_all_users():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users))
            users = result.scalars().all()
            return users
        except SQLAlchemyError as err:
            print(err)
            return []
        
async def reset_signals_history():
    async with AsyncSessionLocal() as session:
        try:
            stmt = update(Users).values(signals_history="").execution_options(synchronize_session="fetch")
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as err:
            print(err)

async def set_signal_interval(interval, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            if user:
                current_intervals = user.signal_interval
                if interval not in current_intervals:
                    current_intervals.append(interval)
                    await session.execute(
                        update(Users).where(Users.tg_id == tg_id).values(signal_interval=current_intervals)
                    )
                    await session.commit()
                    return True
            return False
        except SQLAlchemyError as err:
            print(err)
            return False

async def delete_signal_interval(interval, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()
            if user:
                current_intervals = user.signal_interval
                if interval in current_intervals:
                    current_intervals.remove(interval)
                    await session.execute(
                        update(Users).where(Users.tg_id == tg_id).values(signal_interval=current_intervals)
                    )
                    await session.commit()
                    return True
            return False
        except SQLAlchemyError as err:
            print(err)
            return False
        
        
async def add_signal_history(text, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()  
            if user:
                updated_text = f"{text}\n[{current_time}]"
                if user.signals_history:
                    user.signals_history += f"\n\n{updated_text}"
                else:
                    user.signals_history = updated_text
                await session.commit()
                return True
            
            return False
        
        except SQLAlchemyError as err:
            print(err)
            return False
        
async def bind_mail(email, tg_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Users).filter_by(tg_id=tg_id))
            user = result.scalar()  
            if user:
                user.email = email
                await session.commit()
                return True
            
            return False
        
        except SQLAlchemyError as err:
            print(err)
            return False

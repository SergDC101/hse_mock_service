import asyncio
from src.database import get_async_session
from sqlalchemy import text

async def main():
    async for session in get_async_session():
        try:
            await session.execute(
                text(
                    """
                        INSERT INTO public.role(id, name, permissions)
                        VALUES (1, 'user', null);
                    """
                )
            )
            await session.commit()
            print(f"Таблица role заполнена")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при вставке данных: {e}")
            raise
        finally:
            
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())
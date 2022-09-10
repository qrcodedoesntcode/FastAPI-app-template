from faker import Faker
import os.path
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import async_session
from app.modules.admin.models import User

fake = Faker()


async def generate():
    async with async_session() as session:
        session.add_all(
            [
                User(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password=fake.password(),
                    is_active=True,
                )
                for _ in range(1000)
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(generate())

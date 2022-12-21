import asyncio
import os.path
import sys

from faker import Faker

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import async_session
from app.modules.core.models import Permission, Role, User

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
                for _ in range(100_000)
            ]
        )

        session.add_all(
            [
                Role(
                    name=fake.unique.text(max_nb_chars=50),
                    description=fake.text(max_nb_chars=255),
                )
                for _ in range(5000)
            ]
        )

        session.add_all(
            [
                Permission(
                    scope=fake.unique.text(max_nb_chars=50),
                    description=fake.text(max_nb_chars=255),
                )
                for _ in range(5000)
            ]
        )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(generate())

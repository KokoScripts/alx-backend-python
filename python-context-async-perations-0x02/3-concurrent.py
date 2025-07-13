import asyncio
import aiosqlite

DB_PATH = "my_database.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
    return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
    return users

async def fetch_concurrently():
    users_all, users_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users_all)
    print("Users older than 40:", users_older)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

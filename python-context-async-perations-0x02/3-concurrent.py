import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('user_data.db') as conn:
        async with conn.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            return users
        
async def async_fetch_older_users():
    async with aiosqlite.connect('user_data.db') as conn:
        async with conn.execute('SELECT * FROM users WHERE AGE > 40') as cursor:
            older_users = await cursor.fetchall()
            return older_users
        
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users: ", all_users)
    print("Users older than 40: ", older_users)
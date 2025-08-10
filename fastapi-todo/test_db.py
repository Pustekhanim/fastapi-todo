import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        print("✅ Connected successfully to PostgreSQL!")
        await conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

import asyncio
asyncio.run(test_connection())

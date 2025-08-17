"""
Database connection module for PostgreSQL using asyncpg.

This module provides connection pooling and database utilities for the FastAPI application.
"""

import os
from typing import Optional

import asyncpg


# Global connection pool
CONNECTION_POOL: Optional[asyncpg.Pool] = None


async def create_pool() -> asyncpg.Pool:
    """
    Create a connection pool to the PostgreSQL database.

    Returns:
        asyncpg.Pool: Database connection pool.
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_T8aYtSLp1lqc@ep-orange-violet-aeh16aj4-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    )

    return await asyncpg.create_pool(
        database_url, min_size=1, max_size=10, command_timeout=60
    )


async def get_pool() -> asyncpg.Pool:
    """
    Get the database connection pool, creating it if it doesn't exist.

    Returns:
        asyncpg.Pool: Database connection pool.
    """
    global CONNECTION_POOL
    if CONNECTION_POOL is None:
        CONNECTION_POOL = await create_pool()
    return CONNECTION_POOL


async def close_pool() -> None:
    """
    Close the database connection pool.
    """
    global CONNECTION_POOL
    if CONNECTION_POOL:
        await CONNECTION_POOL.close()
        CONNECTION_POOL = None


async def get_connection() -> asyncpg.Connection:
    """
    Get a database connection from the pool.

    Returns:
        asyncpg.Connection: Database connection.
    """
    pool = await get_pool()
    return await pool.acquire()


async def release_connection(connection: asyncpg.Connection) -> None:
    """
    Release a database connection back to the pool.

    Args:
        connection: The database connection to release.
    """
    pool = await get_pool()
    await pool.release(connection)


class DatabaseConnection:
    """
    Context manager for database connections.

    Usage:
        async with DatabaseConnection() as conn:
            result = await conn.fetch("SELECT * FROM users")
    """

    def __init__(self):
        self.connection: Optional[asyncpg.Connection] = None

    async def __aenter__(self) -> asyncpg.Connection:
        """Enter the async context manager."""
        self.connection = await get_connection()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager."""
        if self.connection:
            await release_connection(self.connection)

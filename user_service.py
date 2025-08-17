"""
User service module for database operations.
"""

from typing import List, Optional
from uuid import UUID

from db import DatabaseConnection
from main import UserModel


async def create_user_in_db(user: UserModel) -> UserModel:
    """
    Create a new user in the database.

    Args:
        user: User model to create.

    Returns:
        UserModel: Created user with database-generated fields.
    """
    async with DatabaseConnection() as conn:
        query = """
        INSERT INTO users (user_id, email_id, auth_provider, provider_id, 
                          first_name, middle_name, last_name, phone_number, 
                          created_at, modified_at, bookmarks, likes)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING *
        """

        result = await conn.fetchrow(
            query,
            user.user_id,
            user.email_id,
            user.auth_provider,
            user.provider_id,
            user.first_name,
            user.middle_name,
            user.last_name,
            user.phone_number,
            user.created_at,
            user.modified_at,
            user.bookmarks,
            user.likes,
        )

        return UserModel(**dict(result))


async def get_user_by_id(user_id: UUID) -> Optional[UserModel]:
    """
    Get a user by their ID.

    Args:
        user_id: The user's UUID.

    Returns:
        UserModel or None: The user if found, None otherwise.
    """
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM users WHERE user_id = $1"
        result = await conn.fetchrow(query, user_id)

        if result:
            return UserModel(**dict(result))
        return None


async def get_all_users() -> List[UserModel]:
    """
    Get all users from the database.

    Returns:
        List[UserModel]: List of all users.
    """
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = await conn.fetch(query)

        return [UserModel(**dict(row)) for row in results]

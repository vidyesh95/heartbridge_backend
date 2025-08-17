"""
Database operations for the FastAPI application.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from db import DatabaseConnection


# Example: Create a user
async def create_user(user_data: dict) -> dict:
    """
    Create a new user in the database.

    Args:
        user_data: Dictionary containing user information

    Returns:
        dict: Created user data
    """
    async with DatabaseConnection() as conn:
        query = """
        INSERT INTO users (user_id, email_id, first_name, last_name, created_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
        """

        result = await conn.fetchrow(
            query,
            user_data["user_id"],
            user_data["email_id"],
            user_data["first_name"],
            user_data["last_name"],
            user_data["created_at"],
        )

        return dict(result)


# Example: Get user by ID
async def get_user_by_id(user_id: UUID) -> Optional[dict]:
    """
    Get a user by their ID.

    Args:
        user_id: The user's UUID

    Returns:
        dict or None: User data if found, None otherwise
    """
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM users WHERE user_id = $1"
        result = await conn.fetchrow(query, user_id)

        if result:
            return dict(result)
        return None


# Example: Get all users
async def get_all_users() -> List[dict]:
    """
    Get all users from the database.

    Returns:
        List[dict]: List of all users
    """
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = await conn.fetch(query)

        return [dict(row) for row in results]


# Example: Update user
async def update_user(user_id: UUID, update_data: dict) -> Optional[dict]:
    """
    Update a user's information.

    Args:
        user_id: The user's UUID
        update_data: Dictionary containing fields to update

    Returns:
        dict or None: Updated user data if found, None otherwise
    """
    async with DatabaseConnection() as conn:
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1

        for field, value in update_data.items():
            set_clauses.append(f"{field} = ${param_count}")
            values.append(value)
            param_count += 1

        # Add modified_at timestamp
        set_clauses.append(f"modified_at = ${param_count}")
        values.append(datetime.utcnow())
        param_count += 1

        # Add user_id for WHERE clause
        values.append(user_id)

        query = f"""
        UPDATE users 
        SET {", ".join(set_clauses)}
        WHERE user_id = ${param_count}
        RETURNING *
        """

        result = await conn.fetchrow(query, *values)

        if result:
            return dict(result)
        return None


# Example: Delete user
async def delete_user(user_id: UUID) -> bool:
    """
    Delete a user from the database.

    Args:
        user_id: The user's UUID

    Returns:
        bool: True if user was deleted, False if not found
    """
    async with DatabaseConnection() as conn:
        query = "DELETE FROM users WHERE user_id = $1"
        result = await conn.execute(query, user_id)

        # Check if any rows were affected
        return result == "DELETE 1"

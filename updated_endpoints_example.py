"""
Example of how to update your FastAPI endpoints to use the database.
"""

from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from datetime import datetime, timezone

from database_operations import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)


# Example: Create user endpoint
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserModel):
    """
    Create a new user.
    """
    try:
        # Convert Pydantic model to dict
        user_data = user.dict()

        # Create user in database
        created_user = await create_user(user_data)

        return created_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )


# Example: Get user by ID
@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: UUID):
    """
    Get a user by their ID.
    """
    try:
        user = await get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}",
        )


# Example: Get all users
@app.get("/users/")
async def get_users_endpoint():
    """
    Get all users.
    """
    try:
        users = await get_all_users()
        return {"users": users, "count": len(users)}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users: {str(e)}",
        )


# Example: Update user
@app.put("/users/{user_id}")
async def update_user_endpoint(user_id: UUID, update_data: dict):
    """
    Update a user's information.
    """
    try:
        updated_user = await update_user(user_id, update_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return updated_user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}",
        )


# Example: Delete user
@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: UUID):
    """
    Delete a user.
    """
    try:
        deleted = await delete_user(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return {"message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}",
        )

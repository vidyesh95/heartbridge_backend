"""
FastAPI application main module.

This module contains the main FastAPI application with basic endpoints.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Hello World"}

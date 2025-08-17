"""
FastAPI application main module.

This module contains the main FastAPI application with basic endpoints.
"""

from datetime import datetime, timezone, date
from uuid import UUID, uuid4
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv

from db import close_pool, get_pool

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    """
    # Startup: Initialize database pool
    await get_pool()
    yield
    # Shutdown: Close database pool
    await close_pool()


# Initialize the FastAPI application
app = FastAPI(
    title="Heartbridge API",
    description="A API for offline first matrimnial website which arranges first meetup between two parties.",
    version="0.0.1",
    lifespan=lifespan,
)


# PostgreSQL database
database = {"users": {}, "profiles": {}}


class Gender(str, Enum):
    """
    Three genders Male, Female and Transgender
    """
    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"


class UserModel(BaseModel):
    """
    User is created on successful sign up with either email via otp,
    phone number via otp or by google Single Sign-On or apple Single Sign-On
    After account has been created user has option to add and verify remaining
    email id, phone number and SSO
    """

    user_id: UUID = Field(default_factory=uuid4)
    email_id: EmailStr | None = None
    phone_number: str | None = None
    auth_provider: str | None
    provider_id: str | None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    bookmarks: str
    likes: str


class ProfileModel(BaseModel):
    """
    User is able to create zero or more profiles which are than
    verified on the user request on phone number or email id
    provided by user of the profile by admin side
    """

    profile_id: UUID = Field(default_factory=uuid4)
    email_id: EmailStr | None = None
    phone_number: str | None = None
    first_name: str
    middle_name: str
    last_name: str
    gender: Gender
    birth_date: str
    height: str
    country_currently_residing: str
    citizen_of_countries: str
    annual_income: str
    personal_assets: str | None = None
    medical_history: str
    profession: str | None = None
    education: str | None = None
    religion: str | None = None
    is_verification_requested: bool = False
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel):
    """
    Create a user with either email id, phone number or SSO
    "user_id": user_id,
    "email_id": email_id,
    "phone_number": phone_number,
    "auth_provider": auth_provider,
    "provider_id": provider_id,
    "first_name": first_name,
    "last_name": last_name,
    "created_at": created_at,
    "modified_at": modified_at,
    "bookmarks": bookmarks,
    "likes": likes,
    """
    now: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    return user


@app.get("/users/{user_id}")
async def read_user(user_id: UUID):
    """
    Retrieve a user by their ID.
    """
    user = database["users"].get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@app.get("/users")
async def read_users():
    """
    Dynamic user_id endpoint build for admin to view all users
    """
    return {
        # "user_id": user_id,
    }


@app.post(
    "/users/{user_id}/profiles/", status_code=status.HTTP_201_CREATED, tags=["Profiles"]
)
async def create_profile(user_id: UUID, profile: ProfileModel):
    """
    Create a new profile for a specific user
    "profile_id": profile_id,
    "email_id": email_id,
    "phone_number": phone_number,
    "first_name": first_name,
    "middle_name": middle_name,
    "last_name": last_name,
    "gender": gender,
    "age": age,
    "height": height,
    "nationality": nationality,
    "citizenship": citizenship,
    "annual_income": annual_income,
    "personal_assets": personal_assets,
    "medical_history": medical_history,
    "profession": profession,
    "education": education,
    "religion": religion,
    "is_verified": is_verified,
    "created_at": created_at,
    "modified_at": modified_at,
    """
    # Check if user exists
    if user_id not in database["users"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    now: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    return profile


@app.get("/profiles/{profile_id}", tags=["Profiles"])
async def read_profile(profile_id: UUID):
    """
    Retrieve a profile by its ID
    """
    profile = database["profiles"].get(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


@app.get("/profiles")
async def read_profiles():
    """
    Get 10 profiles
    """
    return {
        # "user_id": user_id,
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Hello World"}
